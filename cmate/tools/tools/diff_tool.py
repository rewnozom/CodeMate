# /src/tools/diff_tool.py
import difflib

def generate_diff(original: str, updated: str, fromfile: str = 'original', tofile: str = 'updated') -> str:
    """
    Generate a unified diff between the original and updated text.
    """
    diff_lines = list(difflib.unified_diff(
        original.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        fromfile=fromfile,
        tofile=tofile,
        lineterm=''
    ))
    return ''.join(diff_lines)
