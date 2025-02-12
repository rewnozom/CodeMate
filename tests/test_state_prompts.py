import unittest
from cmate.core.prompt_manager import PromptManager

class TestStatePrompts(unittest.TestCase):
    def setUp(self):
        self.prompt_manager = PromptManager("config/prompts")
    
    def test_get_system_prompt(self):
        prompt = self.prompt_manager.get_prompt("system_prompt")
        self.assertIsInstance(prompt, str)
        self.assertIn("semi-autonomous", prompt)

if __name__ == '__main__':
    unittest.main()
