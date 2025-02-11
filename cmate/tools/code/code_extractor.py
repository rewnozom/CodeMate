# /src/code/code_extractor.py
import re
import logging
from markdown_it import MarkdownIt

logger = logging.getLogger(__name__)

def extract_code_blocks(text: str) -> list:
    """
    Extract code blocks from text using regex.
    Returns a list of dictionaries with keys:
      - 'language'
      - 'code_block'
    """
    code_blocks = []
    # Use regex for markdown-style code blocks.
    pattern = r"```(\w+)\n(.*?)```"
    matches = re.finditer(pattern, text, re.DOTALL)
    for match in matches:
        language = match.group(1).strip()
        code_block = match.group(2).strip()
        code_blocks.append({
            "language": language,
            "code_block": code_block
        })
    # Fallback using MarkdownIt if none found.
    if not code_blocks:
        md = MarkdownIt()
        tokens = md.parse(text)
        for token in tokens:
            if token.type == "fence":
                language = token.info.strip()
                code_block = token.content.strip()
                code_blocks.append({
                    "language": language,
                    "code_block": code_block
                })
    logger.debug(f"Extracted {len(code_blocks)} code blocks.")
    return code_blocks

def extract_target_function(code: str, target_function: str) -> str:
    """
    Extract the code of a specific function by name from the code text.
    Uses regex to capture the function definition.
    """
    pattern = rf"def\s+{target_function}\s*\(.*?\):([\s\S]*?)(?=^def\s|\Z)"
    match = re.search(pattern, code, re.MULTILINE)
    if match:
        # Return the full function code (add the definition line)
        lines = code.splitlines()
        # Find the line where the function definition occurs
        for line in lines:
            if line.strip().startswith(f"def {target_function}("):
                function_def_line = line
                break
        else:
            function_def_line = f"def {target_function}(...):"
        return (function_def_line + "\n" + match.group(1)).strip()
    return ""
