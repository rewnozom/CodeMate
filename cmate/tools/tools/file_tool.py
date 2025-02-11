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
