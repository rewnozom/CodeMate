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