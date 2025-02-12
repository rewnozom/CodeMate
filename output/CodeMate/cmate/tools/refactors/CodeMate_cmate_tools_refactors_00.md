# Project Details

# Table of Contents
- [..\CodeMate\cmate\tools\refactors\comment_tool.py](#-CodeMate-cmate-tools-refactors-comment_toolpy)


# ..\..\CodeMate\cmate\tools\refactors\comment_tool.py
## File: ..\..\CodeMate\cmate\tools\refactors\comment_tool.py

```py
# ..\..\CodeMate\cmate\tools\refactors\comment_tool.py
# ./refactors/comment_tool.py
import re
import logging

logger = logging.getLogger(__name__)

def remove_initial_comments(code: str) -> str:
    """
    Remove the initial comment (e.g., a file header with module path info).
    Assumes the very first line that starts with '#' is an initial comment.
    """
    lines = code.splitlines()
    if lines and lines[0].strip().startswith("#"):
        removed_line = lines.pop(0)
        logger.debug(f"Removed initial comment: {removed_line}")
    return "\n".join(lines)

def re_add_initial_comments(comments: list, code: str) -> str:
    """
    Prepend a list of comment lines to the code.
    """
    if comments:
        comments_str = "\n".join(comments) + "\n"
        logger.debug("Re-added initial comments.")
        return comments_str + code
    return code

def extract_initial_comments(code: str) -> (list, str):
    """
    Extract initial comment lines and return a tuple (comments, remaining_code).
    """
    lines = code.splitlines()
    comments = []
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            comments.append(line)
        else:
            return comments, "\n".join(lines[i:])
    return comments, ""

```

---

