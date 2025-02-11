# Project Details

# Table of Contents
- [..\cmate\tools\tool.Docs.md](#-cmate-tools-toolDocsmd)
- [..\cmate\tools\code\code_extractor.py](#-cmate-tools-code-code_extractorpy)
- [..\cmate\tools\code\code_formatter.py](#-cmate-tools-code-code_formatterpy)
- [..\cmate\tools\code\code_integrator.py](#-cmate-tools-code-code_integratorpy)
- [..\cmate\tools\code\code_parser.py](#-cmate-tools-code-code_parserpy)
- [..\cmate\tools\code\diff_generator.py](#-cmate-tools-code-diff_generatorpy)
- [..\cmate\tools\code\import_merger.py](#-cmate-tools-code-import_mergerpy)
- [..\cmate\tools\code\syntax_validator.py](#-cmate-tools-code-syntax_validatorpy)
- [..\cmate\tools\extractors\csv_extractor.py](#-cmate-tools-extractors-csv_extractorpy)
- [..\cmate\tools\extractors\markdown_extractor.py](#-cmate-tools-extractors-markdown_extractorpy)
- [..\cmate\tools\processors\code_removal_processor.py](#-cmate-tools-processors-code_removal_processorpy)
- [..\cmate\tools\processors\llm_processor.py](#-cmate-tools-processors-llm_processorpy)
- [..\cmate\tools\processors\process_code_blocks.py](#-cmate-tools-processors-process_code_blockspy)
- [..\cmate\tools\refactors\comment_tool.py](#-cmate-tools-refactors-comment_toolpy)
- [..\cmate\tools\tools\config_tool.py](#-cmate-tools-tools-config_toolpy)
- [..\cmate\tools\tools\diff_tool.py](#-cmate-tools-tools-diff_toolpy)
- [..\cmate\tools\tools\file_tool.py](#-cmate-tools-tools-file_toolpy)
- [..\cmate\tools\tools\logger_tool.py](#-cmate-tools-tools-logger_toolpy)
- [..\cmate\tools\validators\removal_validator.py](#-cmate-tools-validators-removal_validatorpy)


# ..\..\cmate\tools\tool.Docs.md
## File: ..\..\cmate\tools\tool.Docs.md

```md
# ..\..\cmate\tools\tool.Docs.md

# Step-by-Step Plan for CodeMate Beta Version

> **Note:** This plan only covers the core “tools” and fixed update workflow.


### Under project’s `/cmate/` directory:

```
/cmate/
   /tools/
       file_tool.py         # File I/O, normalization, path validation, and backup creation.
       config_tool.py       # Loads and manages configuration (YAML and .env).
       diff_tool.py         # Generates unified diffs using difflib.
       logger_tool.py       # Sets up custom logging using RichHandler.
       
   /code/
       code_parser.py        # Converts code to/from AST (using ast or astor).
       code_formatter.py     # Formats code using Black.
       syntax_validator.py   # Validates code syntax (via compile()).
       code_extractor.py     # Extracts code blocks (or target functions) from input text.
       code_integrator.py    # Integrates new code (patches) into existing code via AST manipulation.
       import_merger.py      # Merges new import statements into existing code (avoiding duplicates).
       diff_generator.py     # Generates diffs between original and updated code.
       
   /processors/
       process_code_blocks.py  # Orchestrates the complete update process.
       llm_processor.py        # Sends extracted code to the LLM and retrieves the patch.
       # (Optional) code_removal_processor.py – postpone if not needed in beta.
       
   /extractors/
       markdown_extractor.py    # Generates Markdown reports with table of contents (if needed).
       # (Optional) csv_extractor.py – postpone if not part of beta.
       
   /validators/
       # (Optional) removal_validator.py – postpone if not needed in beta.
       
   /refactors/
       comment_tool.py          # Handles removal and re-adding of initial comments.
```

### 1.2. Archive Unused Modules  
Review your current modules (e.g., the parts of _full_backend_.py and Extractorz.py not needed for beta) and archive or remove features that are out of scope (like dynamic workflow logic or non-core extraction features).

---

## 2. Configuration and Logging

### 2.1. Implement `config_tool.py`  
- **Purpose:** Load a YAML configuration file (e.g., `config/default.yaml`) and merge environment variables from a `.env` file.  
- **Key Functions:**  
  - `load_config(config_path: Optional[str] = None) -> dict`  
  - `get_config_value(key: str, default: Any)`  
- **Tasks:**  
  1. Use PyYAML to load the configuration.
  2. Use the dotenv package to load environment variables.
  3. Merge environment-specific values and return a configuration dictionary.

### 2.2. Implement `logger_tool.py`  
- **Purpose:** Set up logging for your agent with both console and file handlers using RichHandler for enhanced formatting.  
- **Key Functions:**  
  - `setup_logging(log_level: str, log_file: str)`  
  - `get_logger(name: str) -> Logger`  
- **Tasks:**  
  1. Configure a RichHandler and a file handler.
  2. Expose a function to return a named logger for use across modules.

---

## 3. File Operations and Backup – `file_tool.py`

### 3.1. Implement Basic File Operations  
- **Key Functions:**  
  - `read_file(file_path: str) -> str`  
  - `write_file(file_path: str, content: str)`  
  - `validate_path(file_path: str) -> bool`  
- **Tasks:**  
  1. Use Python’s built-in functions to read and write files.
  2. Ensure that `validate_path` checks that the file exists and is accessible.

### 3.2. Implement Backup Creation  
- **Key Function:**  
  - `create_backup(file_path: str) -> str`  
- **Tasks:**  
  1. Create (if needed) a backup folder (e.g., `/backups/` or inside the file’s directory).
  2. Copy the original file to a new backup file with a timestamp appended (e.g., `cache_manager.py.bak_YYYYMMDD_HHMMSS`).
  3. Test the backup function with sample files.

---

## 4. Code Parsing and Formatting

### 4.1. Implement `code_parser.py`  
- **Purpose:** Convert source code to an AST and back.  
- **Key Functions:**  
  - `parse_code(code: str) -> ast.AST`  
  - `ast_to_code(tree: ast.AST) -> str`  
- **Tasks:**  
  1. Use Python’s `ast.parse()` to create the AST.
  2. Use `ast.unparse()` if available or fall back to the `astor` library to convert an AST back to source code.
  3. Include error handling and logging.

### 4.2. Implement `code_formatter.py`  
- **Purpose:** Format code using the Black library.  
- **Key Function:**  
  - `format_code(code: str) -> str`  
- **Tasks:**  
  1. Call `black.format_str(code, mode=black.FileMode())` and return the formatted code.
  2. Handle any exceptions and log errors.

---

## 5. Syntax Validation – `syntax_validator.py`

- **Purpose:** Check that modified code is syntactically correct.  
- **Key Function:**  
  - `validate_syntax(code: str, filename: str) -> bool`  
- **Tasks:**  
  1. Use the `compile()` function to test the code.
  2. Return `True` if no syntax errors occur; otherwise, log the error and return `False`.

---

## 6. Diff Generation – `diff_tool.py` (or `diff_generator.py`)

- **Purpose:** Generate a unified diff between two versions of code.  
- **Key Function:**  
  - `generate_diff(original: str, updated: str) -> str`  
- **Tasks:**  
  1. Use Python’s `difflib.unified_diff` to create a diff.
  2. Ensure that the diff is human readable and log it for auditing purposes.

---

## 7. Code Extraction – `code_extractor.py`

### 7.1. Implement Code Block/Function Extraction  
- **Purpose:** From an LLM output or a source file, extract the specific code block (e.g., a target function).  
- **Key Functions:**  
  - `extract_code_blocks(text: str) -> List[Dict[str, Any]]`  
  - Within this, implement logic to:  
    - Search for language-marked code blocks using regex.  
    - Identify special markers (e.g., a comment indicating a module path or function name).  
    - If no regex matches, fall back to using a Markdown parser (such as MarkdownIt).
- **Tasks:**  
  1. Integrate logic from your Extractorz.py module.
  2. Ensure the module can remove any unwanted markers (e.g., removal markers) and handle unchanged markers.
  3. Return a list of dictionaries with keys like `"action"`, `"module_path"`, `"class_name"`, `"method_name"`, `"code_block"`, and `"imports"`.

### 7.2. Implement Comment Handling in `comment_tool.py`  
- **Purpose:** Provide functions to remove initial comments (e.g., file path comments) before processing and re-add them after.  
- **Key Functions:**  
  - `remove_initial_comments(code: str) -> str`  
  - `re_add_initial_comments(comments: List[str], code: str) -> str`  
- **Tasks:**  
  1. Refactor and split out the related logic from your source modules.

---

## 8. Import Merging – `import_merger.py`

- **Purpose:** Merge new import statements from the updated code into the original code without duplication.  
- **Key Function:**  
  - `merge_imports(original_tree: ast.AST, new_tree: ast.AST) -> None`  
- **Tasks:**  
  1. Traverse the ASTs to extract all import nodes.
  2. Compare and insert any missing imports at the beginning of the original AST.
  3. Log each added import.

---

## 9. Code Integration – `code_integrator.py`

- **Purpose:** Replace or integrate updated code blocks (e.g., a function) into the original code.
- **Key Functions:**  
  - `integrate_node(original_tree: ast.AST, new_node: ast.AST) -> None`  
  - `integrate_nodes(original_tree: ast.AST, new_nodes: List[ast.AST]) -> None`  
  - `modify_node(tree: ast.AST, new_node: ast.AST) -> None`  
  - `add_import(tree: ast.AST, import_stmt: str) -> None`  
- **Tasks:**  
  1. Use the code parser to locate the target function node in the original AST.
  2. Replace that node with the new node from the patch.
  3. Use your import merger to integrate any new import statements.
  4. Convert the updated AST back to source code.

---

## 10. LLM Patch Generation – `llm_processor.py`

- **Purpose:** Interface with the LLM to generate patches based on a given prompt and the extracted code block.
- **Key Functions:**  
  - `process_llm_output(text: str, auto_run: bool = False) -> List[Dict[str, Any]]`  
  - `extract_code_blocks_from_text(text: str) -> List[Dict[str, Any]]`  
- **Tasks:**  
  1. Formulate a prompt (using a fixed template) instructing the LLM to update only a specific function (e.g., “update update_cache function”).
  2. Send the prompt (with the extracted function code) to your LLM integration.
  3. Process the returned patch to extract the updated function code.

---

## 11. Orchestrate the Update Process – `process_code_blocks.py`

- **Purpose:** Create a module that ties together all the above tools into a fixed update workflow.
- **Workflow Steps:**  
  1. **Receive Request:**  
     - A command such as:  
       `cmate process "update cache_manager.py: update update_cache function"`
     - Parse the command to identify the target file and function.
  2. **Backup Phase:**  
     - Use `file_tool.create_backup(file_path)` to back up the target file.
  3. **Extraction Phase:**  
     - Read the original file using `file_tool.read_file(file_path)`.
     - Extract the target function’s code using `code_extractor.extract_code_blocks(text)` (and further refine to target the specific function).
  4. **LLM Patch Generation:**  
     - Call `llm_processor.process_llm_output()` with the extracted code and a fixed prompt.
     - Retrieve the updated function code from the LLM response.
  5. **Validation Phase:**  
     - Validate the updated function using `syntax_validator.validate_syntax()`.
     - Generate a diff using `diff_generator.generate_diff(original_function_code, updated_function_code)`.
  6. **Integration Phase:**  
     - Parse the original file into an AST with `code_parser.parse_code()`.
     - Replace the target function’s node using `code_integrator.modify_node()` (or similar).
     - Merge any new imports via `import_merger.merge_imports()`.
     - Convert the updated AST back to code using `code_parser.ast_to_code()`.
     - Format the code with `code_formatter.format_code()`.
  7. **Write Updated File:**  
     - Save the updated file using `file_tool.write_file()`.
  8. **Audit and Reporting:**  
     - Log the diff and the update result.
     - Provide clear CLI feedback (e.g., “cache_manager.py updated successfully; diff: …”).

- **Error Handling:**  
  - At each step, check for errors.
  - If a validation error or syntax error occurs, abort the update.
  - Optionally, revert to the backup if needed.

---

## 12. Testing and Integration

### 12.1. Unit Testing for Each Tool Module  
- Write tests for each module:
  - **config_tool.py:** Ensure configuration values load correctly and override defaults.
  - **logger_tool.py:** Verify that logging is output both to console and file.
  - **file_tool.py:** Test file reading/writing and backup creation.
  - **code_parser.py / code_formatter.py:** Test conversion to/from AST and formatting with Black.
  - **syntax_validator.py:** Confirm that valid code passes and invalid code fails.
  - **diff_tool.py / diff_generator.py:** Verify diff output for known code changes.
  - **code_extractor.py:** Test extraction of a specific function from a sample file.
  - **import_merger.py:** Test that duplicate imports are not added.
  - **code_integrator.py:** Test replacing a target function in an AST.
  - **llm_processor.py:** Simulate an LLM response and ensure the patch is processed correctly.
  - **process_code_blocks.py:** Test the complete update workflow on a sample file.

### 12.2. Integration Testing  
- Create an integration test that:
  1. Uses a sample file (e.g., `cache_manager.py`) containing a target function (`update_cache`).
  2. Triggers the update process through your fixed workflow.
  3. Verifies that:
     - A backup file is created.
     - The target function is correctly extracted.
     - The LLM patch (or a simulated patch) is applied.
     - The resulting file is valid (passes syntax check) and contains only the intended changes.
     - A diff is generated and logged.

### 12.3. Manual Testing via CLI  
- Run the CLI commands (e.g., `cmate process "update cache_manager.py: update update_cache function"`) and verify that:
  - The process prints clear messages (backup created, extraction, patch generation, validation, integration, and update success).
  - Logs and diff outputs are available.

---

## 13. Documentation and Final Polishing

### 13.1. Update Documentation  
- Update your README.md with:
  - The new folder structure.
  - Detailed descriptions of each tool module and its functions.
  - Examples of how to run the update command via the CLI.

### 13.2. Code Quality  
- Run linters (e.g., flake8, pylint) and formatters on your codebase.
- Verify that logging is consistent and errors are handled gracefully.

---

## 14. Final Beta Release Preparation

### 14.1. Final Integration Tests  
- Re-run all unit and integration tests.
- Ensure that the entire update workflow (backup, extraction, LLM patch generation, validation, integration, file writing, diff reporting) works end-to-end.

### 14.2. Prepare the Beta Package  
- Package your project (using setup.py or a similar tool).
- Update installation instructions.
- Write release notes that document:
  - The fixed update workflow.
  - The key modules (tools, code, processors, etc.).
  - Known limitations and future plans.

### 14.3. Release the Beta Version  
- Publish the beta version for testing.
- Provide clear instructions on how to use the CLI.
- Monitor logs and collect user feedback for further improvements.


---

That completes the core modules you need for the beta version of CodeMate. You now have the following modules:

- **Tools:**  
  - `file_tool.py`  
  - `config_tool.py`  
  - `diff_tool.py`  
  - `logger_tool.py`

- **Code:**  
  - `code_parser.py`  
  - `code_formatter.py`  
  - `syntax_validator.py`  
  - `code_extractor.py`  
  - `code_integrator.py`  
  - `import_merger.py`  
  - `diff_generator.py`

- **Processors:**  
  - `process_code_blocks.py`  
  - `llm_processor.py`  
  - `code_removal_processor.py` (stub)

- **Extractors:**  
  - `markdown_extractor.py`  
  - `csv_extractor.py` (stub)

- **Validators:**  
  - `removal_validator.py` (stub)

- **Refactors:**  
  - `comment_tool.py`


```

---

# ..\..\cmate\tools\code\code_extractor.py
## File: ..\..\cmate\tools\code\code_extractor.py

```py
# ..\..\cmate\tools\code\code_extractor.py
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

# ..\..\cmate\tools\code\code_formatter.py
## File: ..\..\cmate\tools\code\code_formatter.py

```py
# ..\..\cmate\tools\code\code_formatter.py
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

# ..\..\cmate\tools\code\code_integrator.py
## File: ..\..\cmate\tools\code\code_integrator.py

```py
# ..\..\cmate\tools\code\code_integrator.py
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

# ..\..\cmate\tools\code\code_parser.py
## File: ..\..\cmate\tools\code\code_parser.py

```py
# ..\..\cmate\tools\code\code_parser.py
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

# ..\..\cmate\tools\code\diff_generator.py
## File: ..\..\cmate\tools\code\diff_generator.py

```py
# ..\..\cmate\tools\code\diff_generator.py
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

# ..\..\cmate\tools\code\import_merger.py
## File: ..\..\cmate\tools\code\import_merger.py

```py
# ..\..\cmate\tools\code\import_merger.py
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

# ..\..\cmate\tools\code\syntax_validator.py
## File: ..\..\cmate\tools\code\syntax_validator.py

```py
# ..\..\cmate\tools\code\syntax_validator.py
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

# ..\..\cmate\tools\extractors\csv_extractor.py
## File: ..\..\cmate\tools\extractors\csv_extractor.py

```py
# ..\..\cmate\tools\extractors\csv_extractor.py
# /src/extractors/csv_extractor.py
import os
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def extract_metrics_to_csv(file_paths: list, output_file: str) -> None:
    """
    Extract simple metrics (e.g., file path and file size) from the given file paths
    and save the data to a CSV file.
    """
    data = []
    for file_path in file_paths:
        try:
            path = Path(file_path)
            size = path.stat().st_size
            data.append({
                "Path": str(path),
                "Size": size
            })
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    logger.info(f"CSV metrics saved to {output_file}")

```

---

# ..\..\cmate\tools\extractors\markdown_extractor.py
## File: ..\..\cmate\tools\extractors\markdown_extractor.py

```py
# ..\..\cmate\tools\extractors\markdown_extractor.py
# /src/extractors/markdown_extractor.py
import os
import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_markdown_report(file_paths: list, extract_dir: str) -> (str, str):
    """
    Generate a Markdown report for the given file paths.
    Returns a tuple: (markdown_content, table_of_contents).
    """
    toc = "# Table of Contents\n\n"
    markdown_content = "# Project Report\n\n"
    file_lines_info = {}
    line_counter = markdown_content.count("\n") + 1

    for file_path in file_paths:
        relative_path = os.path.relpath(file_path, extract_dir)
        toc += f"- [{relative_path}](#{relative_path.replace(' ', '-').replace('.', '')})\n"
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            file_extension = Path(file_path).suffix.lstrip('.')
            start_line = line_counter
            line_counter += content.count("\n") + 5
            end_line = line_counter - 1
            file_lines_info[relative_path] = (start_line, end_line)
            markdown_content += f"## File: {relative_path}\n\n```{file_extension}\n{content}\n```\n\n"
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            continue

    toc_content = toc + "\n"
    logger.debug("Markdown report generated.")
    return markdown_content, toc_content

```

---

# ..\..\cmate\tools\processors\code_removal_processor.py
## File: ..\..\cmate\tools\processors\code_removal_processor.py

```py
# ..\..\cmate\tools\processors\code_removal_processor.py
# /src/processors/code_removal_processor.py
import logging

logger = logging.getLogger(__name__)

def process_removal_instructions(removal_instructions: dict, original_code: str) -> str:
    """
    Process removal instructions to remove specified code elements from the original code.
    (This is a basic stub for beta.)
    Assume removal_instructions is a dict with a 'targets' list, each with a "type" and "name".
    """
    updated_code = original_code
    targets = removal_instructions.get("targets", [])
    for target in targets:
        if target.get("type") == "function":
            func_name = target.get("name")
            import re
            pattern = rf"def\s+{func_name}\s*\(.*?\):([\s\S]*?)(?=^def\s|\Z)"
            updated_code, count = re.subn(pattern, "", updated_code, flags=re.MULTILINE)
            logger.debug(f"Removed {count} instances of function {func_name}")
    return updated_code

```

---

# ..\..\cmate\tools\processors\llm_processor.py
## File: ..\..\cmate\tools\processors\llm_processor.py

```py
# ..\..\cmate\tools\processors\llm_processor.py
# /src/processors/llm_processor.py
import logging
from ..code.code_extractor import extract_code_blocks

logger = logging.getLogger(__name__)

def process_llm_output(text: str) -> list:
    """
    Process LLM output text.
    Extract code blocks and simulate a patch response.
    In this beta version, simply prepend a comment to each code block.
    """
    code_blocks = extract_code_blocks(text)
    patched_blocks = []
    for block in code_blocks:
        patched_code = f"# Patched by LLM\n{block['code_block']}"
        patched_blocks.append({
            "language": block["language"],
            "code_block": patched_code
        })
    logger.debug(f"Processed {len(patched_blocks)} patched code blocks from LLM output.")
    return patched_blocks

```

---

# ..\..\cmate\tools\processors\process_code_blocks.py
## File: ..\..\cmate\tools\processors\process_code_blocks.py

```py
# ..\..\cmate\tools\processors\process_code_blocks.py
# processors/process_code_blocks.py
import logging
from ..tools.file_tool import read_file, write_file, create_backup, validate_path
from ..code.code_parser import parse_code, ast_to_code
from ..code.code_integrator import integrate_node
from ..code.syntax_validator import validate_syntax
from ..code.diff_generator import generate_diff
from ..code.code_formatter import format_code
from ..code.code_extractor import extract_target_function

logger = logging.getLogger(__name__)

def process_code_block_update(file_path: str, target_function: str, updated_function_code: str) -> dict:
    """
    Execute the update process for a specific function in a file.
    
    Steps:
      1. Validate that the file exists.
      2. Create a backup of the file.
      3. Read the original file.
      4. Extract the current target function (for diffing).
      5. Integrate the updated function into the original code.
      6. Validate syntax of the updated code.
      7. Format the updated code.
      8. Generate a diff between original and updated versions.
      9. Write the updated code back to the file.
      10. Return the status and diff.
    """
    # Step 1: Validate file exists.
    if not validate_path(file_path):
        msg = f"File {file_path} does not exist or is not readable."
        logger.error(msg)
        return {"success": False, "error": msg}
    
    # Step 2: Create backup.
    backup_path = create_backup(file_path)
    logger.info(f"Backup created at {backup_path}")
    
    # Step 3: Read the original file.
    original_code = read_file(file_path)
    
    # Step 4: Extract the current target function code.
    original_function_code = extract_target_function(original_code, target_function)
    if not original_function_code:
        msg = f"Target function {target_function} not found in the original file."
        logger.error(msg)
        return {"success": False, "error": msg}
    
    # Step 5: Integrate updated function code.
    try:
        updated_full_code = integrate_node(original_code, updated_function_code, target_function)
    except Exception as e:
        msg = f"Error integrating updated function: {e}"
        logger.error(msg)
        return {"success": False, "error": msg}
    
    # Step 6: Validate syntax.
    if not validate_syntax(updated_full_code, file_path):
        msg = "Updated code has syntax errors."
        logger.error(msg)
        return {"success": False, "error": msg}
    
    # Step 7: Format the updated code.
    updated_full_code = format_code(updated_full_code)
    
    # Step 8: Generate diff.
    diff_text = generate_diff(original_code, updated_full_code, fromfile="Original", tofile="Updated")
    
    # Step 9: Write updated file.
    write_file(file_path, updated_full_code)
    logger.info(f"Updated file written to {file_path}")
    
    # Step 10: Return result.
    return {
        "success": True,
        "message": f"File {file_path} updated successfully.",
        "backup": backup_path,
        "diff": diff_text
    }

```

---

# ..\..\cmate\tools\refactors\comment_tool.py
## File: ..\..\cmate\tools\refactors\comment_tool.py

```py
# ..\..\cmate\tools\refactors\comment_tool.py
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

# ..\..\cmate\tools\tools\config_tool.py
## File: ..\..\cmate\tools\tools\config_tool.py

```py
# ..\..\cmate\tools\tools\config_tool.py
# /src/tools/config_tool.py
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def load_config(config_path: str = None) -> dict:
    """
    Load configuration from a YAML file.
    If config_path is None, defaults to 'config/default.yaml' relative to the project root.
    """
    if config_path:
        path = Path(config_path)
    else:
        path = Path("config/default.yaml")
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def get_config_value(config: dict, key: str, default: any = None) -> any:
    """Retrieve a configuration value with a default."""
    return config.get(key, default)

```

---

# ..\..\cmate\tools\tools\diff_tool.py
## File: ..\..\cmate\tools\tools\diff_tool.py

```py
# ..\..\cmate\tools\tools\diff_tool.py
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

```

---

# ..\..\cmate\tools\tools\file_tool.py
## File: ..\..\cmate\tools\tools\file_tool.py

```py
# ..\..\cmate\tools\tools\file_tool.py
# /src/tools/file_tool.py
import os
import shutil
from datetime import datetime
from pathlib import Path

def read_file(file_path: str) -> str:
    """Read file content from the given file path."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path: str, content: str) -> None:
    """Write content to the given file path."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def validate_path(file_path: str) -> bool:
    """Check if the file exists and is readable."""
    path = Path(file_path)
    return path.is_file() and os.access(str(path), os.R_OK)

def create_backup(file_path: str, backup_dir: str = None) -> str:
    """
    Create a backup copy of the given file.
    If backup_dir is not provided, create a "backups" folder in the same directory as the file.
    Returns the backup file path.
    """
    original_path = Path(file_path)
    if not original_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if backup_dir is None:
        backup_dir = original_path.parent / "backups"
    else:
        backup_dir = Path(backup_dir)
    
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{original_path.stem}.bak_{timestamp}{original_path.suffix}"
    backup_path = backup_dir / backup_filename
    shutil.copy2(str(original_path), str(backup_path))
    return str(backup_path)

```

---

# ..\..\cmate\tools\tools\logger_tool.py
## File: ..\..\cmate\tools\tools\logger_tool.py

```py
# ..\..\cmate\tools\tools\logger_tool.py
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

```

---

# ..\..\cmate\tools\validators\removal_validator.py
## File: ..\..\cmate\tools\validators\removal_validator.py

```py
# ..\..\cmate\tools\validators\removal_validator.py
# /src/validators/removal_validator.py
import json
import logging

logger = logging.getLogger(__name__)

def validate_removal_instructions(instructions: str) -> bool:
    """
    Validate removal instructions provided as JSON.
    Returns True if valid, False otherwise.
    """
    try:
        data = json.loads(instructions)
        if "targets" in data and isinstance(data["targets"], list):
            logger.debug("Removal instructions validated successfully.")
            return True
        else:
            logger.error("Removal instructions missing 'targets' list.")
            return False
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in removal instructions: {e}")
        return False

```

---

