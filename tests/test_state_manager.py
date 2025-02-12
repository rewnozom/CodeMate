import unittest
from cmate.core.state_manager import StateManager, AgentState

class TestStateManager(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()
    
    def test_valid_transition(self):
        self.state_manager.update_state(AgentState.SCANNING_WORKSPACE, {"user_request": "scan"})
        self.assertEqual(self.state_manager.current_state, AgentState.SCANNING_WORKSPACE)
    
    def test_invalid_transition(self):
        with self.assertRaises(ValueError):
            self.state_manager.update_state(AgentState.CODING, {"user_request": "invalid transition"})

if __name__ == '__main__':
    unittest.main()
