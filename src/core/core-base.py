
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class AgentState(Enum):
    """Agent states"""
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    TESTING = "testing"
    ERROR = "error"
    WAITING_USER = "waiting_user"
    CONTEXT_SWITCHING = "context_switching"

@dataclass
class ContextWindow:
    """Manages context window content and tokens"""
    content: List[Dict[str, Any]] = field(default_factory=list)
    total_tokens: int = 0
    max_tokens: int = 60000

    def add_content(self, content: Dict[str, Any], token_count: int) -> bool:
        if self.total_tokens + token_count > self.max_tokens:
            self._trim_context(token_count)
        self.content.append({
            "data": content,
            "tokens": token_count,
            "timestamp": datetime.now().isoformat()
        })
        self.total_tokens += token_count
        return True

    def _trim_context(self, needed_tokens: int) -> None:
        while self.content and self.total_tokens + needed_tokens > self.max_tokens:
            removed = self.content.pop(0)
            self.total_tokens -= removed["tokens"]

@dataclass
class StateMetadata:
    """Metadata for state tracking"""
    last_user_request: Optional[str] = None
    current_task: Optional[str] = None
    error_count: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

class StateManager:
    """Manages agent state and context"""
    
    def __init__(self):
        self.current_state: AgentState = AgentState.IDLE
        self.metadata: StateMetadata = StateMetadata()
        self.context_window: ContextWindow = ContextWindow()
        self.state_history: List[Dict[str, Any]] = []
        self.active_files: List[str] = []
        self.temporary_memory: Dict[str, Any] = {}
        
    def update_state(self, new_state: AgentState, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update agent state with new information"""
        self.current_state = new_state
        self.metadata.last_updated = datetime.now()
        
        if metadata:
            if "user_request" in metadata:
                self.metadata.last_user_request = metadata["user_request"]
            if "current_task" in metadata:
                self.metadata.current_task = metadata["current_task"]
        
        self._record_state_change(new_state, metadata)

    def add_to_context(self, content: Dict[str, Any], token_count: int) -> bool:
        """Add content to context window"""
        return self.context_window.add_content(content, token_count)

    def update_active_files(self, files: List[str]) -> None:
        """Update list of active files being processed"""
        self.active_files = files
        self._record_state_change(self.current_state, {"active_files": files})

    def record_error(self, error: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Record error information"""
        self.metadata.error_count += 1
        error_data = {
            "error": error,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "state": self.current_state.value
        }
        self._record_state_change(AgentState.ERROR, error_data)

    def get_current_context(self) -> List[Dict[str, Any]]:
        """Get current context window content"""
        return [item["data"] for item in self.context_window.content]

    def _record_state_change(self, state: AgentState, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record state change in history"""
        self.state_history.append({
            "state": state.value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "error_count": self.metadata.error_count
        })


from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
from uuid import UUID, uuid4

class WorkflowStepType(Enum):
    """Types of workflow steps"""
    FILE_ANALYSIS = "file_analysis"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    VALIDATION = "validation"
    USER_INTERACTION = "user_interaction"

@dataclass
class WorkflowStep:
    """Individual workflow step"""
    id: UUID
    type: WorkflowStepType
    action: Callable
    description: str
    required: bool = True
    dependencies: List[UUID] = field(default_factory=list)
    completed: bool = False
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3

@dataclass
class Workflow:
    """Complete workflow definition"""
    id: UUID
    name: str
    description: str
    steps: List[WorkflowStep]
    current_step: Optional[UUID] = None
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowManager:
    """Manages workflow creation and execution"""
    
    def __init__(self):
        self.workflows: Dict[UUID, Workflow] = {}
        self.active_workflow: Optional[UUID] = None
        self.step_handlers: Dict[WorkflowStepType, Callable] = {}
        self._initialize_handlers()
        
    def _initialize_handlers(self) -> None:
        """Initialize default step handlers"""
        self.step_handlers.update({
            WorkflowStepType.FILE_ANALYSIS: self._handle_file_analysis,
            WorkflowStepType.PLANNING: self._handle_planning,
            WorkflowStepType.IMPLEMENTATION: self._handle_implementation,
            WorkflowStepType.TESTING: self._handle_testing,
            WorkflowStepType.VALIDATION: self._handle_validation,
            WorkflowStepType.USER_INTERACTION: self._handle_user_interaction
        })

    async def create_workflow(self, request: Dict[str, Any]) -> Workflow:
        """Create new workflow from request"""
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
        return workflow

    async def execute_workflow(self, workflow_id: UUID) -> Dict[str, Any]:
        """Execute workflow steps"""
        workflow = self.workflows[workflow_id]
        self.active_workflow = workflow_id
        
        try:
            for step in workflow.steps:
                if step.dependencies:
                    await self._check_dependencies(step, workflow)
                
                workflow.current_step = step.id
                handler = self.step_handlers.get(step.type)
                if handler:
                    step.result = await handler(step, workflow)
                else:
                    step.result = await step.action()
                
                step.completed = True
                
            workflow.status = "completed"
            workflow.completed_at = datetime.now()
            return {"success": True, "workflow_id": workflow_id}
            
        except Exception as e:
            workflow.status = "error"
            return {"success": False, "error": str(e), "workflow_id": workflow_id}

    async def _check_dependencies(self, step: WorkflowStep, workflow: Workflow) -> None:
        """Check if step dependencies are met"""
        for dep_id in step.dependencies:
            dep_step = next((s for s in workflow.steps if s.id == dep_id), None)
            if not dep_step or not dep_step.completed:
                raise Exception(f"Dependency {dep_id} not met for step {step.id}")

    async def _handle_file_analysis(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle file analysis steps"""
        # Implementation specific to file analysis
        pass

    async def _handle_planning(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle planning steps"""
        # Implementation specific to planning
        pass

    async def _handle_implementation(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle implementation steps"""
        # Implementation specific to implementation
        pass

    async def _handle_testing(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle testing steps"""
        # Implementation specific to testing
        pass

    async def _handle_validation(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle validation steps"""
        # Implementation specific to validation
        pass

    async def _handle_user_interaction(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle user interaction steps"""
        # Implementation specific to user interaction
        pass

    def _create_steps_from_request(self, request: Dict[str, Any]) -> List[WorkflowStep]:
        """Create workflow steps from request"""
        steps = []
        if "analyze_files" in request:
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.FILE_ANALYSIS,
                action=self._handle_file_analysis,
                description="Analyze workspace files"
            ))
        # Add more step creation logic based on request
        return steps

