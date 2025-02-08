from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import re
import ast

@dataclass
class UIComponent:
    """UI component information"""
    name: str
    type: str
    properties: Dict[str, Any]
    children: List['UIComponent']
    events: List[str]
    metadata: Dict[str, Any]

@dataclass
class ValidationIssue:
    """Validation issue details"""
    level: str  # "error", "warning", or "info"
    message: str
    location: str
    suggestion: Optional[str] = None

@dataclass
class FrontendValidationResult:
    """Result of frontend validation"""
    valid: bool
    components: List[UIComponent] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class FrontendValidator:
    """Validates frontend implementation for various file types."""
    
    def __init__(self):
        self.validators = {
            ".py": self._validate_pyside6,
            ".ui": self._validate_ui_file,
            ".qss": self._validate_stylesheet,
            ".qrc": self._validate_resources
        }

    async def validate_file(self, file_path: Union[str, Path]) -> FrontendValidationResult:
        """Validate a frontend file based on its extension."""
        path = Path(file_path)
        validator = self.validators.get(path.suffix.lower())
        if not validator:
            return FrontendValidationResult(
                valid=False,
                errors=[f"Unsupported file type: {path.suffix}"],
                metadata={"file": str(path)}
            )
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return await validator(content, path)
        except Exception as e:
            return FrontendValidationResult(
                valid=False,
                errors=[f"Validation error: {str(e)}"],
                metadata={"file": str(path)}
            )

    async def _validate_pyside6(self, content: str, path: Path) -> FrontendValidationResult:
        """Validate PySide6 Python UI code."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        components: List[UIComponent] = []
        
        if not re.search(r'from\s+PySide6', content):
            errors.append("Missing PySide6 import")
        if not re.search(r'class\s+\w+\s*\(\s*(?:QMainWindow|QWidget|QDialog)\s*\)', content):
            warnings.append("No Qt window class found")
        if 'setupUi' not in content:
            warnings.append("No setupUi method found")
        if not re.search(r'\.connect\(', content):
            warnings.append("No signal connections found")
        
        # Extract components by parsing the code
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    comps = self._extract_components_from_class(node)
                    components.extend(comps)
        except Exception as e:
            errors.append(f"Error parsing UI code: {str(e)}")
        
        valid = len(errors) == 0
        return FrontendValidationResult(
            valid=valid,
            components=components,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    def _extract_components_from_class(self, node: ast.ClassDef) -> List[UIComponent]:
        """Extract UI components from a class definition."""
        components = []
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and isinstance(item.value, ast.Call):
                        if isinstance(item.value.func, ast.Name) and item.value.func.id.startswith('Q'):
                            comp = UIComponent(
                                name=target.id,
                                type=item.value.func.id,
                                properties=self._extract_properties(item.value),
                                children=[],
                                events=self._extract_events(target.id, node),
                                metadata={}
                            )
                            components.append(comp)
        return components

    def _extract_properties(self, node: ast.Call) -> Dict[str, Any]:
        """Extract properties from a widget initialization call."""
        properties = {}
        for keyword in node.keywords:
            try:
                # Use literal evaluation if possible
                properties[keyword.arg] = ast.literal_eval(keyword.value)
            except Exception:
                properties[keyword.arg] = None
        return properties

    def _extract_events(self, component_name: str, class_node: ast.ClassDef) -> List[str]:
        """Extract event names associated with a component."""
        events = []
        for node in ast.walk(class_node):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                # Look for patterns like object.clicked.connect(...)
                attr = node.func
                if hasattr(attr.value, 'id') and attr.value.id == component_name:
                    if attr.attr in ['clicked', 'triggered', 'valueChanged', 'textChanged']:
                        events.append(attr.attr)
        return events

    async def _validate_ui_file(self, content: str, path: Path) -> FrontendValidationResult:
        """Validate a Qt UI file (XML)."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        components: List[UIComponent] = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(content)
            main_widget = root.find('.//widget')
            if main_widget is None or main_widget.get('class') not in ['QMainWindow', 'QWidget', 'QDialog']:
                errors.append("Missing or invalid main widget")
            for widget in root.findall('.//widget'):
                widget_class = widget.get('class')
                widget_name = widget.get('name')
                if not widget_name:
                    warnings.append(f"Widget of type {widget_class} missing name")
                    continue
                comp = UIComponent(
                    name=widget_name,
                    type=widget_class,
                    properties=self._extract_ui_properties(widget),
                    children=self._extract_ui_children(widget),
                    events=[],  # UI files typically do not include event connections
                    metadata={}
                )
                components.append(comp)
            if not root.findall('.//layout'):
                warnings.append("No layouts found in UI file")
        except Exception as e:
            errors.append(f"Invalid UI file: {str(e)}")
        valid = len(errors) == 0
        return FrontendValidationResult(
            valid=valid,
            components=components,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    def _extract_ui_properties(self, widget: Any) -> Dict[str, Any]:
        """Extract properties from a UI widget XML element."""
        properties = {}
        for prop in widget.findall('./property'):
            prop_name = prop.get('name')
            if prop_name:
                value_elem = prop.find('./string')
                if value_elem is not None:
                    properties[prop_name] = value_elem.text
        return properties

    def _extract_ui_children(self, widget: Any) -> List[UIComponent]:
        """Extract child components from a UI widget XML element."""
        children = []
        for child in widget.findall('./widget'):
            widget_class = child.get('class')
            widget_name = child.get('name')
            if widget_name:
                child_comp = UIComponent(
                    name=widget_name,
                    type=widget_class,
                    properties=self._extract_ui_properties(child),
                    children=self._extract_ui_children(child),
                    events=[],
                    metadata={}
                )
                children.append(child_comp)
        return children

    async def _validate_stylesheet(self, content: str, path: Path) -> FrontendValidationResult:
        """Validate a Qt stylesheet (.qss)."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        for i, line in enumerate(content.splitlines(), 1):
            line = line.strip()
            if line and '{' in line and not line.endswith('{'):
                errors.append(f"Invalid selector syntax at line {i}: Selector should end with '{{'")
            if ':' in line and ';' not in line:
                errors.append(f"Missing semicolon after property at line {i}")
        if content.count('{') != content.count('}'):
            errors.append("Unmatched braces in stylesheet")
        if re.search(r'-webkit-|-moz-|-ms-|-o-', content):
            warnings.append("Vendor prefixes found; consider using standard properties")
        valid = len(errors) == 0
        return FrontendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    async def _validate_resources(self, content: str, path: Path) -> FrontendValidationResult:
        """Validate a Qt resource file (.qrc)."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        if not content.strip().startswith('<!DOCTYPE RCC>'):
            errors.append("Invalid resource file format")
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(content)
            resource_paths = [file_elem.text for file_elem in root.findall('.//file') if file_elem.text]
            for res in resource_paths:
                res_file = path.parent / res
                if not res_file.exists():
                    errors.append(f"Resource file not found: {res}")
        except Exception as e:
            errors.append(f"Error parsing resource file: {str(e)}")
        valid = len(errors) == 0
        return FrontendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )
