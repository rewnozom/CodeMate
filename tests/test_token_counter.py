import unittest
from cmate.utils.token_counter import TokenCounter

class TestTokenCounter(unittest.TestCase):
    def setUp(self):
        self.counter = TokenCounter("gpt-3.5-turbo")
    
    def test_count_tokens(self):
        text = "Hello, world! This is a test."
        result = self.counter.count_tokens(text)
        self.assertGreater(result.total_tokens, 0)
    
    def test_truncate_to_token_limit(self):
        text = "word " * 1000
        truncated = self.counter.truncate_to_token_limit(text, 100)
        result = self.counter.count_tokens(truncated)
        self.assertLessEqual(result.total_tokens, 100)

if __name__ == '__main__':
    unittest.main()
