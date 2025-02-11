# /src/code/syntax_validator.py
import logging

logger = logging.getLogger(__name__)

def validate_syntax(code: str, filename: str = "<string>") -> bool:
    """
    Validate the Python code syntax by attempting to compile it.
    Returns True if valid, False otherwise.
    """
    try:
        compile(code, filename, "exec")
        logger.debug(f"Syntax validation passed for {filename}.")
        return True
    except SyntaxError as e:
        logger.error(f"Syntax validation failed for {filename}: {e}")
        return False
