# docs/core/README.md
# Core Components Documentation

## Overview
Core components handle the central logic and coordination of the semi-autonomous agent system.

### Components
- agent_coordinator.py
- state_manager.py
- workflow_manager.py
- event_bus.py
- context_manager.py
- memory_manager.py

## Detailed Documentation

### AgentCoordinator
Main coordinator for the agent system.

#### Key Responsibilities
- Request processing
- Workflow management
- State coordination
- Resource management

#### Usage Example
```python
from core.agent_coordinator import AgentCoordinator

agent = AgentCoordinator()
result = await agent.process_request({
    "type": "analyze",
    "data": {"path": "example.py"}
})
```

### StateManager
Manages system state and context.

#### Key Features
- State transitions
- Context management
- Error tracking
- History maintenance

#### Example
```python
from core.state_manager import StateManager

state_manager = StateManager()
state_manager.update_state(AgentState.ANALYZING, {
    "file": "example.py",
    "action": "syntax_check"
})
```

[More core component details...](./components.md)
