# Project Details

# Table of Contents
- [..\cmate\file_services\file_analyzer.py](#-cmate-file_services-file_analyzerpy)
- [..\cmate\file_services\file_watcher.py](#-cmate-file_services-file_watcherpy)
- [..\cmate\file_services\workspace_scanner.py](#-cmate-file_services-workspace_scannerpy)
- [..\cmate\file_services\__init__.py](#-cmate-file_services-__init__py)


# ..\..\cmate\file_services\file_analyzer.py
## File: ..\..\cmate\file_services\file_analyzer.py

```py
# ..\..\cmate\file_services\file_analyzer.py
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

```

---

# ..\..\cmate\file_services\file_watcher.py
## File: ..\..\cmate\file_services\file_watcher.py

```py
# ..\..\cmate\file_services\file_watcher.py
# src/file_services/file_watcher.py
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

@dataclass
class FileChange:
    """Record of file change"""
    path: Path
    event_type: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

class FileWatcher(FileSystemEventHandler):
    """Watches for file system changes"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        super().__init__()
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.observer = Observer()
        self.changes: List[FileChange] = []
        self.handlers: Dict[str, List[Callable]] = {
            "created": [],
            "modified": [],
            "deleted": [],
            "moved": []
        }
        self.watch_patterns: List[str] = []
        self.ignore_patterns: List[str] = [
            r'__pycache__',
            r'\.git',
            r'\.pytest_cache',
            r'*.pyc'
        ]
        self._is_running = False

    async def start_watching(self) -> None:
        """Start watching for changes"""
        if self._is_running:
            return
            
        self._is_running = True
        self.observer.schedule(self, str(self.workspace), recursive=True)
        self.observer.start()

    async def stop_watching(self) -> None:
        """Stop watching for changes"""
        if not self._is_running:
            return
            
        self._is_running = False
        self.observer.stop()
        self.observer.join()

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation event"""
        if not self._should_handle_event(event):
            return
            
        change = FileChange(
            path=Path(event.src_path).relative_to(self.workspace),
            event_type="created",
            timestamp=datetime.now()
        )
        self.changes.append(change)
        
        for handler in self.handlers["created"]:
            asyncio.create_task(handler(change))

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification event"""
        if not self._should_handle_event(event):
            return
            
        change = FileChange(
            path=Path(event.src_path).relative_to(self.workspace),
            event_type="modified",
            timestamp=datetime.now()
        )
        self.changes.append(change)
        
        for handler in self.handlers["modified"]:
            asyncio.create_task(handler(change))

    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file deletion event"""
        if not self._should_handle_event(event):
            return
            
        change = FileChange(
            path=Path(event.src_path).relative_to(self.workspace),
            event_type="deleted",
            timestamp=datetime.now()
        )
        self.changes.append(change)
        
        for handler in self.handlers["deleted"]:
            asyncio.create_task(handler(change))

    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move event"""
        if not self._should_handle_event(event):
            return
            
        change = FileChange(
            path=Path(event.dest_path).relative_to(self.workspace),
            event_type="moved",
            timestamp=datetime.now(),
            details={
                "source_path": str(Path(event.src_path).relative_to(self.workspace))
            }
        )
        self.changes.append(change)
        
        for handler in self.handlers["moved"]:
            asyncio.create_task(handler(change))

    def add_handler(self, event_type: str, handler: Callable) -> None:
        """Add event handler"""
        if event_type not in self.handlers:
            raise ValueError(f"Invalid event type: {event_type}")
        self.handlers[event_type].append(handler)

    def remove_handler(self, event_type: str, handler: Callable) -> None:
        """Remove event handler"""
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)

    def add_watch_pattern(self, pattern: str) -> None:
        """Add pattern to watch"""
        self.watch_patterns.append(pattern)

    def add_ignore_pattern(self, pattern: str) -> None:
        """Add pattern to ignore"""
        self.ignore_patterns.append(pattern)

    def get_changes(self, 
                   limit: Optional[int] = None,
                   event_type: Optional[str] = None) -> List[FileChange]:
        """Get recorded changes"""
        changes = self.changes
        if event_type:
            changes = [c for c in changes if c.event_type == event_type]
        if limit:
            changes = changes[-limit:]
        return changes

    def clear_changes(self) -> None:
        """Clear recorded changes"""
        self.changes.clear()

    def _should_handle_event(self, event: FileSystemEvent) -> bool:
        """Check if event should be handled"""
        path = Path(event.src_path)
        
        # Check ignore patterns
        if any(path.match(pattern) for pattern in self.ignore_patterns):
            return False
            
        # Check watch patterns
        if self.watch_patterns:
            return any(path.match(pattern) for pattern in self.watch_patterns)
            
        return True

    async def get_recent_changes(self, 
                               seconds: int = 60,
                               event_type: Optional[str] = None) -> List[FileChange]:
        """Get changes from last n seconds"""
        now = datetime.now()
        changes = [
            change for change in self.changes
            if (now - change.timestamp).total_seconds() <= seconds
            and (not event_type or change.event_type == event_type)
        ]
        return changes
```

---

# ..\..\cmate\file_services\workspace_scanner.py
## File: ..\..\cmate\file_services\workspace_scanner.py

```py
# ..\..\cmate\file_services\workspace_scanner.py
# src/file_services/workspace_scanner.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import re
import asyncio

@dataclass
class FileInfo:
    """Information about a file"""
    path: Path
    size: int
    created: datetime
    modified: datetime
    file_type: str
    content_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ScanResult:
    """Result of workspace scan"""
    timestamp: datetime
    files: List[FileInfo]
    total_size: int
    file_types: Dict[str, int]
    metadata: Dict[str, Any]

class WorkspaceScanner:
    """Scans workspace directory structure"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.ignored_patterns = [
            r'__pycache__',
            r'\.git',
            r'\.pytest_cache',
            r'\.venv',
            r'*.pyc',
            r'*.pyo'
        ]
        self.scan_history: List[ScanResult] = []

    async def scan_workspace(self, 
                           max_depth: Optional[int] = None,
                           file_types: Optional[List[str]] = None) -> ScanResult:
        """Scan workspace directory"""
        files = []
        total_size = 0
        file_types_count = {}
        
        try:
            for file_path in self._scan_files(max_depth, file_types):
                try:
                    stat = file_path.stat()
                    file_type = file_path.suffix.lower()[1:] if file_path.suffix else "unknown"
                    
                    # Update statistics
                    total_size += stat.st_size
                    file_types_count[file_type] = file_types_count.get(file_type, 0) + 1
                    
                    # Create file info
                    file_info = FileInfo(
                        path=file_path.relative_to(self.workspace),
                        size=stat.st_size,
                        created=datetime.fromtimestamp(stat.st_ctime),
                        modified=datetime.fromtimestamp(stat.st_mtime),
                        file_type=file_type,
                        content_type=self._get_content_type(file_path)
                    )
                    
                    files.append(file_info)
                    
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
                    
            result = ScanResult(
                timestamp=datetime.now(),
                files=files,
                total_size=total_size,
                file_types=file_types_count,
                metadata={
                    "workspace": str(self.workspace),
                    "max_depth": max_depth,
                    "file_types": file_types
                }
            )
            
            self.scan_history.append(result)
            return result
            
        except Exception as e:
            raise RuntimeError(f"Workspace scan failed: {str(e)}")

    def _scan_files(self, max_depth: Optional[int], file_types: Optional[List[str]]) -> List[Path]:
        """Generator for scanning files"""
        def should_ignore(path: Path) -> bool:
            return any(re.match(pattern, str(path)) for pattern in self.ignored_patterns)
            
        def scan_directory(path: Path, current_depth: int) -> List[Path]:
            if max_depth and current_depth > max_depth:
                return []
                
            files = []
            try:
                for item in path.iterdir():
                    if should_ignore(item):
                        continue
                        
                    if item.is_file():
                        if not file_types or (item.suffix and item.suffix[1:].lower() in file_types):
                            files.append(item)
                    elif item.is_dir():
                        files.extend(scan_directory(item, current_depth + 1))
            except Exception as e:
                print(f"Error scanning directory {path}: {str(e)}")
                
            return files
            
        return scan_directory(self.workspace, 0)

    def _get_content_type(self, file_path: Path) -> Optional[str]:
        """Determine content type of file"""
        content_types = {
            ".txt": "text/plain",
            ".py": "text/x-python",
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".xml": "application/xml",
            ".yaml": "application/x-yaml",
            ".yml": "application/x-yaml"
        }
        return content_types.get(file_path.suffix.lower())
```

---

# ..\..\cmate\file_services\__init__.py
## File: ..\..\cmate\file_services\__init__.py

```py
# ..\..\cmate\file_services\__init__.py
# Auto-generated __init__.py file

```

---

