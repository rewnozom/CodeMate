# /src/code/diff_generator.py
import difflib
import logging

logger = logging.getLogger(__name__)

def generate_diff(original_code: str, updated_code: str, fromfile: str = "original", tofile: str = "updated") -> str:
    """
    Generate a unified diff between original_code and updated_code.
    """
    diff = difflib.unified_diff(
        original_code.splitlines(keepends=True),
        updated_code.splitlines(keepends=True),
        fromfile=fromfile,
        tofile=tofile,
        lineterm=""
    )
    diff_text = "".join(diff)
    logger.debug("Generated diff.")
    return diff_text
