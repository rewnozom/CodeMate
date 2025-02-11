# tests/unit/test_state_manager.py
import pytest
from cmate.core.state_manager import StateManager, AgentState

def test_state_manager_initialization(state_manager):
    """Test state manager initialization"""
    assert state_manager.current_state == AgentState.IDLE
    assert state_manager.metadata is not None

def test_update_state(state_manager):
    """Test updating state"""
    state_manager.update_state(AgentState.ANALYZING, {"test": "data"})
    assert state_manager.current_state == AgentState.ANALYZING
    assert len(state_manager.state_history) == 1

def test_record_error(state_manager):
    """Test error recording"""
    state_manager.record_error("Test error")
    assert state_manager.metadata.error_count == 1
    assert len(state_manager.state_history) > 0