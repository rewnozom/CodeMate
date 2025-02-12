# ..\..\cmate\utils\logger.py
# src/utils/logger.py
import logging
import sys
from rich.logging import RichHandler

# --- Define a custom SUCCESS log level ---
SUCCESS_LEVEL = 25  # Place this between INFO (20) and WARNING (30)
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)

# Add the success method to the Logger class
logging.Logger.success = success

def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """
    Configure the root logger to use RichHandler and, optionally, a file handler.
    
    Args:
        log_level (str): The logging level (e.g., "DEBUG", "INFO").
        log_file (str, optional): Path to a file to also log messages.
    """
    # Configure RichHandler for pretty console output
    rich_handler = RichHandler(rich_tracebacks=True)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    
    handlers = [rich_handler, console_handler]
    
    # If a log_file is provided, add a FileHandler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers
    )

def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with the specified name.
    
    Args:
        name (str): The name of the logger.
    
    Returns:
        logging.Logger: The configured logger.
    """
    return logging.getLogger(name)
