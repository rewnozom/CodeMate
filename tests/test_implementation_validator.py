import unittest
import asyncio
from cmate.validation.implementation_validator import ImplementationValidator

class TestImplementationValidator(unittest.TestCase):
    def setUp(self):
        self.validator = ImplementationValidator()
    
    def test_validate_python_code(self):
        code = "def add(a, b):\n    return a + b\n"
        async def run_test():
            result = await self.validator.validate_implementation(code, "python", {"required_functions": ["add"]})
            self.assertTrue(result.valid)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
