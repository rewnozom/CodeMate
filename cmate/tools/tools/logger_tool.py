# /src/tools/logger_tool.py
import logging
import sys
from rich.logging import RichHandler

def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """
    Set up logging with RichHandler and an optional file handler.
    """
    handlers = [RichHandler()]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        handlers.append(file_handler)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )

def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with the given name.
    """
    return logging.getLogger(name)
