import unittest
from cmate.utils.prompt_templates import PromptTemplateManager

class TestPromptTemplates(unittest.TestCase):
    def setUp(self):
        self.ptm = PromptTemplateManager("config/prompts")
    
    def test_get_and_format_template(self):
        template = self.ptm.get_template("system_prompt")
        self.assertIsNotNone(template)
        formatted = self.ptm.format_prompt("system_prompt", {})
        self.assertIn("semi-autonomous", formatted)

if __name__ == '__main__':
    unittest.main()
