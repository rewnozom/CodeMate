# tests/unit/test_workflow_manager.py
import pytest
from datetime import datetime
from src.core.workflow_manager import WorkflowManager, WorkflowStep, WorkflowStepType

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