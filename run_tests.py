# ..\..\run_tests.py
#!/usr/bin/env python3
"""
run_tests.py

This custom test runner configures logging so that every test module logs to one common file.
After running all tests, it parses that log file and produces a sorted summary report (grouped by errors,
warnings, successes, and info). This version also adds an HTML log handler so that each test run produces
an interactive HTML report for easier review of the step-by-step process.
"""

import logging
import unittest
import os
from datetime import datetime
import atexit

# --- Configuration for the log file ---
LOG_DIR = "temp"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Use a timestamped log file for each test run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILENAME = os.path.join(LOG_DIR, f"test_run_{timestamp}.log")
SUMMARY_FILENAME = os.path.join(LOG_DIR, f"test_run_summary_{timestamp}.log")

# Configure logging for the whole test run (attach FileHandler and StreamHandler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILENAME, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("run_tests")
logger.info("Starting test run...")

# -------------------------------
# Integrate HTML logging handler for tests
# -------------------------------
from cmate.utils.html_logger import HTMLLogHandler
html_handler = HTMLLogHandler(log_dir="logs", filename_prefix="test_run")
# Attach the HTML log handler to the root logger so that all logs are captured.
logging.getLogger().addHandler(html_handler)
# Ensure the handler is closed when the process exits.
atexit.register(html_handler.close)

# --- Discover and run all tests ---
loader = unittest.TestLoader()
suite = loader.discover("tests")  # assumes tests are in the "tests" directory
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

logger.info("Test run completed.")

# --- Parse the unified log file and create a summary ---
def parse_log_file(log_file):
    """Parse the log file and sort lines by severity."""
    errors = []
    warnings = []
    successes = []
    infos = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if "[ERROR]" in line or "[CRITICAL]" in line:
                errors.append(line)
            elif "[WARNING]" in line:
                warnings.append(line)
            elif "[SUCCESS]" in line:
                successes.append(line)
            elif "[INFO]" in line or "[DEBUG]" in line:
                infos.append(line)
    return errors, warnings, successes, infos

errors, warnings, successes, infos = parse_log_file(LOG_FILENAME)

# Write the summary file
with open(SUMMARY_FILENAME, "w", encoding="utf-8") as summary:
    summary.write("==== TEST RUN SUMMARY ====\n")
    summary.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
    summary.write("==== ERRORS ====\n")
    summary.writelines(errors if errors else ["No errors recorded.\n"])
    summary.write("\n==== WARNINGS ====\n")
    summary.writelines(warnings if warnings else ["No warnings recorded.\n"])
    summary.write("\n==== SUCCESS ====\n")
    summary.writelines(successes if successes else ["No success messages recorded.\n"])
    summary.write("\n==== INFO / DEBUG ====\n")
    summary.writelines(infos if infos else ["No info messages recorded.\n"])

logger.info(f"Test run summary created at: {SUMMARY_FILENAME}")
