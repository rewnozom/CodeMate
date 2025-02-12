import unittest
import asyncio
from cmate.validation.test_manager import TestManager
import os

class TestTestManager(unittest.TestCase):
    def setUp(self):
        self.tm = TestManager("./Workspace")
        self.test_file = "temp/dummy_test.py"
        os.makedirs("temp", exist_ok=True)
        with open(self.test_file, "w") as f:
            f.write("def test_dummy():\n    assert True\n")
    
    def test_add_and_run_test(self):
        async def run_test():
            test_id = await self.tm.add_test_case("dummy_test", "A dummy test case", self.test_file, "unit")
            result = await self.tm.run_test(test_id)
            self.assertTrue(result.success)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
