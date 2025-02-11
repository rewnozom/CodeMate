#!/usr/bin/env python
# cmate/utils/config.py

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def load_yaml_config(file_path: Path) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Determine the base configuration path by going three levels up from this file.
BASE_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "default.yaml"
default_config = load_yaml_config(BASE_CONFIG_PATH) if BASE_CONFIG_PATH.exists() else {}

# Merge environment-specific overrides (e.g. development.yaml or production.yaml)
ENV = os.getenv("ENVIRONMENT", "development")
override_path = Path(__file__).parent.parent.parent / "config" / f"{ENV}.yaml"
if override_path.exists():
    override_config = load_yaml_config(override_path)
    default_config.update(override_config)

# Load additional LLM settings from .env if necessary
default_config.setdefault("llm", {})
default_config["llm"]["temperature"] = float(os.getenv("TEMPERATURE", default_config["llm"].get("temperature", 0.7)))
default_config["llm"]["context_window"] = int(os.getenv("CONTEXT_WINDOW", default_config["llm"].get("context_window", 60000)))
default_config["llm"]["default_provider"] = os.getenv("LLM_PROVIDER", default_config["llm"].get("default_provider", "lm_studio"))

# Add conversation and prompt_optimizer settings if not present
default_config["llm"].setdefault("conversation", {"history_limit": 50})
default_config["llm"].setdefault("prompt_optimizer", {"enabled": True, "optimization_factor": 1.0})

# Expose the final configuration as a global variable
config = default_config

def load_config(config_path: str = None) -> dict:
    """
    Load configuration from a YAML file if provided;
    otherwise, return the default configuration.
    """
    if config_path:
        path = Path(config_path)
        if path.exists():
            return load_yaml_config(path)
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
    return config
