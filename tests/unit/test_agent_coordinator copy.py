# tests/unit/test_agent_coordinator.py
import pytest
from datetime import datetime
from cmate.core.agent_coordinator import AgentCoordinator, AgentConfig

async def test_agent_initialization(agent):
    """Test agent initialization"""
    assert agent is not None
    assert isinstance(agent.config, AgentConfig)
    assert agent.state_manager is not None
    assert agent.workflow_manager is not None

async def test_process_request(agent):
    """Test processing a simple request"""
    request = {
        "type": "analyze",
        "data": {"path": "test.py"}
    }
    
    result = await agent.process_request(request)
    assert result["success"] is True
    assert "result" in result

async def test_check_status(agent):
    """Test checking agent status"""
    status = await agent.check_status()
    assert "state" in status
    assert "metrics" in status