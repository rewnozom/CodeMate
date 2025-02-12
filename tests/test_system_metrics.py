import unittest
import asyncio
from cmate.utils.system_metrics import MetricsCollector

class TestSystemMetrics(unittest.TestCase):
    def setUp(self):
        self.collector = MetricsCollector("temp/metrics")
    
    def test_collect_metrics(self):
        metrics = self.collector.collect_metrics()
        self.assertIn("cpu_percent", metrics.__dict__)
    
    def test_async_collect_metrics(self):
        async def run_test():
            metrics = await self.collector.async_collect_metrics()
            self.assertIsNotNone(metrics.network_io)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
