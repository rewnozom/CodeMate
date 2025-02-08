# tests/conftest.py
import pytest
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.core.agent_coordinator import AgentCoordinator, AgentConfig
from src.core.state_manager import StateManager
from src.core.workflow_manager import WorkflowManager

@pytest.fixture
def workspace_path(tmp_path):
    """Create temporary workspace"""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace

@pytest.fixture
def agent_config(workspace_path):
    """Create test agent configuration"""
    return AgentConfig(
        workspace_path=str(workspace_path),
        max_files_per_scan=10,
        context_window_size=1000,
        auto_test=True,
        debug_mode=True
    )

@pytest.fixture
def state_manager():
    """Create test state manager"""
    return StateManager()

@pytest.fixture
def workflow_manager():
    """Create test workflow manager"""
    return WorkflowManager()

@pytest.fixture
def agent(agent_config, state_manager, workflow_manager):
    """Create test agent"""
    return AgentCoordinator(
        config=agent_config,
        state_manager=state_manager,
        workflow_manager=workflow_manager
    )