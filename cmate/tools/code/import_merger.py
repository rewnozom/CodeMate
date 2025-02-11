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
