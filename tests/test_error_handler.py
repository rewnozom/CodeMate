import unittest
from cmate.utils.error_handler import ErrorHandler, ErrorSeverity

class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ErrorHandler()
    
    def test_handle_value_error(self):
        try:
            raise ValueError("Test value error")
        except Exception as e:
            report = self.handler.handle_error(e, ErrorSeverity.ERROR, {"info": "test"})
            self.assertEqual(report.error_type, "ValueError")
            self.assertIn("Test value error", report.message)
            self.assertGreater(len(report.recovery_steps), 0)

if __name__ == '__main__':
    unittest.main()
