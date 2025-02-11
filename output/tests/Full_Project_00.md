# Project Details

# Table of Contents
- [..\tests\conftest.py](#-tests-conftestpy)
- [..\tests\__init__.py](#-tests-__init__py)
- [..\tests\fixtures\__init__.py](#-tests-fixtures-__init__py)
- [..\tests\fixtures\sample_workspace\__init__.py](#-tests-fixtures-sample_workspace-__init__py)
- [..\tests\fixtures\sample_workspace\test_project\main.py](#-tests-fixtures-sample_workspace-test_project-mainpy)
- [..\tests\fixtures\sample_workspace\test_project\__init__.py](#-tests-fixtures-sample_workspace-test_project-__init__py)
- [..\tests\integration\test_end_to_end.py](#-tests-integration-test_end_to_endpy)
- [..\tests\integration\test_workflows.py](#-tests-integration-test_workflowspy)
- [..\tests\integration\__init__.py](#-tests-integration-__init__py)
- [..\tests\unit\test_agent_coordinator.py](#-tests-unit-test_agent_coordinatorpy)
- [..\tests\unit\test_file_analyzer.py](#-tests-unit-test_file_analyzerpy)
- [..\tests\unit\test_state_manager.py](#-tests-unit-test_state_managerpy)
- [..\tests\unit\test_test_manager.py](#-tests-unit-test_test_managerpy)
- [..\tests\unit\test_workflow_manager.py](#-tests-unit-test_workflow_managerpy)
- [..\tests\unit\__init__.py](#-tests-unit-__init__py)


# ..\..\tests\conftest.py
## File: ..\..\tests\conftest.py

```py
# ..\..\tests\conftest.py
# tests/conftest.py
import pytest
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cmate.core.agent_coordinator import AgentCoordinator, AgentConfig
from cmate.core.state_manager import StateManager
from cmate.core.workflow_manager import WorkflowManager

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
```

---

# ..\..\tests\__init__.py
## File: ..\..\tests\__init__.py

```py
# ..\..\tests\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\tests\fixtures\__init__.py
## File: ..\..\tests\fixtures\__init__.py

```py
# ..\..\tests\fixtures\__init__.py
# tests/fixtures/__init__.py
```

---

# ..\..\tests\fixtures\sample_workspace\__init__.py
## File: ..\..\tests\fixtures\sample_workspace\__init__.py

```py
# ..\..\tests\fixtures\sample_workspace\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\tests\fixtures\sample_workspace\test_project\main.py
## File: ..\..\tests\fixtures\sample_workspace\test_project\main.py

```py
# ..\..\tests\fixtures\sample_workspace\test_project\main.py
# tests/fixtures/sample_workspace/test_project/main.py
def example_function():
    """Example function for testing"""
    return True

class ExampleClass:
    """Example class for testing"""
    def method(self):
        return None

# tests/fixtures/mock_data/test_requests.json
{
    "analyze": {
        "type": "analyze",
        "data": {
            "path": "test.py"
        }
    },
    "modify": {
        "type": "modify",
        "data": {
            "path": "test.py",
            "changes": "Rename function"
        }
    },
    "test": {
        "type": "test",
        "data": {
            "path": "test.py"
        }
    }
}
```

---

# ..\..\tests\fixtures\sample_workspace\test_project\__init__.py
## File: ..\..\tests\fixtures\sample_workspace\test_project\__init__.py

```py
# ..\..\tests\fixtures\sample_workspace\test_project\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\tests\integration\test_end_to_end.py
## File: ..\..\tests\integration\test_end_to_end.py

```py
# ..\..\tests\integration\test_end_to_end.py
# tests/integration/test_end_to_end.py
import pytest
from pathlib import Path

async def test_full_analysis_cycle(agent, workspace_path):
    """Test full analysis cycle"""
    # Setup test environment
    test_file = workspace_path / "main.py"
    test_file.write_text("""
class TestClass:
    def __init__(self):
        self.value = 0
        
    def increment(self):
        self.value += 1
        return self.value
    """)
    
    # 1. Analyze file
    analysis_request = {
        "type": "analyze",
        "data": {"path": str(test_file)}
    }
    result = await agent.process_request(analysis_request)
    assert result["success"] is True
    
    # 2. Generate tests
    test_request = {
        "type": "generate_tests",
        "data": {
            "path": str(test_file),
            "class_name": "TestClass"
        }
    }
    result = await agent.process_request(test_request)
    assert result["success"] is True
    
    # 3. Run tests
    test_file = workspace_path / "test_main.py"
    assert test_file.exists()
    
    test_run_request = {
        "type": "run_tests",
        "data": {"path": str(test_file)}
    }
    result = await agent.process_request(test_run_request)
    assert result["success"] is True
```

---

# ..\..\tests\integration\test_workflows.py
## File: ..\..\tests\integration\test_workflows.py

```py
# ..\..\tests\integration\test_workflows.py
# tests/integration/test_workflows.py
import pytest
from pathlib import Path

async def test_complete_workflow(agent, workspace_path):
    """Test complete workflow execution"""
    # Create test file
    test_file = workspace_path / "test.py"
    test_file.write_text("""
def add(a, b):
    return a + b
    """)
    
    # Process request
    request = {
        "type": "analyze",
        "data": {
            "path": str(test_file)
        }
    }
    
    result = await agent.process_request(request)
    assert result["success"] is True
    
    # Check results
    assert "analysis" in result["result"]
    assert len(result["result"]["analysis"].functions) == 1

async def test_file_modification_workflow(agent, workspace_path):
    """Test file modification workflow"""
    # Create test file
    test_file = workspace_path / "modify.py"
    test_file.write_text("""
def old_function():
    pass
    """)
    
    # Process modification request
    request = {
        "type": "modify",
        "data": {
            "path": str(test_file),
            "changes": "Rename function to new_function"
        }
    }
    
    result = await agent.process_request(request)
    assert result["success"] is True
    
    # Verify changes
    content = test_file.read_text()
    assert "new_function" in content
    assert "old_function" not in content
```

---

# ..\..\tests\integration\__init__.py
## File: ..\..\tests\integration\__init__.py

```py
# ..\..\tests\integration\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\tests\unit\test_agent_coordinator.py
## File: ..\..\tests\unit\test_agent_coordinator.py

```py
# ..\..\tests\unit\test_agent_coordinator.py

```

---

# ..\..\tests\unit\test_file_analyzer.py
## File: ..\..\tests\unit\test_file_analyzer.py

```py
# ..\..\tests\unit\test_file_analyzer.py
# tests/unit/test_file_analyzer.py
import pytest
from pathlib import Path
from cmate.file_services.file_analyzer import FileAnalyzer

@pytest.fixture
def test_file(workspace_path):
    """Create test Python file"""
    file_path = workspace_path / "test.py"
    file_path.write_text("""
def test_function():
    '''Test docstring'''
    return True

class TestClass:
    def method(self):
        return None
    """)
    return file_path

async def test_analyze_python_file(test_file):
    """Test Python file analysis"""
    analyzer = FileAnalyzer()
    result = await analyzer.analyze_file(test_file)
    
    assert result is not None
    assert result.metadata.path == test_file
    assert len(result.code_analysis.functions) == 1
    assert len(result.code_analysis.classes) == 1
```

---

# ..\..\tests\unit\test_state_manager.py
## File: ..\..\tests\unit\test_state_manager.py

```py
# ..\..\tests\unit\test_state_manager.py
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
```

---

# ..\..\tests\unit\test_test_manager.py
## File: ..\..\tests\unit\test_test_manager.py

```py
# ..\..\tests\unit\test_test_manager.py
# tests/unit/test_test_manager.py
import pytest
from cmate.validation.test_manager import TestManager

async def test_test_creation(workspace_path):
    """Test creating test case"""
    manager = TestManager(str(workspace_path))
    test_id = await manager.add_test_case(
        name="Test Case",
        description="Test description",
        test_file=workspace_path / "test_case.py",
        test_type="unit"
    )
    
    assert test_id is not None
    test_case = manager.get_test_case(test_id)
    assert test_case.name == "Test Case"
```

---

# ..\..\tests\unit\test_workflow_manager.py
## File: ..\..\tests\unit\test_workflow_manager.py

```py
# ..\..\tests\unit\test_workflow_manager.py
# tests/unit/test_workflow_manager.py
import pytest
from datetime import datetime
from cmate.core.workflow_manager import WorkflowManager, WorkflowStep, WorkflowStepType

async def test_workflow_creation(workflow_manager):
    """Test workflow creation"""
    workflow = await workflow_manager.create_workflow({
        "name": "Test Workflow",
        "description": "Test workflow description"
    })
    
    assert workflow is not None
    assert workflow.name == "Test Workflow"
    assert len(workflow.steps) == 0

async def test_workflow_execution(workflow_manager):
    """Test workflow execution"""
    workflow = await workflow_manager.create_workflow({
        "name": "Test Workflow",
        "description": "Test workflow description"
    })
    
    result = await workflow_manager.execute_workflow(workflow.id)
    assert result["success"] is True
    assert result["workflow_id"] == str(workflow.id)
```

---

# ..\..\tests\unit\__init__.py
## File: ..\..\tests\unit\__init__.py

```py
# ..\..\tests\unit\__init__.py
# Auto-generated __init__.py file

```

---

