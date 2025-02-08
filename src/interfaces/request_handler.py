# src/interfaces/request_handler.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import json
from uuid import UUID, uuid4
from ..core.state_manager import StateManager
from ..core.workflow_manager import WorkflowManager
from ..utils.logger import get_logger

@dataclass
class RequestContext:
    """Context for request processing"""
    id: UUID
    request_type: str
    content: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0

@dataclass
class RequestResult:
    """Result of request processing"""
    success: bool
    data: Optional[Any]
    error: Optional[str]
    processing_time: float
    metadata: Dict[str, Any]

class RequestHandler:
    """Handles incoming requests and their processing"""
    
    def __init__(self, state_manager: StateManager, workflow_manager: WorkflowManager):
        self.state_manager = state_manager
        self.workflow_manager = workflow_manager
        self.logger = get_logger(__name__)
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.active_requests: Dict[UUID, RequestContext] = {}
        self._running = False

    async def start(self) -> None:
        """Start request processing"""
        self._running = True
        await self._process_queue()

    async def stop(self) -> None:
        """Stop request processing"""
        self._running = False

    async def handle_request(self, request_data: Dict[str, Any]) -> RequestResult:
        """Handle incoming request"""
        start_time = datetime.now()
        request_id = uuid4()
        
        try:
            # Validate request
            self._validate_request(request_data)
            
            # Create request context
            context = RequestContext(
                id=request_id,
                request_type=request_data.get("type", "unknown"),
                content=request_data,
                timestamp=datetime.now(),
                metadata=request_data.get("metadata", {}),
                priority=request_data.get("priority", 0)
            )
            
            # Add to active requests
            self.active_requests[request_id] = context
            
            # Process request
            result = await self._process_request(context)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return RequestResult(
                success=True,
                data=result,
                error=None,
                processing_time=processing_time,
                metadata={"request_id": str(request_id)}
            )
            
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return RequestResult(
                success=False,
                data=None,
                error=str(e),
                processing_time=processing_time,
                metadata={"request_id": str(request_id)}
            )
        finally:
            self.active_requests.pop(request_id, None)

    async def _process_queue(self) -> None:
        """Process requests from queue"""
        while self._running:
            try:
                request = await self.request_queue.get()
                await self.handle_request(request)
                self.request_queue.task_done()
            except Exception as e:
                self.logger.error(f"Error in queue processing: {str(e)}")
                await asyncio.sleep(1)

    async def _process_request(self, context: RequestContext) -> Any:
        """Process individual request"""
        # Update state
        self.state_manager.update_state("processing", {
            "request_id": str(context.id),
            "request_type": context.request_type
        })
        
        # Create workflow
        workflow = await self.workflow_manager.create_workflow({
            "type": context.request_type,
            "data": context.content,
            "metadata": context.metadata
        })
        
        # Execute workflow
        result = await self.workflow_manager.execute_workflow(workflow.id)
        
        # Update state
        self.state_manager.update_state("idle")
        
        return result

    def _validate_request(self, request_data: Dict[str, Any]) -> None:
        """Validate request data"""
        required_fields = ["type", "data"]
        for field in required_fields:
            if field not in request_data:
                raise ValueError(f"Missing required field: {field}")

