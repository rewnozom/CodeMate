"""
prompt_manager.py

Hanterar systemets promptmallar. Laddar promptar från konfigurationsfiler
(i YAML-format) och möjliggör att lägga till, uppdatera och hämta formaterade promptar.
För att undvika förvirring hos agenten innehåller varje prompt utförlig vägledning.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import os

# För att ladda YAML-filer
try:
    import yaml
except ImportError:
    yaml = None
    print("Varning: PyYAML saknas. Installera med 'pip install pyyaml' för att ladda YAML-promptar.")

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

class PromptManager:
    def __init__(self, prompt_dir: Optional[str] = None):
        self.prompt_dir = Path(prompt_dir) if prompt_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        # Ladda från filer och eventuella default promptar
        self._load_prompts()
        self._load_default_prompts()

    def _load_prompts(self) -> None:
        """Ladda promptar från YAML-filer i prompt_dir."""
        if self.prompt_dir.exists():
            for prompt_file in self.prompt_dir.glob("*.yaml"):
                try:
                    with open(prompt_file, 'r', encoding='utf-8') as f:
                        if yaml:
                            data = yaml.safe_load(f)
                        else:
                            data = {}  # Om yaml saknas, hoppa över
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

    def _load_default_prompts(self) -> None:
        """
        Om inga promptar laddats in, eller för att komplettera,
        lägg in några standardpromptar med utförlig vägledning.
        """
        defaults = {
            "system_prompt": PromptTemplate(
                name="system_prompt",
                content=(
                    "Du är en semi-autonom agent specialiserad på att analysera, modifiera och testa kod. "
                    "Arbeta systematiskt: analysera läget, planera noggrant, implementera med hänsyn till kodstil, "
                    "och testa utförligt. Använd endast filer i ./Workspace. Var noggrann med dokumentation och "
                    "felsökning vid behov."
                ),
                variables=[],
                description="Basprompt för agentinitialisering med tydlig vägledning",
                category="system"
            ),
            "analysis_prompt": PromptTemplate(
                name="analysis_prompt",
                content=(
                    "Analysera följande filer och ge en översikt av strukturen, identifiera nyckelkomponenter, "
                    "potentiella problem och beroenden. Förbered en lista med rekommenderade åtgärder.\nFiler: {files}"
                ),
                variables=["files"],
                description="Detaljerad prompt för filanalys med stegvis vägledning",
                category="analysis"
            ),
            "implementation_prompt": PromptTemplate(
                name="implementation_prompt",
                content=(
                    "Implementera de begärda ändringarna enligt följande riktlinjer:\n"
                    "1. Följ den befintliga kodstilen noggrant.\n"
                    "2. Lägg till lämplig dokumentation i koden.\n"
                    "3. Skriv enhetstester för att validera ändringarna.\n"
                    "4. Inför robust felhantering.\n\n"
                    "Ändringar: {changes}\nPåverkade filer: {files}"
                ),
                variables=["changes", "files"],
                description="Prompt för implementeringssteg med tydliga anvisningar",
                category="implementation"
            ),
            "test_prompt": PromptTemplate(
                name="test_prompt",
                content=(
                    "Skapa tester för de följande ändringarna:\n"
                    "1. Enhetstester för ny funktionalitet.\n"
                    "2. Integrationstester där det är nödvändigt.\n"
                    "3. Täckning av kantfall och felhantering.\n\n"
                    "Implementering: {implementation}\nFiler att testa: {files}"
                ),
                variables=["implementation", "files"],
                description="Prompt för teststeg med detaljerade krav",
                category="testing"
            )
        }
        # Lägg in defaults om de inte redan finns
        for key, prompt in defaults.items():
            if key not in self.templates:
                self.templates[key] = prompt

    def get_prompt(self, name: str, variables: Optional[Dict[str, Any]] = None) -> str:
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
        return [t for t in self.templates.values() if t.category == category]

    def get_template_variables(self, name: str) -> List[str]:
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found")
        return self.templates[name].variables.copy()
