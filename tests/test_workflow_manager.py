import unittest
import asyncio
from uuid import UUID
from cmate.core.workflow_manager import WorkflowManager, WorkflowType

class TestWorkflowManager(unittest.TestCase):
    def setUp(self):
        self.workflow_manager = WorkflowManager()
    
    def test_create_and_execute_workflow(self):
        async def run_test():
            workflow = await self.workflow_manager.create_workflow(
                workflow_type=WorkflowType.NAVIGATION,
                name="Test Navigation Workflow",
                description="Testing workflow creation",
                context={"target_path": "./Workspace/dummy.txt"}
            )
            self.assertIsInstance(workflow.id, UUID)
            result = await self.workflow_manager.execute_workflow(workflow.id)
            self.assertIn("success", result)
            self.assertTrue(result.get("success"))
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
