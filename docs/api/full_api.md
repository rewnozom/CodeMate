# docs/api/full_api.md
# Complete API Reference

## Core Module

### agent_coordinator.py
```python
class AgentCoordinator:
    """Main coordinator for the semi-autonomous agent"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize agent coordinator"""
        
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process user request"""
        
    async def check_status(self) -> Dict[str, Any]:
        """Get current agent status"""
```

[Additional API details...](./modules/)
