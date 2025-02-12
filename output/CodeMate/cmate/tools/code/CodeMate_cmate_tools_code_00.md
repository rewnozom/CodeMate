# Project Details

# Table of Contents
- [..\CodeMate\cmate\tools\code\code_extractor.py](#-CodeMate-cmate-tools-code-code_extractorpy)
- [..\CodeMate\cmate\tools\code\code_formatter.py](#-CodeMate-cmate-tools-code-code_formatterpy)
- [..\CodeMate\cmate\tools\code\code_integrator.py](#-CodeMate-cmate-tools-code-code_integratorpy)
- [..\CodeMate\cmate\tools\code\code_parser.py](#-CodeMate-cmate-tools-code-code_parserpy)
- [..\CodeMate\cmate\tools\code\diff_generator.py](#-CodeMate-cmate-tools-code-diff_generatorpy)
- [..\CodeMate\cmate\tools\code\import_merger.py](#-CodeMate-cmate-tools-code-import_mergerpy)
- [..\CodeMate\cmate\tools\code\syntax_validator.py](#-CodeMate-cmate-tools-code-syntax_validatorpy)


# ..\..\CodeMate\cmate\tools\code\code_extractor.py
## File: ..\..\CodeMate\cmate\tools\code\code_extractor.py

```py
# ..\..\CodeMate\cmate\tools\code\code_extractor.py
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

```

---

# ..\..\CodeMate\cmate\tools\code\code_formatter.py
## File: ..\..\CodeMate\cmate\tools\code\code_formatter.py

```py
# ..\..\CodeMate\cmate\tools\code\code_formatter.py
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

```

---

# ..\..\CodeMate\cmate\tools\code\code_integrator.py
## File: ..\..\CodeMate\cmate\tools\code\code_integrator.py

```py
# ..\..\CodeMate\cmate\tools\code\code_integrator.py
# /src/code/code_integrator.py
import ast
import logging
from .code_parser import parse_code, ast_to_code
from .import_merger import merge_imports

logger = logging.getLogger(__name__)

def integrate_node(original_code: str, new_function_code: str, target_function: str) -> str:
    """
    Integrate the updated target function into the original code.
    Replaces the existing function definition with the new one.
    """
    try:
        original_tree = parse_code(original_code)
        new_tree = parse_code(new_function_code)
    except Exception as e:
        logger.error(f"Error parsing code: {e}")
        raise

    # Find the function node to be replaced in the original AST.
    target_index = None
    for i, node in enumerate(original_tree.body):
        if isinstance(node, ast.FunctionDef) and node.name == target_function:
            target_index = i
            break

    if target_index is None:
        msg = f"Target function {target_function} not found in the original code."
        logger.error(msg)
        raise ValueError(msg)

    # Assume the first node of new_tree is the updated function.
    updated_node = new_tree.body[0]
    original_tree.body[target_index] = updated_node

    # Merge any new imports from new_tree.
    merge_imports(original_tree, new_tree)

    updated_code = ast_to_code(original_tree)
    logger.debug("Integrated updated function into original code.")
    return updated_code

```

---

# ..\..\CodeMate\cmate\tools\code\code_parser.py
## File: ..\..\CodeMate\cmate\tools\code\code_parser.py

```py
# ..\..\CodeMate\cmate\tools\code\code_parser.py
# /src/code/code_parser.py
import ast
import logging

try:
    # For Python 3.9 and later
    from ast import unparse as ast_unparse
except ImportError:
    import astor

logger = logging.getLogger(__name__)

def parse_code(code: str) -> ast.AST:
    """
    Parse Python source code into an AST.
    """
    try:
        tree = ast.parse(code)
        logger.debug("Parsed code into AST successfully.")
        return tree
    except SyntaxError as e:
        logger.error(f"Syntax error while parsing code: {e}")
        raise

def ast_to_code(tree: ast.AST) -> str:
    """
    Convert an AST back to Python source code.
    Uses ast.unparse if available; otherwise, falls back to astor.
    """
    try:
        if 'ast_unparse' in globals():
            code = ast_unparse(tree)
        else:
            code = astor.to_source(tree)
        logger.debug("Converted AST back to source code successfully.")
        return code
    except Exception as e:
        logger.error(f"Error converting AST to code: {e}")
        raise

```

---

# ..\..\CodeMate\cmate\tools\code\diff_generator.py
## File: ..\..\CodeMate\cmate\tools\code\diff_generator.py

```py
# ..\..\CodeMate\cmate\tools\code\diff_generator.py
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

```

---

# ..\..\CodeMate\cmate\tools\code\import_merger.py
## File: ..\..\CodeMate\cmate\tools\code\import_merger.py

```py
# ..\..\CodeMate\cmate\tools\code\import_merger.py
# /src/code/import_merger.py
import ast
import logging

logger = logging.getLogger(__name__)

def merge_imports(original_tree: ast.AST, new_tree: ast.AST) -> None:
    """
    Merge import statements from new_tree into original_tree without duplicates.
    """
    original_imports = [node for node in original_tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    new_imports = [node for node in new_tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    existing_imports = set(ast.dump(node) for node in original_imports)
    for new_imp in new_imports:
        if ast.dump(new_imp) not in existing_imports:
            original_tree.body.insert(0, new_imp)
            logger.debug(f"Added new import: {ast.dump(new_imp)}")

```

---

# ..\..\CodeMate\cmate\tools\code\syntax_validator.py
## File: ..\..\CodeMate\cmate\tools\code\syntax_validator.py

```py
# ..\..\CodeMate\cmate\tools\code\syntax_validator.py
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

```

---

