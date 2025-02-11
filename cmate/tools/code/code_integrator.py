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
