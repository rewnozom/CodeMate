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
