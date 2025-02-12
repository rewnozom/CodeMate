import unittest
import asyncio
from cmate.core.agent_coordinator import AgentCoordinator, AgentConfig
from cmate.core.state_manager import StateManager
from cmate.core.workflow_manager import WorkflowManager

class TestAgentEndToEnd(unittest.TestCase):
    def setUp(self):
        config = AgentConfig(
            workspace_path="./Workspace",
            max_files_per_scan=5,
            context_window_size=60000,
            auto_test=True,
            debug_mode=True
        )
        state_manager = StateManager()
        workflow_manager = WorkflowManager()
        self.agent = AgentCoordinator(config, state_manager, workflow_manager)
    
    def test_process_request_and_status(self):
        async def run_test():
            request = {
                "type": "analyze",
                "data": {"path": "./Workspace"}
            }
            result = await self.agent.process_request(request)
            self.assertIn("success", result)
            self.assertTrue(result["success"])
            status = await self.agent.check_status()
            self.assertIn("state", status)
            await self.agent.refresh_llm_context()
            code = await self.agent.generate_code("Generate a simple hello world function in Python")
            self.assertIsInstance(code, str)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
