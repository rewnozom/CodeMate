import unittest
from cmate.utils.config import load_config

class TestConfig(unittest.TestCase):
    def test_load_default_config(self):
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn("general", config)

if __name__ == '__main__':
    unittest.main()
