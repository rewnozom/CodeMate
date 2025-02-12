# ..\..\cmate\core\navigation_executor.py
"""
cmate/core/navigation_executor.py

Handles execution of navigation actions including:
- File creation and modification
- Directory structure management
- Safe file operations with backup/rollback
- Multi-file operations
"""

import shutil
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from uuid import UUID, uuid4
import logging

from ..utils.error_handler import ErrorHandler
from ..core.dependency_analyzer import ComponentDependencyAnalyzer
from ..file_services.file_analyzer import FileAnalyzer

logger = logging.getLogger(__name__)
logger.success("NavigationActionExecutor module loaded successfully.")

class NavigationActionType(Enum):
    """Types of navigation actions"""
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
    MOVE = "move"
    BACKUP = "backup"
    RESTORE = "restore"

@dataclass
class NavigationAction:
    """Represents a navigation action to be executed"""
    id: UUID
    action_type: NavigationActionType
    source_path: Path
    target_path: Optional[Path] = None
    content: Optional[str] = None
    backup_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ActionResult:
    """Result of an executed navigation action"""
    action_id: UUID
    success: bool
    source_path: Path
    target_path: Optional[Path]
    backup_created: bool
    error: Optional[str] = None
    changes_made: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class NavigationActionExecutor:
    """Executes navigation actions with safety checks and rollback capability"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.backup_dir = self.workspace / ".backups"
        self.error_handler = ErrorHandler()
        self.dependency_analyzer = ComponentDependencyAnalyzer(str(self.workspace))
        self.file_analyzer = FileAnalyzer()
        
        # Initialize backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Track active operations
        self.active_operations: Dict[UUID, NavigationAction] = {}
        self.operation_results: Dict[UUID, ActionResult] = {}
        logger.success("NavigationActionExecutor initialized successfully.")

    async def execute_action(self, action: NavigationAction) -> ActionResult:
        """Execute a navigation action with safety checks"""
        try:
            # Register active operation
            self.active_operations[action.id] = action
            
            # Validate paths
            await self._validate_paths(action)
            
            # Create backup if needed
            if action.action_type in [NavigationActionType.MODIFY, NavigationActionType.DELETE]:
                action.backup_path = await self._create_backup(action.source_path)
            
            # Execute appropriate action
            if action.action_type == NavigationActionType.CREATE:
                result = await self._execute_create(action)
            elif action.action_type == NavigationActionType.MODIFY:
                result = await self._execute_modify(action)
            elif action.action_type == NavigationActionType.DELETE:
                result = await self._execute_delete(action)
            elif action.action_type == NavigationActionType.MOVE:
                result = await self._execute_move(action)
            else:
                raise ValueError(f"Unsupported action type: {action.action_type}")
            
            # Store and return result
            self.operation_results[action.id] = result
            logger.success("Navigation action %s executed successfully.", action.id)
            return result
            
        except Exception as e:
            error_msg = str(e)
            self.error_handler.handle_error(e, metadata={
                "action_id": str(action.id),
                "action_type": action.action_type.value
            })
            
            # Attempt recovery if backup exists
            if action.backup_path:
                await self._restore_backup(action)
                error_msg += " (Backup restored)"
            
            result = ActionResult(
                action_id=action.id,
                success=False,
                source_path=action.source_path,
                target_path=action.target_path,
                backup_created=bool(action.backup_path),
                error=error_msg,
                changes_made={}
            )
            
            self.operation_results[action.id] = result
            return result
            
        finally:
            # Cleanup active operation
            self.active_operations.pop(action.id, None)

    async def _validate_paths(self, action: NavigationAction) -> None:
        """Validate source and target paths"""
        # Check paths are within workspace
        if not str(action.source_path).startswith(str(self.workspace)):
            raise ValueError(f"Source path must be within workspace: {action.source_path}")
        
        if action.target_path and not str(action.target_path).startswith(str(self.workspace)):
            raise ValueError(f"Target path must be within workspace: {action.target_path}")
        
        # Check source exists for appropriate actions
        if action.action_type in [NavigationActionType.MODIFY, NavigationActionType.DELETE, NavigationActionType.MOVE]:
            if not action.source_path.exists():
                raise FileNotFoundError(f"Source path does not exist: {action.source_path}")
        
        # Check target doesn't exist for create/move
        if action.action_type in [NavigationActionType.CREATE, NavigationActionType.MOVE]:
            if action.target_path and action.target_path.exists():
                raise FileExistsError(f"Target path already exists: {action.target_path}")

    async def _create_backup(self, path: Path) -> Path:
        """Create backup of a file"""
        if not path.exists():
            return None
            
        # Create timestamp-based backup path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"{path.name}.{timestamp}.bak"
        
        # Copy file to backup
        shutil.copy2(path, backup_path)
        logger.success("Backup created for file %s at %s", path, backup_path)
        return backup_path

    async def _restore_backup(self, action: NavigationAction) -> None:
        """Restore from backup"""
        if not action.backup_path or not action.backup_path.exists():
            return
            
        # Restore original file
        shutil.copy2(action.backup_path, action.source_path)
        
        # Clean up backup
        action.backup_path.unlink()
        logger.success("Backup restored for action %s", action.id)

    async def _execute_create(self, action: NavigationAction) -> ActionResult:
        """Execute file creation"""
        target_path = action.target_path or action.source_path
        
        # Create parent directories if needed
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        if action.content:
            target_path.write_text(action.content)
        else:
            target_path.touch()
        
        logger.success("File created successfully at %s", target_path)
        return ActionResult(
            action_id=action.id,
            success=True,
            source_path=action.source_path,
            target_path=target_path,
            backup_created=False,
            changes_made={"operation": "create", "path": str(target_path)}
        )

    async def _execute_modify(self, action: NavigationAction) -> ActionResult:
        """Execute file modification"""
        if not action.content:
            raise ValueError("Content required for modify action")
        
        # Write new content
        action.source_path.write_text(action.content)
        
        # Analyze changes
        original_content = ""
        if action.backup_path:
            original_content = action.backup_path.read_text()
        
        changes = self._analyze_changes(original_content, action.content)
        logger.success("File modified successfully at %s", action.source_path)
        return ActionResult(
            action_id=action.id,
            success=True,
            source_path=action.source_path,
            target_path=None,
            backup_created=bool(action.backup_path),
            changes_made=changes
        )

    async def _execute_delete(self, action: NavigationAction) -> ActionResult:
        """Execute file deletion"""
        # Delete file
        action.source_path.unlink()
        logger.success("File deleted successfully: %s", action.source_path)
        return ActionResult(
            action_id=action.id,
            success=True,
            source_path=action.source_path,
            target_path=None,
            backup_created=bool(action.backup_path),
            changes_made={"operation": "delete", "path": str(action.source_path)}
        )

    async def _execute_move(self, action: NavigationAction) -> ActionResult:
        """Execute file move"""
        if not action.target_path:
            raise ValueError("Target path required for move action")
        
        # Create parent directories if needed
        action.target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.move(str(action.source_path), str(action.target_path))
        logger.success("File moved successfully from %s to %s", action.source_path, action.target_path)
        return ActionResult(
            action_id=action.id,
            success=True,
            source_path=action.source_path,
            target_path=action.target_path,
            backup_created=False,
            changes_made={
                "operation": "move",
                "source": str(action.source_path),
                "target": str(action.target_path)
            }
        )

    def _analyze_changes(self, original: str, modified: str) -> Dict[str, Any]:
        """Analyze changes between original and modified content"""
        changes = {
            "operation": "modify",
            "lines_changed": 0,
            "additions": 0,
            "deletions": 0
        }
        
        original_lines = original.splitlines()
        modified_lines = modified.splitlines()
        
        # Simple line-based diff
        changes["lines_changed"] = abs(len(modified_lines) - len(original_lines))
        changes["additions"] = sum(1 for line in modified_lines if line not in original_lines)
        changes["deletions"] = sum(1 for line in original_lines if line not in modified_lines)
        
        return changes

    async def cleanup_backups(self, max_age_hours: int = 24) -> int:
        """Clean up old backup files"""
        cleanup_count = 0
        current_time = datetime.now()
        
        for backup_file in self.backup_dir.glob("*.bak"):
            try:
                # Parse timestamp from filename
                timestamp_str = backup_file.stem.split(".")[-1]
                backup_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                # Check age
                age_hours = (current_time - backup_time).total_seconds() / 3600
                if age_hours > max_age_hours:
                    backup_file.unlink()
                    cleanup_count += 1
                    
            except Exception as e:
                self.error_handler.handle_error(e, metadata={
                    "backup_file": str(backup_file)
                })
                
        if cleanup_count:
            logger.success("Cleaned up %d backup files.", cleanup_count)
        return cleanup_count

    def get_operation_history(self, limit: Optional[int] = None) -> List[ActionResult]:
        """Get history of operations"""
        history = sorted(
            self.operation_results.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return history[:limit] if limit else history

    def get_active_operations(self) -> List[NavigationAction]:
        """Get list of currently active operations"""
        return list(self.active_operations.values())
