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