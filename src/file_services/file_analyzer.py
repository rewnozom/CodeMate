from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import ast
import re
import json
import yaml  # Ensure PyYAML is installed

@dataclass
class FileMetadata:
    """File metadata information"""
    path: Path
    size: int
    created: datetime
    modified: datetime
    type: str
    encoding: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CodeAnalysis:
    """Analysis of code structure"""
    imports: List[str]
    classes: List[str]
    functions: List[str]
    dependencies: List[str]
    complexity: int
    issues: List[str]
    metadata: Dict[str, Any]

@dataclass
class FileAnalysis:
    """Complete file analysis report"""
    path: Path
    size: int
    created: datetime
    modified: datetime
    file_type: str
    encoding: str
    line_count: int
    code_analysis: Optional[CodeAnalysis] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class FileAnalyzer:
    """
    Analyzes file content and structure.
    
    Supports multiple file types (Python, JavaScript, HTML, CSS, JSON, YAML).
    """
    
    def __init__(self):
        self.analyzers = {
            ".py": self._analyze_python,
            ".js": self._analyze_javascript,
            ".html": self._analyze_html,
            ".css": self._analyze_css,
            ".json": self._analyze_json,
            ".yaml": self._analyze_yaml,
            ".yml": self._analyze_yaml
        }
        self.encoding_detectors = ["utf-8", "latin-1", "cp1252"]

    async def analyze_file(self, file_path: Union[str, Path]) -> FileAnalysis:
        """Analyze a file's content and structure."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        stat = path.stat()
        file_type = path.suffix.lower()
        encoding = self._detect_encoding(path)
        try:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            line_count = len(content.splitlines())
            analyzer = self.analyzers.get(file_type)
            code_analysis = await analyzer(content) if analyzer else None
            return FileAnalysis(
                path=path,
                size=stat.st_size,
                created=datetime.fromtimestamp(stat.st_ctime),
                modified=datetime.fromtimestamp(stat.st_mtime),
                file_type=file_type,
                encoding=encoding,
                line_count=line_count,
                code_analysis=code_analysis,
                metadata={}
            )
        except Exception as e:
            raise RuntimeError(f"Analysis failed for {path}: {str(e)}")

    def _detect_encoding(self, path: Path) -> str:
        """Detect file encoding from a list of candidates."""
        for enc in self.encoding_detectors:
            try:
                with open(path, 'r', encoding=enc) as f:
                    f.read()
                return enc
            except UnicodeDecodeError:
                continue
        return "utf-8"  # Default encoding

    async def _analyze_python(self, content: str) -> CodeAnalysis:
        """Analyze Python code: imports, classes, functions, complexity, and issues."""
        imports = []
        classes = []
        functions = []
        dependencies = []
        issues = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(name.name for name in node.names)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.extend(f"{node.module}.{name.name}" for name in node.names)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            functions.append(f"{node.name}.{item.name}")
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
            complexity = self._calculate_complexity(tree)
            issues.extend(self._check_python_issues(tree))
        except SyntaxError as e:
            issues.append(f"Syntax error: {str(e)}")
        return CodeAnalysis(
            imports=list(set(imports)),
            classes=classes,
            functions=functions,
            dependencies=dependencies,
            complexity=complexity,
            issues=issues,
            metadata={}
        )

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate a simple complexity metric for Python code."""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.ExceptHandler)):
                complexity += 1
        return complexity

    def _check_python_issues(self, tree: ast.AST) -> List[str]:
        """Check for common Python code issues."""
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append("Bare except found; consider catching specific exceptions")
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        issues.append(f"Mutable default argument in function {node.name}")
        return issues

    async def _analyze_javascript(self, content: str) -> CodeAnalysis:
        """Analyze JavaScript code."""
        import_pattern = r'(?:import|require)\s*\(?[\'"](.*?)[\'"]'
        func_pattern = r'(?:function|const|let|var)\s+(\w+)\s*(?:=)?\s*(?:function)?\s*\('
        imports = re.findall(import_pattern, content)
        functions = re.findall(func_pattern, content)
        classes = re.findall(r'class\s+(\w+)', content)
        complexity = 1
        for pattern in [r'\bif\b', r'\bfor\b', r'\bwhile\b', r'\bswitch\b', r'\bcatch\b']:
            complexity += len(re.findall(pattern, content))
        issues = []
        if 'eval(' in content:
            issues.append("Use of eval() detected")
        return CodeAnalysis(
            imports=imports,
            classes=classes,
            functions=functions,
            dependencies=[],
            complexity=complexity,
            issues=issues,
            metadata={}
        )

    async def _analyze_html(self, content: str) -> CodeAnalysis:
        """Analyze HTML content by extracting dependencies."""
        script_pattern = r'<script[^>]*src=[\'"]([^\'"]+)[\'"]'
        style_pattern = r'<link[^>]*href=[\'"]([^\'"]+)[\'"]'
        dependencies = re.findall(script_pattern, content) + re.findall(style_pattern, content)
        issues = []
        if 'onclick=' in content:
            issues.append("Inline JavaScript events found")
        if 'style=' in content:
            issues.append("Inline styles found")
        return CodeAnalysis(
            imports=[],
            classes=[],
            functions=[],
            dependencies=list(set(dependencies)),
            complexity=0,
            issues=issues,
            metadata={}
        )

    async def _analyze_css(self, content: str) -> CodeAnalysis:
        """Analyze CSS content by extracting selectors and properties."""
        selectors = {}
        current_selector = None
        for line in content.splitlines():
            line = line.strip()
            if line.endswith('{'):
                current_selector = line[:-1].strip()
                selectors[current_selector] = []
            elif line.endswith('}'):
                current_selector = None
            elif current_selector and ':' in line:
                prop = line.split(':', 1)[0].strip()
                selectors[current_selector].append(prop)
        issues = []
        if '!important' in content:
            issues.append("Use of !important found")
        return CodeAnalysis(
            imports=[],
            classes=[],
            functions=[],
            dependencies=[],
            complexity=0,
            issues=issues,
            metadata={"selectors": selectors}
        )

    async def _analyze_json(self, content: str) -> CodeAnalysis:
        """Analyze JSON content."""
        issues = []
        try:
            data = json.loads(content)
            metadata = {"keys": list(data.keys()) if isinstance(data, dict) else None}
        except Exception as e:
            issues.append(f"JSON parse error: {str(e)}")
            metadata = {}
        return CodeAnalysis(
            imports=[],
            classes=[],
            functions=[],
            dependencies=[],
            complexity=0,
            issues=issues,
            metadata=metadata
        )

    async def _analyze_yaml(self, content: str) -> CodeAnalysis:
        """Analyze YAML content."""
        issues = []
        try:
            data = yaml.safe_load(content)
            metadata = {"keys": list(data.keys()) if isinstance(data, dict) else None}
        except Exception as e:
            issues.append(f"YAML parse error: {str(e)}")
            metadata = {}
        return CodeAnalysis(
            imports=[],
            classes=[],
            functions=[],
            dependencies=[],
            complexity=0,
            issues=issues,
            metadata=metadata
        )
