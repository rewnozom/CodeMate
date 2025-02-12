# Project Details

# Table of Contents
- [..\CodeMate\cmate\validation\__init__.py](#-CodeMate-cmate-validation-__init__py)
- [..\CodeMate\cmate\validation\backend_validator.py](#-CodeMate-cmate-validation-backend_validatorpy)
- [..\CodeMate\cmate\validation\frontend_validator.py](#-CodeMate-cmate-validation-frontend_validatorpy)
- [..\CodeMate\cmate\validation\implementation_validator.py](#-CodeMate-cmate-validation-implementation_validatorpy)
- [..\CodeMate\cmate\validation\test_manager.py](#-CodeMate-cmate-validation-test_managerpy)
- [..\CodeMate\cmate\validation\validation_rules.py](#-CodeMate-cmate-validation-validation_rulespy)


# ..\..\CodeMate\cmate\validation\__init__.py
## File: ..\..\CodeMate\cmate\validation\__init__.py

```py
# ..\..\CodeMate\cmate\validation\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\cmate\validation\backend_validator.py
## File: ..\..\CodeMate\cmate\validation\backend_validator.py

```py
# ..\..\CodeMate\cmate\validation\backend_validator.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import ast
import json
import re
from pathlib import Path

@dataclass
class ValidationIssue:
    """Details of a validation issue."""
    level: str  # e.g. "error", "warning", "info"
    message: str
    location: str
    suggestion: Optional[str] = None

@dataclass
class CodeFunction:
    """Information about a function in the code."""
    name: str
    args: List[str]
    returns: Optional[str]
    docstring: Optional[str]
    complexity: int
    source: str

@dataclass
class CodeClass:
    """Information about a class in the code."""
    name: str
    bases: List[str]
    methods: List[CodeFunction]
    docstring: Optional[str]
    properties: List[str]

@dataclass
class BackendValidationResult:
    """Result of backend validation."""
    valid: bool
    functions: List[CodeFunction] = field(default_factory=list)
    classes: List[CodeClass] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    issues: List[ValidationIssue] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class BackendValidator:
    """Validates backend implementation for various file types."""
    
    def __init__(self):
        self.max_complexity = 10
        self.required_docstrings = True
        self.check_type_hints = True
        self.validators = {
            ".py": self._validate_python,
            ".json": self._validate_json,
            ".yaml": self._validate_yaml,
            ".yml": self._validate_yaml,
            ".sql": self._validate_sql
        }

    async def validate_file(self, file_path: Union[str, Path]) -> BackendValidationResult:
        """Validate a backend file based on its extension."""
        path = Path(file_path)
        validator = self.validators.get(path.suffix.lower())
        if not validator:
            return BackendValidationResult(
                valid=False,
                errors=[f"Unsupported file type: {path.suffix}"],
                metadata={"file": str(path)}
            )
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return await validator(content, path)
        except Exception as e:
            return BackendValidationResult(
                valid=False,
                errors=[f"Validation error: {str(e)}"],
                metadata={"file": str(path)}
            )

    async def _validate_python(self, content: str, path: Path) -> BackendValidationResult:
        """Validate Python backend code with structural and style checks."""
        issues: List[ValidationIssue] = []
        functions: List[CodeFunction] = []
        classes: List[CodeClass] = []
        imports: List[str] = []
        metrics = {"loc": len(content.splitlines()), "comments": len(re.findall(r'#.*$', content, re.MULTILINE))}
        
        try:
            tree = ast.parse(content)
            
            # Analyze imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for name in node.names:
                        imports.append(f"{module}.{name.name}")
            # Check duplicate imports
            dupes = {x for x in imports if imports.count(x) > 1}
            if dupes:
                issues.append(ValidationIssue(
                    level="warning",
                    message=f"Duplicate imports found: {dupes}",
                    location="imports",
                    suggestion="Remove duplicate imports"
                ))
            
            # Analyze functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    returns = self._get_type_name(node.returns) if node.returns else None
                    docstring = ast.get_docstring(node)
                    complexity = self._calculate_complexity(node)
                    func = CodeFunction(
                        name=node.name,
                        args=args,
                        returns=returns,
                        docstring=docstring,
                        complexity=complexity,
                        source=ast.unparse(node) if hasattr(ast, "unparse") else ""
                    )
                    functions.append(func)
                    # Validate function details
                    if complexity > self.max_complexity:
                        issues.append(ValidationIssue(
                            level="warning",
                            message=f"Function {node.name} has high complexity ({complexity})",
                            location=f"function {node.name}",
                            suggestion="Consider refactoring into smaller functions"
                        ))
                    if self.required_docstrings and not docstring:
                        issues.append(ValidationIssue(
                            level="warning",
                            message=f"Missing docstring in function {node.name}",
                            location=f"function {node.name}",
                            suggestion="Add a docstring describing the function's purpose and parameters"
                        ))
                    if self.check_type_hints and not returns:
                        issues.append(ValidationIssue(
                            level="info",
                            message=f"Missing return type hint in function {node.name}",
                            location=f"function {node.name}",
                            suggestion="Add return type hint"
                        ))
            
            # Analyze classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    bases = [self._get_type_name(base) for base in node.bases]
                    methods = []
                    properties = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            args = [arg.arg for arg in item.args.args]
                            ret = self._get_type_name(item.returns) if item.returns else None
                            doc = ast.get_docstring(item)
                            comp = self._calculate_complexity(item)
                            methods.append(CodeFunction(
                                name=item.name,
                                args=args,
                                returns=ret,
                                docstring=doc,
                                complexity=comp,
                                source=ast.unparse(item) if hasattr(ast, "unparse") else ""
                            ))
                        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            properties.append(item.target.id)
                    cls = CodeClass(
                        name=node.name,
                        bases=bases,
                        methods=methods,
                        docstring=ast.get_docstring(node),
                        properties=properties
                    )
                    classes.append(cls)
                    if self.required_docstrings and not cls.docstring:
                        issues.append(ValidationIssue(
                            level="warning",
                            message=f"Missing docstring in class {node.name}",
                            location=f"class {node.name}",
                            suggestion="Add a docstring describing the class's purpose"
                        ))
                    if not bases:
                        issues.append(ValidationIssue(
                            level="info",
                            message=f"Class {node.name} has no base classes",
                            location=f"class {node.name}",
                            suggestion="Consider whether inheritance is applicable"
                        ))
                    for method in methods:
                        if method.complexity > self.max_complexity:
                            issues.append(ValidationIssue(
                                level="warning",
                                message=f"Method {method.name} in class {node.name} has high complexity ({method.complexity})",
                                location=f"class {node.name}",
                                suggestion="Refactor the method into simpler sub-methods"
                            ))
            
            overall_complexity = sum(func.complexity for func in functions) + sum(
                sum(m.complexity for m in cls.methods) for cls in classes
            )
            metrics["complexity"] = overall_complexity
            
        except SyntaxError as e:
            issues.append(ValidationIssue(
                level="error",
                message=f"Syntax error: {str(e)}",
                location=f"line {e.lineno}",
                suggestion="Fix syntax errors"
            ))
        except Exception as e:
            issues.append(ValidationIssue(
                level="error",
                message=f"Validation error: {str(e)}",
                location="file",
                suggestion="Check the file for issues"
            ))
            
        valid = not any(issue.level == "error" for issue in issues)
        return BackendValidationResult(
            valid=valid,
            functions=functions,
            classes=classes,
            imports=imports,
            issues=issues,
            metrics=metrics,
            metadata={"file": str(path)}
        )

    def _get_type_name(self, node: Optional[ast.AST]) -> str:
        """Get string representation of a type annotation node."""
        if node is None:
            return ""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_type_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_type_name(node.value)}[{self._get_type_name(node.slice)}]"
        else:
            return str(node)

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate a simple cyclomatic complexity metric for a node."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    async def _validate_json(self, content: str, path: Path) -> BackendValidationResult:
        """Validate a JSON configuration file."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                required_fields = {"version", "description"}
                missing = required_fields - set(data.keys())
                if missing:
                    warnings.append(f"Missing recommended fields: {missing}")
            metadata["structure"] = {"type": type(data).__name__, "keys": list(data.keys()) if isinstance(data, dict) else None}
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {str(e)}")
        valid = len(errors) == 0
        return BackendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    async def _validate_yaml(self, content: str, path: Path) -> BackendValidationResult:
        """Validate a YAML configuration file."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        try:
            import yaml
            data = yaml.safe_load(content)
            if isinstance(data, dict):
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if line.strip() and line.startswith(' '):
                        indent = len(line) - len(line.lstrip())
                        if indent % 2 != 0:
                            warnings.append(f"Inconsistent indentation at line {i}")
                def check_empty(d, prefix=""):
                    for k, v in d.items():
                        if v is None:
                            warnings.append(f"Empty value for key: {prefix + str(k)}")
                        elif isinstance(v, dict):
                            check_empty(v, f"{prefix}{k}.")
                check_empty(data)
            metadata["structure"] = {"type": type(data).__name__, "keys": list(data.keys()) if isinstance(data, dict) else None}
        except Exception as e:
            errors.append(f"Invalid YAML: {str(e)}")
        valid = len(errors) == 0
        return BackendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    async def _validate_sql(self, content: str, path: Path) -> BackendValidationResult:
        """Validate an SQL file with basic syntax checks."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        statements = [stmt.strip() for stmt in content.split(';') if stmt.strip()]
        for i, stmt in enumerate(statements, 1):
            if not any(stmt.upper().startswith(keyword) for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']):
                warnings.append(f"Unknown SQL statement type at statement {i}")
            if 'SELECT *' in stmt.upper():
                warnings.append(f"Use of SELECT * found in statement {i}")
            if 'DROP TABLE' in stmt.upper() and 'IF EXISTS' not in stmt.upper():
                warnings.append(f"DROP TABLE without IF EXISTS in statement {i}")
            if 'CREATE TABLE' in stmt.upper() and 'IF NOT EXISTS' not in stmt.upper():
                warnings.append(f"CREATE TABLE without IF NOT EXISTS in statement {i}")
        metadata["statements_count"] = len(statements)
        valid = len(errors) == 0
        return BackendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

```

---

# ..\..\CodeMate\cmate\validation\frontend_validator.py
## File: ..\..\CodeMate\cmate\validation\frontend_validator.py

```py
# ..\..\CodeMate\cmate\validation\frontend_validator.py
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

```

---

# ..\..\CodeMate\cmate\validation\implementation_validator.py
## File: ..\..\CodeMate\cmate\validation\implementation_validator.py

```py
# ..\..\CodeMate\cmate\validation\implementation_validator.py
# src/validation/implementation_validator.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import ast
import re

@dataclass
class ValidationResult:
    """Result of code validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    metadata: Dict[str, Any]

class ImplementationValidator:
    """Validates code implementation against requirements"""
    
    def __init__(self):
        self.requirements: Dict[str, Any] = {}
        self.validation_rules: Dict[str, callable] = {}
        self._initialize_validators()

    def _initialize_validators(self) -> None:
        """Initialize validation rules"""
        self.validation_rules.update({
            'python': self._validate_python_code,
            'javascript': self._validate_javascript_code,
            'html': self._validate_html_code,
            'css': self._validate_css_code
        })

    async def validate_implementation(self,
                                   code: str,
                                   language: str,
                                   requirements: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate code implementation"""
        if requirements:
            self.requirements.update(requirements)
            
        validator = self.validation_rules.get(language.lower())
        if not validator:
            return ValidationResult(
                valid=False,
                errors=[f"Unsupported language: {language}"],
                warnings=[],
                suggestions=[],
                metadata={}
            )
            
        return await validator(code)

    async def _validate_python_code(self, code: str) -> ValidationResult:
        """Validate Python code"""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Parse code
            tree = ast.parse(code)
            
            # Check syntax
            compile(code, '<string>', 'exec')
            
            # Analyze structure
            for node in ast.walk(tree):
                # Check function definitions
                if isinstance(node, ast.FunctionDef):
                    if not node.returns:
                        warnings.append(f"Missing return type hint in function {node.name}")
                    if not ast.get_docstring(node):
                        warnings.append(f"Missing docstring in function {node.name}")
                
                # Check class definitions
                elif isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        warnings.append(f"Missing docstring in class {node.name}")
                
                # Check error handling
                elif isinstance(node, ast.Try):
                    if not any(isinstance(handler.type, ast.Name) for handler in node.handlers):
                        warnings.append("Generic exception handler found")
                
                # Check variable names
                elif isinstance(node, ast.Name):
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.id):
                        warnings.append(f"Variable name {node.id} does not follow PEP 8")
            
            # Check requirements
            if 'required_functions' in self.requirements:
                found_functions = {n.name for n in ast.walk(tree) 
                                 if isinstance(n, ast.FunctionDef)}
                missing = set(self.requirements['required_functions']) - found_functions
                if missing:
                    errors.append(f"Missing required functions: {missing}")
            
        except SyntaxError as e:
            errors.append(f"Syntax error: {str(e)}")
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={
                "language": "python",
                "ast_nodes": len(list(ast.walk(tree))) if 'tree' in locals() else 0
            }
        )

    async def _validate_javascript_code(self, code: str) -> ValidationResult:
        """Validate JavaScript code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check basic syntax
        if code.count('{') != code.count('}'):
            errors.append("Mismatched curly braces")
            
        # Check for common issues
        if 'eval(' in code:
            warnings.append("Use of eval() detected")
        if 'with(' in code:
            warnings.append("Use of with statement detected")
            
        # Check semicolons
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.endswith('{') and not line.endswith('}') and \
               not line.endswith(';') and not line.startswith('//'):
                warnings.append(f"Missing semicolon on line {i}")
                
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "javascript"}
        )

    async def _validate_html_code(self, code: str) -> ValidationResult:
        """Validate HTML code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for unclosed tags
        tag_stack = []
        for match in re.finditer(r'</?(\w+)[^>]*>', code):
            tag = match.group(1)
            if match.group(0).startswith('</'):
                if not tag_stack or tag_stack[-1] != tag:
                    errors.append(f"Mismatched closing tag: {tag}")
                else:
                    tag_stack.pop()
            elif not match.group(0).endswith('/>'):
                tag_stack.append(tag)
                
        if tag_stack:
            errors.append(f"Unclosed tags: {', '.join(tag_stack)}")
            
        # Check for accessibility
        for match in re.finditer(r'<img[^>]*>', code):
            if 'alt=' not in match.group(0):
                warnings.append("Image missing alt attribute")
                
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "html"}
        )

    async def _validate_css_code(self, code: str) -> ValidationResult:
        """Validate CSS code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for unclosed blocks
        if code.count('{') != code.count('}'):
            errors.append("Mismatched curly braces")
            
        # Check for vendor prefixes
        vendor_prefixes = ['-webkit-', '-moz-', '-ms-', '-o-']
        for prefix in vendor_prefixes:
            if prefix in code:
                suggestions.append(f"Consider using autoprefixer for {prefix} properties")
                
        # Check for !important
        if '!important' in code:
            warnings.append("Use of !important found - consider refactoring")
            
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "css"}
        )

```

---

# ..\..\CodeMate\cmate\validation\test_manager.py
## File: ..\..\CodeMate\cmate\validation\test_manager.py

```py
# ..\..\CodeMate\cmate\validation\test_manager.py
# src/validation/test_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import subprocess
from pathlib import Path
import re
from uuid import UUID, uuid4

@dataclass
class TestCase:
    """Individual test case"""
    id: UUID
    name: str
    description: str
    test_file: Path
    test_type: str  # unit, integration, e2e
    dependencies: List[str]
    timeout: int = 30
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    last_result: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestResult:
    """Result of test execution"""
    test_id: UUID
    success: bool
    output: str
    error: Optional[str]
    duration: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class TestManager:
    """Manages test execution and results"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.test_cases: Dict[UUID, TestCase] = {}
        self.test_results: Dict[UUID, List[TestResult]] = {}
        self.active_tests: Dict[UUID, asyncio.Task] = {}
        
    async def add_test_case(self, 
                          name: str,
                          description: str,
                          test_file: Union[str, Path],
                          test_type: str,
                          dependencies: List[str] = None,
                          metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Add new test case"""
        test_id = uuid4()
        test_file = Path(test_file)
        
        if not test_file.exists():
            raise FileNotFoundError(f"Test file not found: {test_file}")
        
        self.test_cases[test_id] = TestCase(
            id=test_id,
            name=name,
            description=description,
            test_file=test_file,
            test_type=test_type,
            dependencies=dependencies or [],
            metadata=metadata or {}
        )
        
        return test_id

    async def run_test(self, test_id: UUID) -> TestResult:
        """Run specific test case"""
        if test_id not in self.test_cases:
            raise ValueError(f"Test case not found: {test_id}")
            
        test_case = self.test_cases[test_id]
        start_time = datetime.now()
        
        try:
            # Check dependencies
            for dep in test_case.dependencies:
                if not await self._check_dependency(dep):
                    raise RuntimeError(f"Dependency not met: {dep}")
            
            # Run test
            process = await asyncio.create_subprocess_exec(
                "python", "-m", "pytest", str(test_case.test_file),
                "-v", "--capture=sys",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace)
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=test_case.timeout
                )
                
                success = process.returncode == 0
                output = stdout.decode()
                error = stderr.decode() if stderr else None
                
            except asyncio.TimeoutError:
                success = False
                output = "Test timed out"
                error = f"Test exceeded timeout of {test_case.timeout} seconds"
                
            duration = (datetime.now() - start_time).total_seconds()
            
            # Create result
            result = TestResult(
                test_id=test_id,
                success=success,
                output=output,
                error=error,
                duration=duration,
                timestamp=datetime.now()
            )
            
            # Update test case
            test_case.last_run = datetime.now()
            test_case.last_result = success
            
            # Store result
            if test_id not in self.test_results:
                self.test_results[test_id] = []
            self.test_results[test_id].append(result)
            
            return result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            result = TestResult(
                test_id=test_id,
                success=False,
                output="",
                error=str(e),
                duration=duration,
                timestamp=datetime.now()
            )
            
            if test_id not in self.test_results:
                self.test_results[test_id] = []
            self.test_results[test_id].append(result)
            
            return result

    async def run_all_tests(self, test_type: Optional[str] = None) -> Dict[UUID, TestResult]:
        """Run all test cases of specified type"""
        results = {}
        test_cases = [
            tc for tc in self.test_cases.values()
            if not test_type or tc.test_type == test_type
        ]
        
        for test_case in test_cases:
            results[test_case.id] = await self.run_test(test_case.id)
            
        return results

    async def get_test_history(self, 
                            test_id: UUID,
                            limit: Optional[int] = None) -> List[TestResult]:
        """Get test execution history"""
        if test_id not in self.test_results:
            return []
            
        results = self.test_results[test_id]
        if limit:
            results = results[-limit:]
            
        return results

    async def analyze_results(self, results: Dict[UUID, TestResult]) -> Dict[str, Any]:
        """Analyze test results"""
        total_tests = len(results)
        passed_tests = len([r for r in results.values() if r.success])
        failed_tests = total_tests - passed_tests
        
        total_duration = sum(r.duration for r in results.values())
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_duration,
            "average_duration": avg_duration,
            "failed_test_ids": [
                test_id for test_id, result in results.items()
                if not result.success
            ]
        }

    async def _check_dependency(self, dependency: str) -> bool:
        """Check if dependency is satisfied"""
        if dependency.startswith("test:"):
            # Check test dependency
            test_name = dependency[5:]
            for test in self.test_cases.values():
                if test.name == test_name:
                    return test.last_result is True
        elif dependency.startswith("file:"):
            # Check file dependency
            file_path = self.workspace / dependency[5:]
            return file_path.exists()
        return False
