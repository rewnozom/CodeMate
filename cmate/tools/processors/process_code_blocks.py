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
