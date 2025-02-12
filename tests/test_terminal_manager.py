import unittest
import asyncio
from cmate.interfaces.terminal_manager import TerminalManager

class TestTerminalManager(unittest.TestCase):
    def setUp(self):
        self.tm = TerminalManager("./Workspace")
    
    def test_execute_command(self):
        async def run_test():
            result = await self.tm.execute_command("echo Hello", capture_output=True)
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Hello", result.stdout)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
