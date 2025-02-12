import unittest
import asyncio
from cmate.core.navigation_system import NavigationDecisionSystem, NavigationContext, NavigationResult
from cmate.core.state_manager import AgentState

class TestNavigationSystem(unittest.TestCase):
    def setUp(self):
        self.workspace_path = "./Workspace"
        self.nav_system = NavigationDecisionSystem(self.workspace_path)
    
    def test_prepare_and_execute_navigation(self):
        async def run_test():
            request = "Analyze file structure"
            workspace_data = {"dummy": "data"}
            context = await self.nav_system.prepare_decision_context(request, workspace_data, AgentState.IDLE)
            self.assertIsInstance(context, NavigationContext)
            result = await self.nav_system.execute_navigation("ANALYZE_FILE", context)
            self.assertIsInstance(result, NavigationResult)
            self.assertTrue(result.success)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
