
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

