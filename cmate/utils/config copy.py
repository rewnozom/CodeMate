# src/utils/config.py
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path (Optional[str]): Path to the configuration file.
                                     Defaults to "config/default.yaml" if not provided.
    
    Returns:
        Dict[str, Any]: The configuration data as a dictionary.
    
    Raises:
        FileNotFoundError: If the configuration file is not found.
    """
    if config_path:
        path = Path(config_path)
    else:
        path = Path("config/default.yaml")
        
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
        
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config
