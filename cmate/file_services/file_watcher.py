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
            r".*\.pyc"
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