```

---

# ..\..\CodeMate\cmate\validation\validation_rules.py
## File: ..\..\CodeMate\cmate\validation\validation_rules.py

```py
# ..\..\CodeMate\cmate\validation\validation_rules.py
# cmate/validation/validation_rules.py
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
import re
from enum import Enum

# Updated enum values: use numeric values for ordering.
class ValidationLevel(Enum):
    STRICT = 1
    NORMAL = 2
    LENIENT = 3

@dataclass
class ValidationRule:
    """Individual validation rule"""
    name: str
    description: str
    validator: Callable
    level: ValidationLevel
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """Result of validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]

class ValidationRules:
    """Manages and applies validation rules"""
    
    def __init__(self, level: ValidationLevel = ValidationLevel.NORMAL):
        self.level = level
        self.rules: Dict[str, ValidationRule] = {}
        self._initialize_rules()

    def _initialize_rules(self) -> None:
        """Initialize default validation rules"""
        # Setup basic rules
        self.add_rule(
            "valid_path",
            "Validate file path format",
            self._validate_path,
            ValidationLevel.STRICT
        )
        
        self.add_rule(
            "code_syntax",
            "Validate Python code syntax",
            self._validate_code_syntax,
            ValidationLevel.STRICT
        )
        
        self.add_rule(
            "function_name",
            "Validate function naming convention",
            self._validate_function_name,
            ValidationLevel.NORMAL
        )
        
        self.add_rule(
            "variable_name",
            "Validate variable naming convention",
            self._validate_variable_name,
            ValidationLevel.NORMAL
        )

    def add_rule(self,
                name: str,
                description: str,
                validator: Callable,
                level: ValidationLevel) -> None:
        """Add new validation rule"""
        self.rules[name] = ValidationRule(
            name=name,
            description=description,
            validator=validator,
            level=level
        )

    def validate(self, content: Any, rule_names: Optional[List[str]] = None) -> ValidationResult:
        """Validate content against rules"""
        errors = []
        warnings = []
        metadata = {}
        
        rules_to_apply = []
        if rule_names:
            rules_to_apply = [r for n, r in self.rules.items() if n in rule_names and r.enabled]
        else:
            rules_to_apply = [r for r in self.rules.values() if r.enabled]
        
        for rule in rules_to_apply:
            try:
                if rule.level.value <= self.level.value:
                    result = rule.validator(content)
                    if isinstance(result, dict):
                        if not result.get("valid", False):
                            if rule.level == ValidationLevel.STRICT:
                                errors.extend(result.get("errors", []))
                            else:
                                warnings.extend(result.get("errors", []))
                        metadata[rule.name] = result.get("metadata", {})
            except Exception as e:
                errors.append(f"Rule '{rule.name}' failed: {str(e)}")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    def _validate_path(self, path: str) -> Dict[str, Any]:
        """Validate file path"""
        if not isinstance(path, str):
            return {"valid": False, "errors": ["Path must be a string"]}
            
        if ".." in path:
            return {"valid": False, "errors": ["Path cannot contain parent directory references"]}
            
        if not path.startswith("./Workspace"):
            return {"valid": False, "errors": ["Path must be within Workspace directory"]}
            
        return {"valid": True, "metadata": {"path": path}}

    def _validate_code_syntax(self, code: str) -> Dict[str, Any]:
        """Validate Python code syntax"""
        try:
            compile(code, "<string>", "exec")
            return {"valid": True}
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [f"Syntax error: {str(e)}"],
                "metadata": {"line": e.lineno, "offset": e.offset}
            }

    def _validate_function_name(self, name: str) -> Dict[str, Any]:
        """Validate function naming convention"""
        if not re.match(r'^[a-z_][a-z0-9_]*$', name):
            return {
                "valid": False,
                "errors": ["Function name must be lowercase with underscores"]
            }
        return {"valid": True}

    def _validate_variable_name(self, name: str) -> Dict[str, Any]:
        """Validate variable naming convention"""
        if not re.match(r'^[a-z_][a-z0-9_]*$', name):
            return {
                "valid": False,
                "errors": ["Variable name must be lowercase with underscores"]
            }
        return {"valid": True}

```

---

