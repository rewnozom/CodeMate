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
