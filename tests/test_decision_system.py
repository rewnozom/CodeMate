import unittest
from cmate.llm.model_selector import model_selector
from cmate.core.state_manager import AgentState

class TestDecisionSystem(unittest.TestCase):
    def test_model_selection(self):
        model = model_selector.select_model(AgentState.CODING)
        self.assertIsInstance(model, str)
        model_default = model_selector.select_model(AgentState.IDLE)
        self.assertEqual(model_default, model_selector.default_model)

if __name__ == '__main__':
    unittest.main()
