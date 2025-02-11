# Project Details

# Table of Contents
- [..\cmate\config\prompts.py](#-cmate-config-promptspy)
- [..\cmate\config\__init__.py](#-cmate-config-__init__py)


# ..\..\cmate\config\prompts.py
## File: ..\..\cmate\config\prompts.py

```py
# ..\..\cmate\config\prompts.py
# src/config/prompts.py
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import yaml

@dataclass
class PromptTemplate:
    """Template for system prompts"""
    name: str
    content: str
    variables: List[str]
    description: str
    category: str
    version: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class PromptConfig:
    """Manages prompt templates and configurations"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        self.categories: Dict[str, List[str]] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load prompt configurations"""
        if not self.config_dir.exists():
            return

        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file) as f:
                    data = yaml.safe_load(f)
                    category = config_file.stem
                    
                    for name, template_data in data.items():
                        template = PromptTemplate(
                            name=name,
                            content=template_data["content"].strip(),
                            variables=template_data.get("variables", []),
                            description=template_data.get("description", ""),
                            category=template_data.get("category", category),
                            version=template_data.get("version", "1.0"),
                            metadata=template_data.get("metadata", {})
                        )
                        
                        self.templates[name] = template
                        
                        if template.category not in self.categories:
                            self.categories[template.category] = []
                        self.categories[template.category].append(name)
                        
            except Exception as e:
                print(f"Error loading prompt config {config_file}: {str(e)}")

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get prompt template by name"""
        return self.templates.get(name)

    def get_category_templates(self, category: str) -> List[PromptTemplate]:
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
            
        try:
            return template.content.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing required variable: {str(e)}")

    def add_template(self,
                    name: str,
                    content: str,
                    variables: List[str],
                    description: str = "",
                    category: str = "custom",
                    version: str = "1.0",
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add new prompt template"""
        if name in self.templates:
            raise ValueError(f"Template already exists: {name}")
            
        template = PromptTemplate(
            name=name,
            content=content.strip(),
            variables=variables,
            description=description,
            category=category,
            version=version,
            metadata=metadata or {}
        )
        
        self.templates[name] = template
        
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
        
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
            template.content = content.strip()
        if variables is not None:
            template.variables = variables
        if metadata is not None:
            template.metadata.update(metadata)
            
        template.updated_at = datetime.now()
        template.version = self._increment_version(template.version)
        
        self._save_template(template)

    def _increment_version(self, version: str) -> str:
        """Increment version number"""
        parts = version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return '.'.join(parts)

    def _save_template(self, template: PromptTemplate) -> None:
        """Save template to configuration file"""
        config_file = self.config_dir / f"{template.category}.yaml"
        
        # Load existing templates
        templates_data = {}
        if config_file.exists():
            with open(config_file) as f:
                templates_data = yaml.safe_load(f) or {}
                
        # Update template
        templates_data[template.name] = {
            "content": template.content,
            "variables": template.variables,
            "description": template.description,
            "category": template.category,
            "version": template.version,
            "metadata": template.metadata
        }
        
        # Save to file
        with open(config_file, 'w') as f:
            yaml.dump(templates_data, f, default_flow_style=False)


```

---

# ..\..\cmate\config\__init__.py
## File: ..\..\cmate\config\__init__.py

```py
# ..\..\cmate\config\__init__.py
# Auto-generated __init__.py file

```

---

