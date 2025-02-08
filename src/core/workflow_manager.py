# src/core/workflow_manager.py
import asyncio
import json
import logging
import os
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

WORKFLOWS_FILE = Path("temp/workflows.json")

@dataclass
class Workflow:
    """Represents a workflow with its metadata and execution status."""
    id: str
    type: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"  # possible values: pending, in_progress, completed, failed, cancelled
    result: Optional[Any] = None

class WorkflowManager:
    """
    Manages workflows created by the agent.
    
    Uses an internal asyncio.Queue to schedule workflows sequentially,
    supports cancellation, and logs detailed metrics.
    """
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.active_workflow_id: Optional[str] = None
        self.workflow_queue: asyncio.Queue = asyncio.Queue()
        self.workflow_tasks: Dict[str, asyncio.Task] = {}
        self.logger = logging.getLogger(__name__)
        self._worker_task: Optional[asyncio.Task] = None
        # Optionally load persisted workflows
        self._load_workflows()

    async def start_worker(self) -> None:
        """Start the workflow processing worker."""
        if not self._worker_task:
            self._worker_task = asyncio.create_task(self._workflow_worker())
            self.logger.info("Workflow worker started.")

    async def shutdown(self) -> None:
        """Shutdown workflow processing gracefully."""
        self.logger.info("Shutting down workflow manager...")
        # Cancel the worker task if running
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                self.logger.info("Workflow worker cancelled.")
            self._worker_task = None
        # Cancel any active workflow tasks
        for wf_id, task in self.workflow_tasks.items():
            task.cancel()
        self.workflow_tasks.clear()
        # Persist current workflows
        self._persist_workflows()

    async def create_workflow(self, workflow_data: Dict[str, Any]) -> Workflow:
        """
        Create a new workflow using the provided data.
        workflow_data should contain at least 'type' and 'data' keys.
        """
        workflow_id = str(uuid.uuid4())
        workflow = Workflow(
            id=workflow_id,
            type=workflow_data.get("type", "generic"),
            data=workflow_data.get("data", {}),
            metadata=workflow_data.get("metadata", {})
        )
        self.workflows[workflow_id] = workflow
        await self.workflow_queue.put(workflow)
        self.logger.info(f"Workflow {workflow_id} created and queued.")
        self._persist_workflows()
        # Ensure the worker is running.
        await self.start_worker()
        return workflow

    async def execute_workflow(self, workflow_id: str) -> Any:
        """
        Execute the workflow with the given ID.
        If the workflow is already queued, wait until its execution completes.
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")
        # Wait until the workflow is completed.
        while self.workflows[workflow_id].status in ["pending", "in_progress"]:
            await asyncio.sleep(0.5)
        return self.workflows[workflow_id].result

    async def _workflow_worker(self) -> None:
        """Worker loop that processes workflows sequentially from the queue."""
        while True:
            try:
                workflow: Workflow = await self.workflow_queue.get()
                self.active_workflow_id = workflow.id
                workflow.status = "in_progress"
                self.logger.info(f"Executing workflow {workflow.id} of type '{workflow.type}'")
                # Create a task for execution so that we can support cancellation
                task = asyncio.create_task(self._execute_workflow_task(workflow))
                self.workflow_tasks[workflow.id] = task
                await task
                self.active_workflow_id = None
                self.workflow_queue.task_done()
                self._persist_workflows()
            except asyncio.CancelledError:
                self.logger.info("Workflow worker received cancellation.")
                break
            except Exception as e:
                self.logger.error(f"Error in workflow worker: {str(e)}")
                await asyncio.sleep(1)

    async def _execute_workflow_task(self, workflow: Workflow) -> None:
        """Simulate workflow execution; replace with real logic as needed."""
        start_time = datetime.now()
        try:
            # Simulate workflow steps (here, simply a delay)
            await asyncio.sleep(2)
            workflow.result = {
                "message": f"Workflow {workflow.id} executed successfully",
                "data": workflow.data
            }
            workflow.status = "completed"
            self.logger.info(f"Workflow {workflow.id} completed in {(datetime.now() - start_time).total_seconds()} seconds.")
        except asyncio.CancelledError:
            workflow.status = "cancelled"
            self.logger.info(f"Workflow {workflow.id} cancelled.")
            raise
        except Exception as e:
            workflow.result = {"error": str(e)}
            workflow.status = "failed"
            self.logger.error(f"Workflow {workflow.id} failed: {str(e)}")

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Return status and details of the specified workflow."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")
        wf = self.workflows[workflow_id]
        return {
            "id": wf.id,
            "type": wf.type,
            "status": wf.status,
            "created_at": wf.created_at.isoformat(),
            "metadata": wf.metadata,
            "result": wf.result
        }

    def get_active_workflow(self) -> Optional[str]:
        """Return the ID of the currently active workflow, if any."""
        return self.active_workflow_id

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Attempt to cancel a workflow execution."""
        task = self.workflow_tasks.get(workflow_id)
        if task and not task.done():
            task.cancel()
            self.workflows[workflow_id].status = "cancelled"
            self.logger.info(f"Workflow {workflow_id} cancellation requested.")
            return True
        return False

    def _persist_workflows(self) -> None:
        """Persist workflow metadata to a JSON file."""
        try:
            if not WORKFLOWS_FILE.parent.exists():
                WORKFLOWS_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {wf_id: {
                        "id": wf.id,
                        "type": wf.type,
                        "data": wf.data,
                        "metadata": wf.metadata,
                        "created_at": wf.created_at.isoformat(),
                        "status": wf.status,
                        "result": wf.result
                    } for wf_id, wf in self.workflows.items()}
            with open(WORKFLOWS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error persisting workflows: {str(e)}")

    def _load_workflows(self) -> None:
        """Load persisted workflows from a JSON file."""
        if WORKFLOWS_FILE.exists():
            try:
                with open(WORKFLOWS_FILE, 'r') as f:
                    data = json.load(f)
                for wf_id, wf_data in data.items():
                    wf = Workflow(
                        id=wf_data["id"],
                        type=wf_data["type"],
                        data=wf_data["data"],
                        metadata=wf_data["metadata"],
                        created_at=datetime.fromisoformat(wf_data["created_at"]),
                        status=wf_data["status"],
                        result=wf_data.get("result")
                    )
                    self.workflows[wf_id] = wf
            except Exception as e:
                self.logger.error(f"Error loading workflows: {str(e)}")
