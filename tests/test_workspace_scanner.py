import unittest
import asyncio
from cmate.file_services.workspace_scanner import WorkspaceScanner, ScanResult

class TestWorkspaceScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = WorkspaceScanner("./Workspace")
    
    def test_scan_workspace(self):
        async def run_test():
            result = await self.scanner.scan_workspace(max_depth=2)
            self.assertIsInstance(result, ScanResult)
            self.assertIsInstance(result.files, list)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
