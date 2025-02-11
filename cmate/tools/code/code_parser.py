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
