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