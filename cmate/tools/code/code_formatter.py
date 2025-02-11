# /src/code/code_formatter.py
import logging
import black

logger = logging.getLogger(__name__)

def format_code(code: str) -> str:
    """
    Format code using Black.
    """
    try:
        formatted_code = black.format_str(code, mode=black.FileMode())
        logger.debug("Code formatted successfully with Black.")
        return formatted_code
    except Exception as e:
        logger.error(f"Error formatting code: {e}")
        return code
