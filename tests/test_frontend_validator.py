import unittest
import asyncio
from cmate.validation.frontend_validator import FrontendValidator

class TestFrontendValidator(unittest.TestCase):
    def setUp(self):
        self.validator = FrontendValidator()
    
    def test_validate_pyside6(self):
        code = """
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
"""
        async def run_test():
            result = await self.validator._validate_pyside6(code, "dummy.py")
            self.assertTrue(result.valid)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
