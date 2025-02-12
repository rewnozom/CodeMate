# cmate/file_services/workspace_analyzer.py

from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .workspace_scanner import WorkspaceScanner
from .file_analyzer import FileAnalyzer

class WorkspaceAnalyzer:
    """
    Analyzes the workspace specifically for a given request.
    - Identifies relevant files based on request keywords.
    - Classifies components (e.g. FRONTEND, BACKEND, TEST, CONFIGURATION).
    - Identifies file dependencies.
    """
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.scanner = WorkspaceScanner(str(self.workspace_path))
        self.file_analyzer = FileAnalyzer()

    async def analyze_for_request(self, request: str, workspace_path: Path) -> Dict[str, Any]:
        """
        Analyze the workspace based on the user's request.
        
        Returns a dictionary containing:
          - A list of relevant file paths.
          - A mapping of file paths to their classified component type.
          - A mapping of file paths to their dependencies.
        """
        scan_result = await self.scanner.scan_workspace()
        relevant_files = []
        classifications = {}
        dependencies = {}

        for file_info in scan_result.files:
            # A simple heuristic: consider the file relevant if any keyword from the request appears in the file name.
            if any(keyword in file_info.path.name.lower() for keyword in request.lower().split()):
                relevant_files.append(file_info.path)
                component_type = await self.identify_component_type(file_info.path)
                classifications[str(file_info.path)] = component_type
                deps = await self.get_dependencies(file_info.path)
                dependencies[str(file_info.path)] = [str(dep) for dep in deps]

        return {
            "relevant_files": [str(p) for p in relevant_files],
            "classifications": classifications,
            "dependencies": dependencies,
            "scan_timestamp": datetime.now().isoformat()
        }

    async def identify_component_type(self, file_path: Path) -> str:
        """
        Identify the component type of the given file.
        Returns one of: "FRONTEND", "BACKEND", "TEST", "CONFIGURATION", or "UNKNOWN".
        """
        suffix = file_path.suffix.lower()
        if suffix in [".html", ".css", ".js"]:
            return "FRONTEND"
        elif suffix == ".py":
            # If the filename contains "test", classify it as a test file.
            if "test" in file_path.name.lower():
                return "TEST"
            return "BACKEND"
        elif suffix in [".json", ".yaml", ".yml"]:
            return "CONFIGURATION"
        return "UNKNOWN"

    async def get_dependencies(self, file_path: Path) -> List[Path]:
        """
        Identify dependencies for the given file.
        For Python files, this can use the imports list from the FileAnalyzer.
        For other file types, additional logic can be added.
        """
        analysis = await self.file_analyzer.analyze_file(file_path)
        if file_path.suffix.lower() == ".py" and analysis.code_analysis:
            # Return dependencies as a list of (possibly unresolved) import names.
            return [Path(imp) for imp in analysis.code_analysis.imports]
        return []
