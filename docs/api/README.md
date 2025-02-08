# docs/api/README.md
# API Documentation

## Core Components

### AgentCoordinator
The main coordinator for the semi-autonomous agent system. Handles request processing, workflow management, and system state.

#### Methods
- `process_request(request: Dict[str, Any]) -> Dict[str, Any>`
- `check_status() -> Dict[str, Any]`
- `initialize() -> None`

### StateManager
Manages agent state and context information.

#### Methods
- `update_state(state: AgentState, metadata: Optional[Dict[str, Any]] = None) -> None`
- `get_current_state() -> Dict[str, Any]`
- `record_error(error: str, context: Optional[Dict[str, Any]] = None) -> None`

### WorkflowManager
Handles workflow creation, execution, and monitoring.

#### Methods
- `create_workflow(request: Dict[str, Any]) -> Workflow`
- `execute_workflow(workflow_id: UUID) -> Dict[str, Any]`
- `get_workflow_status(workflow_id: UUID) -> Dict[str, Any]`

[Full API Documentation](./full_api.md)
