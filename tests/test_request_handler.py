import unittest
import asyncio
from cmate.interfaces.request_handler import RequestHandler
from cmate.core.state_manager import StateManager, AgentState
from cmate.core.workflow_manager import WorkflowManager

class DummyWorkflowManager(WorkflowManager):
    async def create_workflow(self, workflow_type, name, description, context=None, parent_id=None):
        from uuid import uuid4
        class DummyWorkflow:
            def __init__(self):
                self.id = uuid4()
        return DummyWorkflow()
    async def execute_workflow(self, workflow_id):
        return {"success": True, "workflow_id": str(workflow_id)}

class TestRequestHandler(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()
        self.workflow_manager = DummyWorkflowManager()
        self.request_handler = RequestHandler(self.state_manager, self.workflow_manager)
    
    def test_handle_request(self):
        async def run_test():
            request = {"type": "analyze", "data": {"path": "./Workspace"}}
            result = await self.request_handler.handle_request(request)
            self.assertTrue(result.success)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
