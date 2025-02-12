import unittest
import asyncio
from cmate.validation.backend_validator import BackendValidator

class TestBackendValidator(unittest.TestCase):
    def setUp(self):
        self.validator = BackendValidator()
    
    def test_validate_python(self):
        code = "def foo(x):\n    return x * 2\n"
        async def run_test():
            result = await self.validator._validate_python(code, "dummy.py")
            self.assertTrue(result.valid)
            self.assertGreaterEqual(len(result.functions), 1)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
