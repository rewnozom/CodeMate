import unittest
import asyncio
from cmate.file_services.file_watcher import FileWatcher

class TestFileWatcher(unittest.TestCase):
    def setUp(self):
        self.workspace = "./Workspace"
        self.file_watcher = FileWatcher(self.workspace)
    
    def test_start_and_stop_watching(self):
        async def run_test():
            await self.file_watcher.start_watching()
            self.assertTrue(self.file_watcher._is_running)
            await asyncio.sleep(0.1)
            await self.file_watcher.stop_watching()
            self.assertFalse(self.file_watcher._is_running)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
