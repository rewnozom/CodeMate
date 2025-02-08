# src/utils/prompt_templates.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import yaml
from pathlib import Path
import re

@dataclass
class PromptTemplate:
    """Template for system prompts"""
    name: str
    content: str
    variables: List[str]
    description: str
    category: str
    version: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class PromptTemplateManager:
    """Manages system prompt templates"""
    
    def __init__(self, template_dir: Optional[str] = None):
        self.template_dir = Path(template_dir) if template_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        self.categories: Dict[str, List[str]] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load templates from configuration files"""
        if not self.template_dir.exists():
            return

        for template_file in self.template_dir.glob("*.yaml"):
            try:
                with open(template_file) as f:
                    data = yaml.safe_load(f)
                    for name, template_data in data.items():
                        template = PromptTemplate(
                            name=name,
                            content=template_data["content"],
                            variables=template_data.get("variables", []),
                            description=template_data.get("description", ""),
                            category=template_data.get("category", "general"),
                            version=template_data.get("version", "1.0"),
                            metadata=template_data.get("metadata", {})
                        )
                        
                        self.templates[name] = template
                        
                        # Update categories
                        if template.category not in self.categories:
                            self.categories[template.category] = []
                        self.categories[template.category].append(name)
                        
            except Exception as e:
                print(f"Error loading template file {template_file}: {str(e)}")

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get template by name"""
        return self.templates.get(name)

    def get_templates_by_category(self, category: str) -> List[PromptTemplate]:
        """Get all templates in category"""
        template_names = self.categories.get(category, [])
        return [self.templates[name] for name in template_names]

    def format_prompt(self, 
                     template_name: str,
                     variables: Dict[str, Any]) -> str:
        """Format prompt with variables"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")
            
        # Validate variables
        missing_vars = set(template.variables) - set(variables.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")
            
        try:
            return template.content.format(**variables)
        except KeyError as e:
            raise ValueError(f"Invalid variable reference: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error formatting prompt: {str(e)}")

    def add_template(self,
                    name: str,
                    content: str,
                    variables: List[str],
                    description: str = "",
                    category: str = "custom",
                    version: str = "1.0",
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add new template"""
        if name in self.templates:
            raise ValueError(f"Template already exists: {name}")
            
        template = PromptTemplate(
            name=name,
            content=content,
            variables=variables,
            description=description,
            category=category,
            version=version,
            metadata=metadata or {}
        )
        
        self.templates[name] = template
        
        # Update categories
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
        
        # Save to file
        self._save_template(template)

    def update_template(self,
                       name: str,
                       content: Optional[str] = None,
                       variables: Optional[List[str]] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update existing template"""
        template = self.get_template(name)
        if not template:
            raise ValueError(f"Template not found: {name}")
            
        if content is not None:
            template.content = content
        if variables is not None:
            template.variables = variables
        if metadata is not None:
            template.metadata.update(metadata)
            
        # Update version
        version_parts = template.version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        template.version = '.'.join(version_parts)
        
        # Save changes
        self._save_template(template)

    def _save_template(self, template: PromptTemplate) -> None:
        """Save template to file"""
        if not self.template_dir.exists():
            self.template_dir.mkdir(parents=True)
            
        file_path = self.template_dir / f"{template.category}.yaml"
        
        # Load existing templates in category
        templates_data = {}
        if file_path.exists():
            with open(file_path) as f:
                templates_data = yaml.safe_load(f) or {}
                
        # Update template data
        templates_data[template.name] = {
            "content": template.content,
            "variables": template.variables,
            "description": template.description,
            "category": template.category,
            "version": template.version,
            "metadata": template.metadata
        }
        
        # Save to file
        with open(file_path, 'w') as f:
            yaml.dump(templates_data, f, sort_keys=False, indent=2)

    def extract_variables(self, content: str) -> List[str]:
        """Extract variable names from template content"""
        return [m.group(1) for m in re.finditer(r'\{(\w+)\}', content)]