# src/task_management/progress_tracker.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
import json
from pathlib import Path

# Import logger and configuration loader
from utils.logger import get_logger
from utils.config import load_config

# -------------------------------
# Define Task Status and Progress Data Structures
# -------------------------------

class TaskStatus(Enum):
    """Task status states"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"

@dataclass
class TaskProgress:
    """Task progress information"""
    task_id: UUID
    name: str
    description: str
    status: TaskStatus
    progress: float  # 0-100
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    dependencies: List[UUID] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProgressSnapshot:
    """Progress tracking snapshot"""
    timestamp: datetime
    completed_tasks: int
    total_tasks: int
    overall_progress: float
    status_counts: Dict[str, int]
    active_tasks: List[str]

# -------------------------------
# ProgressTracker Class Definition
# -------------------------------

class ProgressTracker:
    """Tracks task and workflow progress and records periodic snapshots."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.logger = get_logger(__name__)
        # Load configuration (if available) to set snapshot interval; default to 300 seconds (5 minutes)
        config = load_config()  # Assumes load_config returns a dict
        self.snapshot_interval: int = config.get("progress_tracker", {}).get("snapshot_interval", 300)
        
        # Set storage directory for progress data
        self.storage_path = Path(storage_path) if storage_path else Path("temp/progress_tracker")
        if not self.storage_path.exists():
            self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.tasks: Dict[UUID, TaskProgress] = {}
        self.snapshots: List[ProgressSnapshot] = []
        self.last_snapshot: Optional[datetime] = None
        
        # Attempt to load previously saved progress data
        self._load_progress()

    def record_snapshot(self) -> None:
        """Record a progress snapshot based on current task data."""
        now = datetime.now()
        total_tasks = len(self.tasks)
        completed_tasks = sum(
            1 for task in self.tasks.values()
            if task.status in [TaskStatus.COMPLETED, TaskStatus.SKIPPED, TaskStatus.FAILED]
        )
        overall_progress = (sum(task.progress for task in self.tasks.values()) / total_tasks) if total_tasks > 0 else 0.0
        
        # Count statuses
        status_counts: Dict[str, int] = {}
        for task in self.tasks.values():
            status_str = task.status.value
            status_counts[status_str] = status_counts.get(status_str, 0) + 1
        
        active_tasks = [str(task.task_id) for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS]
        
        snapshot = ProgressSnapshot(
            timestamp=now,
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            overall_progress=overall_progress,
            status_counts=status_counts,
            active_tasks=active_tasks
        )
        self.snapshots.append(snapshot)
        self.last_snapshot = now
        self.logger.info(f"Recorded progress snapshot at {now.isoformat()}")
        self._save_progress()

    def get_task_progress(self, task_id: Union[str, UUID]) -> Optional[TaskProgress]:
        """Get progress information for a specific task."""
        if isinstance(task_id, str):
            task_id = UUID(task_id)
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[TaskProgress]:
        """Return all tracked tasks."""
        return list(self.tasks.values())

    def get_active_tasks(self) -> List[TaskProgress]:
        """Return all currently active tasks."""
        return [task for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS]

    def calculate_overall_progress(self) -> float:
        """Calculate overall progress across all tasks."""
        if not self.tasks:
            return 0.0
        total_progress = sum(task.progress for task in self.tasks.values())
        return total_progress / len(self.tasks)

    # -------------------------------
    # Persistence Methods
    # -------------------------------

    def _save_progress(self) -> None:
        """Persist current tasks and snapshots to a JSON file."""
        try:
            data = {
                "tasks": {
                    str(task_id): {
                        "name": task.name,
                        "description": task.description,
                        "status": task.status.value,
                        "progress": task.progress,
                        "created_at": task.created_at.isoformat(),
                        "started_at": task.started_at.isoformat() if task.started_at else None,
                        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                        "dependencies": [str(dep) for dep in task.dependencies],
                        "metadata": task.metadata
                    } for task_id, task in self.tasks.items()
                },
                "snapshots": [
                    {
                        "timestamp": snap.timestamp.isoformat(),
                        "completed_tasks": snap.completed_tasks,
                        "total_tasks": snap.total_tasks,
                        "overall_progress": snap.overall_progress,
                        "status_counts": snap.status_counts,
                        "active_tasks": snap.active_tasks
                    } for snap in self.snapshots
                ]
            }
            progress_file = self.storage_path / "progress.json"
            with open(progress_file, "w") as f:
                json.dump(data, f, indent=2)
            self.logger.info("Progress data saved successfully.")
        except Exception as e:
            self.logger.error(f"Error saving progress data: {str(e)}")

    def _load_progress(self) -> None:
        """Load tasks and snapshots from persistent storage."""
        progress_file = self.storage_path / "progress.json"
        if not progress_file.exists():
            return
        try:
            with open(progress_file, "r") as f:
                data = json.load(f)
            tasks_data = data.get("tasks", {})
            for task_id_str, task_data in tasks_data.items():
                task = TaskProgress(
                    task_id=UUID(task_id_str),
                    name=task_data["name"],
                    description=task_data["description"],
                    status=TaskStatus(task_data["status"]),
                    progress=task_data["progress"],
                    created_at=datetime.fromisoformat(task_data["created_at"]),
                    started_at=datetime.fromisoformat(task_data["started_at"]) if task_data.get("started_at") else None,
                    completed_at=datetime.fromisoformat(task_data["completed_at"]) if task_data.get("completed_at") else None,
                    dependencies=[UUID(dep) for dep in task_data.get("dependencies", [])],
                    metadata=task_data.get("metadata", {})
                )
                self.tasks[task.task_id] = task
            snapshots_data = data.get("snapshots", [])
            for snap_data in snapshots_data:
                snap = ProgressSnapshot(
                    timestamp=datetime.fromisoformat(snap_data["timestamp"]),
                    completed_tasks=snap_data["completed_tasks"],
                    total_tasks=snap_data["total_tasks"],
                    overall_progress=snap_data["overall_progress"],
                    status_counts=snap_data["status_counts"],
                    active_tasks=snap_data["active_tasks"]
                )
                self.snapshots.append(snap)
            if self.snapshots:
                self.last_snapshot = self.snapshots[-1].timestamp
            self.logger.info("Progress data loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading progress data: {str(e)}")
