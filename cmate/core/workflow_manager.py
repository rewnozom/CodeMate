# ..\..\cmate\core\workflow_manager.py
"""
cmate/core/workflow_manager.py

Enhanced workflow manager with support for:
- Navigation workflows
- Multi-component operations
- Advanced state tracking
- Step-based validation
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from uuid import UUID, uuid4
import logging

from .state_manager import AgentState
from .event_bus import EventBus, EventCategory, EventPriority
from ..utils.logger import get_logger

logger = get_logger(__name__)

class WorkflowStepType(Enum):
    """Extended workflow step types"""
    WORKSPACE_SCAN = "workspace_scan"
    COMPONENT_ANALYSIS = "component_analysis"
    DEPENDENCY_ANALYSIS = "dependency_analysis"
    PATH_TRANSITION = "path_transition"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    CODE_GENERATION = "code_generation"
    CODE_MODIFICATION = "code_modification"
    TEST_GENERATION = "test_generation"
    TEST_EXECUTION = "test_execution"
    VALIDATION = "validation"
    ERROR_ANALYSIS = "error_analysis"
    RECOVERY = "recovery"

class WorkflowType(Enum):
    """Types of workflows"""
    NAVIGATION = "navigation"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    RECOVERY = "recovery"
    COMPOSITE = "composite"

@dataclass
class WorkflowStep:
    """Enhanced workflow step"""
    id: UUID
    type: WorkflowStepType
    action: Callable[..., Any]
    description: str
    required: bool = True
    dependencies: List[UUID] = field(default_factory=list)
    validation_steps: List[Callable] = field(default_factory=list)
    completed: bool = False
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3
    execution_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Workflow:
    """Enhanced workflow definition"""
    id: UUID
    type: WorkflowType
    name: str
    description: str
    steps: List[WorkflowStep]
    current_step: Optional[UUID] = None
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    parent_workflow: Optional[UUID] = None
    child_workflows: List[UUID] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowContext:
    """Context for workflow execution"""
    workflow_id: UUID
    current_path: Optional[Path] = None
    target_path: Optional[Path] = None
    components: List[Path] = field(default_factory=list)
    dependencies: Dict[Path, List[Path]] = field(default_factory=dict)
    state_history: List[AgentState] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowManager:
    """Enhanced workflow manager with navigation support"""
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        self.logger = get_logger(__name__)
        self.event_bus = event_bus or EventBus()
        self.workflows: Dict[UUID, Workflow] = {}
        self.contexts: Dict[UUID, WorkflowContext] = {}
        self.active_workflow: Optional[UUID] = None
        self._worker_task: Optional[asyncio.Task] = None
        self._running = False
        
        # Initialize step handlers
        self.step_handlers = {
            WorkflowStepType.WORKSPACE_SCAN: self._handle_workspace_scan,
            WorkflowStepType.COMPONENT_ANALYSIS: self._handle_component_analysis,
            WorkflowStepType.DEPENDENCY_ANALYSIS: self._handle_dependency_analysis,
            WorkflowStepType.PATH_TRANSITION: self._handle_path_transition,
            # Additional step handlers can be added here.
        }
        self.logger.info("WorkflowManager initialized.")
        self.logger.success("WorkflowManager initialized successfully.")

    async def start(self) -> None:
        """Start workflow processing"""
        if not self._running:
            self._running = True
            self._worker_task = asyncio.create_task(self._workflow_worker())
            self.logger.success("Workflow manager started successfully.")

    async def shutdown(self) -> None:
        """Gracefully shut down workflow processing"""
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
            self._worker_task = None
        self.logger.success("Workflow manager shut down successfully.")

    async def create_workflow(
        self,
        workflow_type: WorkflowType,
        name: str,
        description: str,
        context: Optional[Dict[str, Any]] = None,
        parent_id: Optional[UUID] = None
    ) -> Workflow:
        """Create a new workflow"""
        workflow_id = uuid4()
        self.logger.info("Creating workflow '%s' of type '%s' with id: %s", name, workflow_type.value, workflow_id)
        
        workflow_context = WorkflowContext(
            workflow_id=workflow_id,
            metadata=context or {}
        )
        self.contexts[workflow_id] = workflow_context
        
        steps = await self._create_workflow_steps(workflow_type, context or {})
        workflow = Workflow(
            id=workflow_id,
            type=workflow_type,
            name=name,
            description=description,
            steps=steps,
            parent_workflow=parent_id,
            metadata=context or {}
        )
        self.workflows[workflow_id] = workflow
        
        if parent_id and parent_id in self.workflows:
            self.workflows[parent_id].child_workflows.append(workflow_id)
            self.logger.debug("Linked workflow %s as child of %s", workflow_id, parent_id)
        
        await self.event_bus.publish(
            "workflow_created",
            {"workflow_id": str(workflow_id), "type": workflow_type.value, "name": name},
            category=EventCategory.SYSTEM
        )
        self.logger.success("Workflow '%s' created successfully.", name)
        return workflow

    async def _create_workflow_steps(
        self,
        workflow_type: WorkflowType,
        context: Dict[str, Any]
    ) -> List[WorkflowStep]:
        """Create appropriate steps for the workflow type"""
        steps = []
        if workflow_type == WorkflowType.NAVIGATION:
            steps.extend([
                WorkflowStep(
                    id=uuid4(),
                    type=WorkflowStepType.WORKSPACE_SCAN,
                    action=self.step_handlers[WorkflowStepType.WORKSPACE_SCAN],
                    description="Scan workspace for components"
                ),
                WorkflowStep(
                    id=uuid4(),
                    type=WorkflowStepType.COMPONENT_ANALYSIS,
                    action=self.step_handlers[WorkflowStepType.COMPONENT_ANALYSIS],
                    description="Analyze selected component"
                ),
                WorkflowStep(
                    id=uuid4(),
                    type=WorkflowStepType.DEPENDENCY_ANALYSIS,
                    action=self.step_handlers[WorkflowStepType.DEPENDENCY_ANALYSIS],
                    description="Analyze component dependencies"
                )
            ])
            if context.get("target_path"):
                steps.append(
                    WorkflowStep(
                        id=uuid4(),
                        type=WorkflowStepType.PATH_TRANSITION,
                        action=self.step_handlers[WorkflowStepType.PATH_TRANSITION],
                        description="Transition to target path"
                    )
                )
        # Additional workflow types can be handled here.
        self.logger.debug("Workflow steps created: %s", steps)
        return steps

    async def execute_workflow(self, workflow_id: UUID) -> Dict[str, Any]:
        """Execute a workflow and return the results"""
        if workflow_id not in self.workflows:
            error_msg = f"Workflow not found: {workflow_id}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
            
        workflow = self.workflows[workflow_id]
        context = self.contexts[workflow_id]
        self.active_workflow = workflow_id
        self.logger.info("Executing workflow %s (%s)", workflow.name, workflow_id)
        
        try:
            for step in workflow.steps:
                workflow.current_step = step.id
                await self._check_step_dependencies(step, workflow)
                total_execution_time = 0.0
                success = False
                while not success:
                    attempt_start = datetime.now()
                    try:
                        self.logger.debug("Executing step %s (%s)", step.id, step.description)
                        step.result = await step.action(context)
                        step.completed = True
                        success = True
                        self.logger.info("Step %s completed successfully.", step.id)
                    except Exception as e:
                        step.error = str(e)
                        step.retries += 1
                        self.logger.warning("Step %s failed on attempt %d: %s", step.id, step.retries, str(e))
                        if step.retries >= step.max_retries:
                            self.logger.error("Step %s exceeded maximum retries.", step.id)
                            raise
                    finally:
                        total_execution_time += (datetime.now() - attempt_start).total_seconds()
                step.execution_time = total_execution_time
                for validation in step.validation_steps:
                    await validation(step.result)
                await self._update_context(context, step)
            workflow.status = "completed"
            workflow.completed_at = datetime.now()
            self.logger.success("Workflow %s completed successfully in %s seconds.", workflow.name,
                             sum(s.execution_time or 0 for s in workflow.steps))
            return {
                "success": True,
                "workflow_id": str(workflow_id),
                "steps_completed": len(workflow.steps),
                "execution_time": sum(s.execution_time or 0 for s in workflow.steps)
            }
        except Exception as e:
            workflow.status = "error"
            self.logger.error("Workflow %s failed: %s", workflow.name, str(e))
            return {
                "success": False,
                "workflow_id": str(workflow_id),
                "error": str(e)
            }
        finally:
            if self.active_workflow == workflow_id:
                self.active_workflow = None

    async def _check_step_dependencies(self, step: WorkflowStep, workflow: Workflow) -> None:
        """Check if the dependencies for a step are met"""
        for dep_id in step.dependencies:
            dep_step = next((s for s in workflow.steps if s.id == dep_id), None)
            if not dep_step or not dep_step.completed:
                error_msg = f"Dependency {dep_id} not met for step {step.id}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

    async def _update_context(self, context: WorkflowContext, step: WorkflowStep) -> None:
        """Update the workflow context based on the step result"""
        if not step.result:
            return
        if step.type == WorkflowStepType.WORKSPACE_SCAN:
            context.components = step.result.get("components", [])
        elif step.type == WorkflowStepType.COMPONENT_ANALYSIS:
            context.metadata["component_info"] = step.result.get("component_info", {})
        elif step.type == WorkflowStepType.DEPENDENCY_ANALYSIS:
            context.dependencies.update(step.result.get("dependencies", {}))
        elif step.type == WorkflowStepType.PATH_TRANSITION:
            context.current_path = step.result.get("new_path")
        self.logger.debug("Workflow context updated after step %s", step.id)

    async def _workflow_worker(self) -> None:
        """Background worker for processing workflows"""
        self.logger.info("Workflow worker started.")
        while self._running:
            try:
                for workflow in list(self.workflows.values()):
                    if workflow.status == "pending":
                        self.logger.debug("Auto-executing pending workflow: %s", workflow.id)
                        await self.execute_workflow(workflow.id)
                await asyncio.sleep(1)
            except Exception as e:
                self.logger.error("Error in workflow worker: %s", str(e))
                await asyncio.sleep(1)

    # Step handler implementations
    async def _handle_workspace_scan(self, context: WorkflowContext) -> Dict[str, Any]:
        self.logger.debug("Handling workspace scan step.")
        # Implementation would use a workspace scanner
        return {"components": []}

    async def _handle_component_analysis(self, context: WorkflowContext) -> Dict[str, Any]:
        self.logger.debug("Handling component analysis step.")
        # Implementation would use a component analyzer
        return {"component_info": {}}

    async def _handle_dependency_analysis(self, context: WorkflowContext) -> Dict[str, Any]:
        self.logger.debug("Handling dependency analysis step.")
        # Implementation would use a dependency analyzer
        return {"dependencies": {}}

    async def _handle_path_transition(self, context: WorkflowContext) -> Dict[str, Any]:
        self.logger.debug("Handling path transition step.")
        # Implementation would handle path changes
        return {"new_path": context.target_path}

    def get_active_workflow(self) -> Optional[UUID]:
        """Get the ID of the currently active workflow"""
        return self.active_workflow

    def get_workflow_status(self, workflow_id: UUID) -> Optional[Dict[str, Any]]:
        """Get detailed status of a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        return {
            "id": str(workflow.id),
            "type": workflow.type.value,
            "status": workflow.status,
            "current_step": str(workflow.current_step) if workflow.current_step else None,
            "steps_total": len(workflow.steps),
            "steps_completed": len([s for s in workflow.steps if s.completed]),
            "created_at": workflow.created_at.isoformat(),
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None
        }

    def get_workflow_chain(self, workflow_id: UUID) -> List[UUID]:
        """Get the full chain of related workflows"""
        chain = []
        workflow = self.workflows.get(workflow_id)
        current = workflow
        while current and current.parent_workflow:
            chain.insert(0, current.parent_workflow)
            current = self.workflows.get(current.parent_workflow)
        if workflow:
            chain.append(workflow.id)
        if workflow:
            chain.extend(workflow.child_workflows)
        self.logger.debug("Workflow chain for %s: %s", workflow_id, chain)
        return chain

    def analyze_workflow_metrics(self, workflow_id: UUID) -> Dict[str, Any]:
        """Analyze execution metrics for a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {}
        completed_steps = [s for s in workflow.steps if s.completed]
        failed_steps = [s for s in workflow.steps if s.error]
        metrics = {
            "total_steps": len(workflow.steps),
            "completed_steps": len(completed_steps),
            "failed_steps": len(failed_steps),
            "total_execution_time": sum(s.execution_time or 0 for s in workflow.steps),
            "average_step_time": (sum(s.execution_time or 0 for s in completed_steps) / len(completed_steps)
                                  if completed_steps else 0),
            "retry_count": sum(s.retries for s in workflow.steps),
            "error_rate": (len(failed_steps) / len(workflow.steps)) if workflow.steps else 0,
            "steps_by_type": self._count_steps_by_type(workflow),
            "execution_timeline": self._generate_timeline(workflow),
            "bottlenecks": self._identify_bottlenecks(workflow)
        }
        if workflow.child_workflows:
            child_metrics = {}
            for child_id in workflow.child_workflows:
                child_metrics[str(child_id)] = self.analyze_workflow_metrics(child_id)
            metrics["child_workflows"] = child_metrics
        self.logger.debug("Workflow metrics for %s: %s", workflow_id, metrics)
        return metrics

    def _count_steps_by_type(self, workflow: Workflow) -> Dict[str, int]:
        type_counts = {}
        for step in workflow.steps:
            type_name = step.type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        return type_counts

    def _generate_timeline(self, workflow: Workflow) -> List[Dict[str, Any]]:
        timeline = []
        for step in workflow.steps:
            if step.completed and step.execution_time is not None:
                timeline.append({
                    "step_id": str(step.id),
                    "type": step.type.value,
                    "execution_time": step.execution_time,
                    "retries": step.retries,
                    "status": "completed" if step.completed else "failed" if step.error else "pending"
                })
        return timeline

    def _identify_bottlenecks(self, workflow: Workflow) -> List[Dict[str, Any]]:
        bottlenecks = []
        avg_time = (sum(s.execution_time or 0 for s in workflow.steps) / len(workflow.steps)
                    if workflow.steps else 0)
        for step in workflow.steps:
            if step.execution_time and step.execution_time > (avg_time * 1.5):
                bottlenecks.append({
                    "step_id": str(step.id),
                    "type": step.type.value,
                    "execution_time": step.execution_time,
                    "avg_time_ratio": (step.execution_time / avg_time) if avg_time else 0,
                    "retries": step.retries
                })
        return sorted(bottlenecks, key=lambda x: x["execution_time"], reverse=True)

    def clear_completed_workflows(self, max_age_hours: int = 24) -> int:
        threshold = datetime.now() - timedelta(hours=max_age_hours)
        removed = 0
        for workflow_id, workflow in list(self.workflows.items()):
            if (workflow.status == "completed" and 
                workflow.completed_at and 
                workflow.completed_at < threshold):
                del self.workflows[workflow_id]
                removed += 1
        self.logger.success("Cleared %d completed workflows older than %d hours.", removed, max_age_hours)
        return removed
