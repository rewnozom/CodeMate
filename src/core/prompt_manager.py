# src/core/prompt_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from pathlib import Path

@dataclass
class PromptTemplate:
    """Template for system prompts"""
    name: str
    content: str
    variables: List[str]
    description: str
    category: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_used: Optional[datetime] = None
    usage_count: int = 0

class PromptManager:
    """Manages system prompts and templates"""
    
    def __init__(self, prompt_dir: Optional[str] = None):
        self.prompt_dir = Path(prompt_dir) if prompt_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        self.default_prompts: Dict[str, str] = {}
        self._load_prompts()

    def _load_prompts(self) -> None:
        """Load prompts from configuration files"""
        if self.prompt_dir.exists():
            for prompt_file in self.prompt_dir.glob("*.yaml"):
                try:
                    with open(prompt_file) as f:
                        data = json.load(f)
                        for name, template_data in data.items():
                            self.templates[name] = PromptTemplate(
                                name=name,
                                content=template_data["content"],
                                variables=template_data.get("variables", []),
                                description=template_data.get("description", ""),
                                category=template_data.get("category", "general"),
                                metadata=template_data.get("metadata", {})
                            )
                except Exception as e:
                    print(f"Error loading prompt file {prompt_file}: {str(e)}")

    def get_prompt(self, name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Get formatted prompt from template"""
        if name not in self.templates:
            raise KeyError(f"Prompt template '{name}' not found")
            
        template = self.templates[name]
        content = template.content
        
        if variables:
            try:
                content = content.format(**variables)
            except KeyError as e:
                raise ValueError(f"Missing required variable {str(e)}")
                
        template.last_used = datetime.now()
        template.usage_count += 1
        
        return content

    def add_template(self, 
                    name: str,
                    content: str,
                    variables: List[str],
                    description: str = "",
                    category: str = "custom",
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add new prompt template"""
        if name in self.templates:
            raise ValueError(f"Template '{name}' already exists")
            
        self.templates[name] = PromptTemplate(
            name=name,
            content=content,
            variables=variables,
            description=description,
            category=category,
            metadata=metadata or {}
        )

    def update_template(self,
                       name: str,
                       content: Optional[str] = None,
                       variables: Optional[List[str]] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update existing template"""
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found")
            
        template = self.templates[name]
        if content is not None:
            template.content = content
        if variables is not None:
            template.variables = variables
        if metadata is not None:
            template.metadata.update(metadata)

    def get_templates_by_category(self, category: str) -> List[PromptTemplate]:
        """Get all templates in a category"""
        return [t for t in self.templates.values() if t.category == category]

    def get_template_variables(self, name: str) -> List[str]:
        """Get required variables for a template"""
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found")
        return self.templates[name].variables.copy()
