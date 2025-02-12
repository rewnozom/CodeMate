# ..\..\cmate\core\prompt_manager.py
"""
prompt_manager.py

Manages the system's prompt templates. Loads prompts from configuration
files (in YAML format) and allows adding, updating, and retrieving formatted prompts.
To avoid confusion for the agent, each prompt contains detailed guidance.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import os
import logging

# For loading YAML files
try:
    import yaml
except ImportError:
    yaml = None
    print("Warning: PyYAML is missing. Install with 'pip install pyyaml' to load YAML prompts.")

logger = logging.getLogger(__name__)

@dataclass
class PromptTemplate:
    name: str
    content: str
    variables: List[str]
    description: str
    category: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_used: Optional[datetime] = None
    usage_count: int = 0
    # Assuming version is needed for update_template (if not, you may remove it)
    version: str = "1.0.0"

class PromptManager:
    def __init__(self, prompt_dir: Optional[str] = None):
        self.prompt_dir = Path(prompt_dir) if prompt_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        logger.info("Initializing PromptManager with directory: %s", self.prompt_dir)
        self._load_prompts()
        self._load_default_prompts()
        logger.success("PromptManager loaded successfully with %d templates.", len(self.templates))

    def _load_prompts(self) -> None:
        """Load prompts from YAML files in prompt_dir."""
        if self.prompt_dir.exists():
            for prompt_file in self.prompt_dir.glob("*.yaml"):
                try:
                    with open(prompt_file, 'r', encoding='utf-8') as f:
                        if yaml:
                            data = yaml.safe_load(f)
                        else:
                            data = {}  # If YAML is missing, skip
                        for name, template_data in data.items():
                            self.templates[name] = PromptTemplate(
                                name=name,
                                content=template_data["content"],
                                variables=template_data.get("variables", []),
                                description=template_data.get("description", ""),
                                category=template_data.get("category", "general"),
                                metadata=template_data.get("metadata", {})
                            )
                    logger.debug("Loaded prompts from file: %s", prompt_file)
                except Exception as e:
                    logger.error("Error loading prompt file %s: %s", prompt_file, str(e))
        else:
            logger.warning("Prompt directory does not exist: %s", self.prompt_dir)

    def _load_default_prompts(self) -> None:
        """
        If no prompts have been loaded or to supplement them,
        load some default prompts with detailed guidance.
        """
        defaults = {
            "system_prompt": PromptTemplate(
                name="system_prompt",
                content=(
                    "You are a semi-autonomous agent specialized in analyzing, modifying, and testing code. "
                    "Work systematically: analyze the situation, plan carefully, implement with meticulous adherence "
                    "to coding style, and test thoroughly. Only use files in the ./Workspace directory. Be diligent with "
                    "documentation and debugging as needed."
                ),
                variables=[],
                description="Base prompt for agent initialization with clear guidance",
                category="system"
            ),
            "analysis_prompt": PromptTemplate(
                name="analysis_prompt",
                content=(
                    "Analyze the following files and provide an overview of the structure, identifying key components, "
                    "potential issues, and dependencies. Prepare a list of recommended actions.\nFiles: {files}"
                ),
                variables=["files"],
                description="Detailed prompt for file analysis with step-by-step guidance",
                category="analysis"
            ),
            "implementation_prompt": PromptTemplate(
                name="implementation_prompt",
                content=(
                    "Implement the requested changes according to the following guidelines:\n"
                    "1. Follow the existing coding style meticulously.\n"
                    "2. Add appropriate documentation to the code.\n"
                    "3. Write unit tests to validate the changes.\n"
                    "4. Incorporate robust error handling.\n\n"
                    "Changes: {changes}\nAffected files: {files}"
                ),
                variables=["changes", "files"],
                description="Prompt for implementation steps with clear instructions",
                category="implementation"
            ),
            "test_prompt": PromptTemplate(
                name="test_prompt",
                content=(
                    "Create tests for the following changes:\n"
                    "1. Unit tests for the new functionality.\n"
                    "2. Integration tests where necessary.\n"
                    "3. Coverage of edge cases and error handling.\n\n"
                    "Implementation: {implementation}\nFiles to test: {files}"
                ),
                variables=["implementation", "files"],
                description="Prompt for test development with detailed requirements",
                category="testing"
            )
        }
        for key, prompt in defaults.items():
            if key not in self.templates:
                self.templates[key] = prompt
                logger.debug("Default prompt added: %s", key)

    def get_prompt(self, name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        if name not in self.templates:
            error_msg = f"Prompt template '{name}' not found"
            logger.error(error_msg)
            raise KeyError(error_msg)
        template = self.templates[name]
        content = template.content
        if variables:
            try:
                content = content.format(**variables)
            except KeyError as e:
                error_msg = f"Missing required variable {str(e)} for template {name}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        template.last_used = datetime.now()
        template.usage_count += 1
        logger.debug("Retrieved prompt '%s' with variables: %s", name, variables)
        return content

    def add_template(self, name: str, content: str, variables: List[str], description: str = "", category: str = "custom", metadata: Optional[Dict[str, Any]] = None) -> None:
        if name in self.templates:
            error_msg = f"Template '{name}' already exists"
            logger.error(error_msg)
            raise ValueError(error_msg)
        self.templates[name] = PromptTemplate(
            name=name,
            content=content,
            variables=variables,
            description=description,
            category=category,
            metadata=metadata or {}
        )
        logger.success("Added new template: %s", name)

    def update_template(self, name: str, content: Optional[str] = None, variables: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        if name not in self.templates:
            error_msg = f"Template '{name}' not found"
            logger.error(error_msg)
            raise KeyError(error_msg)
        template = self.templates[name]
        if content is not None:
            template.content = content
        if variables is not None:
            template.variables = variables
        if metadata is not None:
            template.metadata.update(metadata)
        # Update version (simple increment)
        version_parts = template.version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        template.version = '.'.join(version_parts)
        logger.success("Updated template '%s' to version %s", name, template.version)

    def get_templates_by_category(self, category: str) -> List[PromptTemplate]:
        return [t for t in self.templates.values() if t.category == category]

    def get_template_variables(self, name: str) -> List[str]:
        if name not in self.templates:
            error_msg = f"Template '{name}' not found"
            logger.error(error_msg)
            raise KeyError(error_msg)
        return self.templates[name].variables.copy()
