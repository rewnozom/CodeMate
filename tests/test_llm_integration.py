import unittest
import asyncio
from cmate.llm.llm_agent import llm_agent

class TestLLMIntegration(unittest.TestCase):
    def test_ask_method(self):
        async def run_test():
            response = await llm_agent.ask("Hello, world!")
            self.assertIn("content", response)
            self.assertIsInstance(response["content"], str)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
