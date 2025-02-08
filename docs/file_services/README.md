# docs/file_services/README.md
# File Services Documentation

## Overview
File services handle all file system interactions and code analysis.

### Components
- file_system_navigator.py
- file_analyzer.py
- workspace_scanner.py
- file_watcher.py

## Usage Examples

### FileAnalyzer
```python
from file_services.file_analyzer import FileAnalyzer

analyzer = FileAnalyzer()
result = await analyzer.analyze_file("path/to/file.py")
```

### WorkspaceScanner
```python
from file_services.workspace_scanner import WorkspaceScanner

scanner = WorkspaceScanner()
files = await scanner.scan_workspace(max_depth=2)
```

[More file service details...](./services.md)
