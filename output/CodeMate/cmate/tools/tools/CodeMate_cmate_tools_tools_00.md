# Project Details

# Table of Contents
- [..\CodeMate\cmate\tools\tools\config_tool.py](#-CodeMate-cmate-tools-tools-config_toolpy)
- [..\CodeMate\cmate\tools\tools\diff_tool.py](#-CodeMate-cmate-tools-tools-diff_toolpy)
- [..\CodeMate\cmate\tools\tools\file_tool.py](#-CodeMate-cmate-tools-tools-file_toolpy)
- [..\CodeMate\cmate\tools\tools\logger_tool.py](#-CodeMate-cmate-tools-tools-logger_toolpy)


# ..\..\CodeMate\cmate\tools\tools\config_tool.py
## File: ..\..\CodeMate\cmate\tools\tools\config_tool.py

```py
# ..\..\CodeMate\cmate\tools\tools\config_tool.py
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

# ..\..\CodeMate\cmate\tools\tools\diff_tool.py
## File: ..\..\CodeMate\cmate\tools\tools\diff_tool.py

```py
# ..\..\CodeMate\cmate\tools\tools\diff_tool.py
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

# ..\..\CodeMate\cmate\tools\tools\file_tool.py
## File: ..\..\CodeMate\cmate\tools\tools\file_tool.py

```py
# ..\..\CodeMate\cmate\tools\tools\file_tool.py
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

# ..\..\CodeMate\cmate\tools\tools\logger_tool.py
## File: ..\..\CodeMate\cmate\tools\tools\logger_tool.py

```py
# ..\..\CodeMate\cmate\tools\tools\logger_tool.py
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

