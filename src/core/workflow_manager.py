"""
workflow_manager.py

Hanterar skapande, köning och stegbaserad exekvering av workflows.
Inkluderar stöd för asynkrona steg med tidsmätning och felhantering.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from pathlib import Path

# Fil för att spara workflows
WORKFLOWS_FILE = Path("temp/workflows.json")


class WorkflowStepType(Enum):
    FILE_ANALYSIS = "file_analysis"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    VALIDATION = "validation"
    USER_INTERACTION = "user_interaction"


@dataclass
class WorkflowStep:
    """Enstaka steg i en workflow."""
    id: UUID
    type: WorkflowStepType
    action: Callable[..., Any]
    description: str
    required: bool = True
    dependencies: List[UUID] = field(default_factory=list)
    completed: bool = False
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3
    execution_time: Optional[float] = None  # Nytt fält för att mäta tiden för steget


@dataclass
class Workflow:
    """Hela workflow-definitionen."""
    id: UUID
    name: str
    description: str
    steps: List[WorkflowStep]
    current_step: Optional[UUID] = None
    status: str = "pending"  # pending, in_progress, completed, error
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkflowManager:
    """
    Hanterar skapande, köning och exekvering av workflows.
    Använder en asynkron kö och stödjer felhantering samt tidsmätning per steg.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.workflows: Dict[UUID, Workflow] = {}
        self.active_workflow: Optional[UUID] = None
        self.workflow_queue: asyncio.Queue = asyncio.Queue()
        self._worker_task: Optional[asyncio.Task] = None
        self.step_handlers: Dict[WorkflowStepType, Callable[..., Any]] = {}
        self._initialize_handlers()
        self._load_workflows()

    def _initialize_handlers(self) -> None:
        """Initierar standardstegshanterare."""
        self.step_handlers.update({
            WorkflowStepType.FILE_ANALYSIS: self._handle_file_analysis,
            WorkflowStepType.PLANNING: self._handle_planning,
            WorkflowStepType.IMPLEMENTATION: self._handle_implementation,
            WorkflowStepType.TESTING: self._handle_testing,
            WorkflowStepType.VALIDATION: self._handle_validation,
            WorkflowStepType.USER_INTERACTION: self._handle_user_interaction
        })

    async def start_worker(self) -> None:
        """Starta workflow-arbetaren om den inte redan är igång."""
        if not self._worker_task:
            self._worker_task = asyncio.create_task(self._workflow_worker())
            self.logger.info("Workflow worker started.")

    async def shutdown(self) -> None:
        """Stäng ner workflow manager på ett graciöst sätt."""
        self.logger.info("Shutting down workflow manager...")
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                self.logger.info("Workflow worker cancelled.")
            self._worker_task = None
        self._persist_workflows()

    async def create_workflow(self, request: Dict[str, Any]) -> Workflow:
        """
        Skapa en ny workflow utifrån en request.
        Requesten bör innehålla t.ex. 'name', 'description' och flaggor (ex. 'analyze_files')
        för att bygga workflow-steget.
        """
        workflow_id = uuid4()
        steps = self._create_steps_from_request(request)
        workflow = Workflow(
            id=workflow_id,
            name=request.get("name", "Unnamed Workflow"),
            description=request.get("description", ""),
            steps=steps,
            metadata=request
        )
        self.workflows[workflow_id] = workflow
        await self.workflow_queue.put(workflow)
        self.logger.info(f"Workflow {workflow_id} created and queued.")
        self._persist_workflows()
        await self.start_worker()
        return workflow

    async def execute_workflow(self, workflow_id: UUID) -> Dict[str, Any]:
        """
        Exekvera workflow med givet ID.
        Väntar tills workflow-processen (av arbetaren) är klar.
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")

        while self.workflows[workflow_id].status in ["pending", "in_progress"]:
            await asyncio.sleep(0.5)
        return {"workflow_id": workflow_id, "status": self.workflows[workflow_id].status}

    async def _workflow_worker(self) -> None:
        """Arbetsloop som hanterar workflows från kön."""
        while True:
            try:
                workflow: Workflow = await self.workflow_queue.get()
                self.active_workflow = workflow.id
                workflow.status = "in_progress"
                self.logger.info(f"Executing workflow {workflow.id}: {workflow.name}")
                await self._execute_workflow(workflow)
                self.active_workflow = None
                self.workflow_queue.task_done()
                self._persist_workflows()
            except asyncio.CancelledError:
                self.logger.info("Workflow worker received cancellation.")
                break
            except Exception as e:
                self.logger.error(f"Error in workflow worker: {str(e)}")
                await asyncio.sleep(1)

    async def _execute_workflow(self, workflow: Workflow) -> None:
        """Exekvera varje steg i workflow med beroendehantering och tidsmätning."""
        try:
            for step in workflow.steps:
                if step.dependencies:
                    await self._check_dependencies(step, workflow)
                workflow.current_step = step.id
                step_start = datetime.now()
                handler = self.step_handlers.get(step.type)
                if handler:
                    step.result = await handler(step, workflow)
                else:
                    step.result = await step.action()
                step.completed = True
                step.execution_time = (datetime.now() - step_start).total_seconds()
                self.logger.info(f"Step {step.id} ({step.type.value}) completed in {step.execution_time:.2f} seconds.")
            workflow.status = "completed"
            workflow.completed_at = datetime.now()
            self.logger.info(f"Workflow {workflow.id} completed.")
        except Exception as e:
            workflow.status = "error"
            self.logger.error(f"Workflow {workflow.id} failed: {str(e)}")
            raise

    async def _check_dependencies(self, step: WorkflowStep, workflow: Workflow) -> None:
        """Säkerställ att alla beroenden för ett steg är uppfyllda innan exekvering."""
        for dep_id in step.dependencies:
            dep_step = next((s for s in workflow.steps if s.id == dep_id), None)
            if not dep_step or not dep_step.completed:
                raise Exception(f"Dependency {dep_id} not met for step {step.id}")

    def _create_steps_from_request(self, request: Dict[str, Any]) -> List[WorkflowStep]:
        """
        Skapa workflow-steg baserat på request.
        Exempel: om request innehåller "analyze_files" läggs ett FILE_ANALYSIS-steg till.
        Du kan utöka denna logik med fler flaggor (t.ex. plan, implement, test).
        """
        steps = []
        if request.get("analyze_files"):
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.FILE_ANALYSIS,
                action=self._handle_file_analysis,
                description="Analyze workspace files"
            ))
        if request.get("plan_workflow"):
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.PLANNING,
                action=self._handle_planning,
                description="Plan the workflow tasks"
            ))
        if request.get("implement_changes"):
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.IMPLEMENTATION,
                action=self._handle_implementation,
                description="Implement requested changes"
            ))
        if request.get("run_tests"):
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.TESTING,
                action=self._handle_testing,
                description="Execute tests"
            ))
        # Ytterligare steg kan läggas till här…
        return steps

    # Standard stegshanterare (simulerar arbete med asyncio.sleep)
    async def _handle_file_analysis(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling file analysis for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "File analysis completed", "details": workflow.metadata}

    async def _handle_planning(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling planning for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "Planning completed"}

    async def _handle_implementation(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling implementation for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "Implementation completed"}

    async def _handle_testing(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling testing for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "Testing completed"}

    async def _handle_validation(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling validation for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "Validation completed"}

    async def _handle_user_interaction(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling user interaction for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "User interaction completed"}

    def _persist_workflows(self) -> None:
        """Spara alla workflows i en JSON-fil."""
        try:
            if not WORKFLOWS_FILE.parent.exists():
                WORKFLOWS_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {}
            for wf_id, wf in self.workflows.items():
                data[str(wf_id)] = {
                    "id": str(wf.id),
                    "name": wf.name,
                    "description": wf.description,
                    "steps": [
                        {
                            "id": str(step.id),
                            "type": step.type.value,
                            "description": step.description,
                            "completed": step.completed,
                            "result": step.result,
                            "error": step.error,
                            "retries": step.retries,
                            "max_retries": step.max_retries,
                            "dependencies": [str(dep) for dep in step.dependencies],
                            "execution_time": step.execution_time
                        } for step in wf.steps
                    ],
                    "current_step": str(wf.current_step) if wf.current_step else None,
                    "status": wf.status,
                    "created_at": wf.created_at.isoformat(),
                    "completed_at": wf.completed_at.isoformat() if wf.completed_at else None,
                    "metadata": wf.metadata
                }
            with open(WORKFLOWS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error persisting workflows: {str(e)}")

    def _load_workflows(self) -> None:
        """Ladda sparade workflows från JSON-fil om den finns."""
        if WORKFLOWS_FILE.exists():
            try:
                with open(WORKFLOWS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for wf_id_str, wf_data in data.items():
                    wf_id = UUID(wf_data["id"])
                    steps = []
                    for step_data in wf_data["steps"]:
                        steps.append(WorkflowStep(
                            id=UUID(step_data["id"]),
                            type=WorkflowStepType(step_data["type"]),
                            action=self.step_handlers.get(WorkflowStepType(step_data["type"]), lambda: None),
                            description=step_data["description"],
                            required=True,
                            dependencies=[UUID(dep) for dep in step_data["dependencies"]],
                            completed=step_data["completed"],
                            result=step_data["result"],
                            error=step_data["error"],
                            retries=step_data["retries"],
                            max_retries=step_data["max_retries"],
                            execution_time=step_data.get("execution_time")
                        ))
                    workflow = Workflow(
                        id=wf_id,
                        name=wf_data["name"],
                        description=wf_data["description"],
                        steps=steps,
                        current_step=UUID(wf_data["current_step"]) if wf_data["current_step"] else None,
                        status=wf_data["status"],
                        created_at=datetime.fromisoformat(wf_data["created_at"]),
                        completed_at=datetime.fromisoformat(wf_data["completed_at"]) if wf_data["completed_at"] else None,
                        metadata=wf_data["metadata"]
                    )
                    self.workflows[wf_id] = workflow
                self.logger.info("Workflows loaded successfully.")
            except Exception as e:
                self.logger.error(f"Error loading workflows: {str(e)}")
