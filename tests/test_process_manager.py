import unittest
import asyncio
from cmate.task_management.process_manager import ProcessManager

class TestProcessManager(unittest.TestCase):
    def setUp(self):
        self.pm = ProcessManager("./Workspace")
    
    def test_start_and_stop_process(self):
        async def run_test():
            # Use a string command; on Windows "echo Hello" runs via the shell.
            process_id = await self.pm.start_process("echo_test", "echo Hello")
            self.assertIsNotNone(process_id)
            await asyncio.sleep(1)
            active = self.pm.get_active_processes()
            self.assertIsInstance(active, list)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
