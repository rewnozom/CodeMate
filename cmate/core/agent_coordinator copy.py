# src/core/agent_coordinator.py
import asyncio
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Callable, List, Optional

# Import required core modules
from ..core.state_manager import StateManager
from ..core.workflow_manager import WorkflowManager

@dataclass
class AgentConfig:
    """Configuration for the agent coordinator."""
    workspace_path: str = "./Workspace"
    max_files_per_scan: int = 10
    context_window_size: int = 60000
    auto_test: bool = True
    debug_mode: bool = False
    # Add any additional configuration fields as needed.

class AgentCoordinator:
    """
    Coordinates agent activities by processing requests, delegating workflows,
    updating state, and publishing events.
    """
    def __init__(
        self,
        config: AgentConfig,
        state_manager: StateManager,
        workflow_manager: WorkflowManager
    ):
        self.config = config
        self.state_manager = state_manager
        self.workflow_manager = workflow_manager
        self.logger = logging.getLogger(__name__)
        self.start_time = datetime.now()
        # Audit trail for requests (list of dict records)
        self.audit_log: List[Dict[str, Any]] = []
        # Subscribers for agent events
        self.event_subscribers: List[Callable[[Dict[str, Any]], None]] = []

    def subscribe_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Allow external components to subscribe to agent events."""
        self.event_subscribers.append(callback)

    def _publish_event(self, event: Dict[str, Any]) -> None:
        """Publish an event to all subscribers."""
        for callback in self.event_subscribers:
            try:
                callback(event)
            except Exception as e:
                self.logger.error(f"Error in event subscriber callback: {str(e)}")

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming request by creating and executing an appropriate workflow.
        The request must contain at least a 'type' and 'data' field.
        """
        request_id = str(uuid.uuid4())
        self.audit_log.append({
            "request_id": request_id,
            "request": request,
            "timestamp": datetime.now().isoformat()
        })
        self.logger.info(f"Processing request {request_id}: {request}")

        try:
            request_type = request.get("type")
            data = request.get("data", {})

            # Basic request validation
            if not request_type:
                raise ValueError("Request must contain a 'type' field.")

            # Update state to 'processing'
            self.state_manager.update_state("processing", {"request_id": request_id, "request_type": request_type})

            # Publish event that request processing is starting.
            self._publish_event({
                "event": "request_started",
                "request_id": request_id,
                "request_type": request_type,
                "timestamp": datetime.now().isoformat()
            })

            # Create workflow for known request types
            if request_type in ["analyze", "execute", "process"]:
                workflow = await self.workflow_manager.create_workflow({
                    "type": request_type,
                    "data": data,
                    "metadata": request.get("metadata", {"request_id": request_id})
                })
                result = await self.workflow_manager.execute_workflow(workflow.id)
            else:
                result = {"message": f"Unknown request type: {request_type}"}

            # Update state to 'idle' after processing
            self.state_manager.update_state("idle", {"last_request": request_type})
            self._publish_event({
                "event": "request_completed",
                "request_id": request_id,
                "request_type": request_type,
                "timestamp": datetime.now().isoformat(),
                "result": result
            })
            return {"success": True, "result": result, "request_id": request_id}
        except Exception as e:
            self.logger.error(f"Error processing request {request_id}: {str(e)}")
            self.state_manager.update_state("error", {"request_id": request_id, "error": str(e)})
            self._publish_event({
                "event": "request_failed",
                "request_id": request_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return {"success": False, "error": str(e), "request_id": request_id}

    async def check_status(self) -> Dict[str, Any]:
        """
        Return the current status of the agent, including its state, any active workflow,
        and basic uptime metrics.
        """
        state = self.state_manager.get_state()
        active_workflow = self.workflow_manager.get_active_workflow()
        uptime = (datetime.now() - self.start_time).total_seconds()
        return {
            "state": state,
            "active_workflow": active_workflow,
            "uptime": uptime,
            "audit_log": self.audit_log[-10:],  # return last 10 audit entries
            "metrics": {}  # Extend with additional metrics as needed.
        }

    async def shutdown(self) -> None:
        """
        Gracefully shut down the agent.
        Cancels any running workflows, persists state, and publishes a shutdown event.
        """
        self.logger.info("Shutting down agent...")
        self.state_manager.update_state("shutting_down", {"timestamp": datetime.now().isoformat()})
        # Stop workflow processing
        await self.workflow_manager.shutdown()
        self.state_manager.update_state("shutdown", {"timestamp": datetime.now().isoformat()})
        self._publish_event({
            "event": "agent_shutdown",
            "timestamp": datetime.now().isoformat()
        })
