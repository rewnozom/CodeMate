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