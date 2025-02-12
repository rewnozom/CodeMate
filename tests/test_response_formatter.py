import unittest
from cmate.interfaces.response_formatter import ResponseFormatter, FormattingConfig, ResponseFormat

class TestResponseFormatter(unittest.TestCase):
    def setUp(self):
        config = FormattingConfig(format_type=ResponseFormat.JSON)
        self.formatter = ResponseFormatter(config)
    
    def test_format_json(self):
        content = {"key": "value"}
        formatted = self.formatter.format_response(content, ResponseFormat.JSON)
        self.assertTrue(formatted.startswith("{"))
    
    def test_format_text(self):
        content = "Hello world!"
        formatted = self.formatter.format_response(content, ResponseFormat.TEXT)
        self.assertIn("Hello world!", formatted)

if __name__ == '__main__':
    unittest.main()
