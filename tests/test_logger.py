import unittest
from cmate.utils.logger import setup_logging, get_logger
import os

class TestLogger(unittest.TestCase):
    def test_get_logger(self):
        logger = get_logger("test_logger")
        self.assertIsNotNone(logger)
        setup_logging("DEBUG", log_file="temp/test_logger.log")
        logger.debug("This is a test message")
        self.assertTrue(os.path.exists("temp/test_logger.log"))

if __name__ == '__main__':
    unittest.main()
