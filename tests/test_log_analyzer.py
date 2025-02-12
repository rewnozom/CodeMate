import unittest
import asyncio
import os
from datetime import datetime
from cmate.utils.log_analyzer import LogAnalyzer, LogAnalysis
from pathlib import Path

class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = LogAnalyzer()
        self.log_path = "temp/test_log.log"
        os.makedirs("temp", exist_ok=True)
        with open(self.log_path, "w") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{now} [INFO] [test] This is an info message\n")
            f.write(f"{now} [ERROR] [test] This is an error message\n")
    
    def test_analyze_log(self):
        async def run_test():
            analysis: LogAnalysis = await self.analyzer.analyze_log(self.log_path)
            self.assertGreaterEqual(analysis.total_entries, 2)
            self.assertIn("INFO", analysis.entries_by_level)
            self.assertIn("ERROR", analysis.entries_by_level)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
