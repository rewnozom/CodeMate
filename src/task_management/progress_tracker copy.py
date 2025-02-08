# src/task_management/progress_tracker.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum
from pathlib import Path

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
    task_id: str
    name: str
    status: TaskStatus
    progress: float  # 0-100
    start_time: datetime
    end_time: Optional[datetime] = None
    subtasks: List['TaskProgress'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class ProgressTracker:
    """Tracks progress of tasks and workflows"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else Path("temp/progress")
        self.tasks: Dict[str, TaskProgress] = {}
        self.active_task: Optional[str] = None
        
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self._load_progress()

    def start_task(self, 
                  task_id: str,
                  name: str,
                  metadata: Optional[Dict[str, Any]] = None) -> TaskProgress:
        """Start tracking a new task"""
        task = TaskProgress(
            task_id=task_id,
            name=name,
            status=TaskStatus.IN_PROGRESS,
            progress=0.0,
            start_time=datetime.now(),
            metadata=metadata or {}
        )
        
        self.tasks[task_id] = task
        self.active_task = task_id
        self._save_progress()
        
        return task

    def update_progress(self,
                       task_id: str,
                       progress: float,
                       status: Optional[TaskStatus] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update task progress"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        task = self.tasks[task_id]
        task.progress = min(100.0, max(0.0, progress))
        
        if status:
            task.status = status
            if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED]:
                task.end_time = datetime.now()
                
        if metadata:
            task.metadata.update(metadata)
            
        self._save_progress()

    def add_subtask(self,
                   parent_id: str,
                   subtask_id: str,
                   name: str,
                   metadata: Optional[Dict[str, Any]] = None) -> TaskProgress:
        """Add a subtask to a parent task"""
        if parent_id not in self.tasks:
            raise ValueError(f"Parent task {parent_id} not found")
            
        subtask = TaskProgress(
            task_id=subtask_id,
            name=name,
            status=TaskStatus.NOT_STARTED,
            progress=0.0,
            start_time=datetime.now(),
            metadata=metadata or {}
        )
        
        self.tasks[parent_id].subtasks.append(subtask)
        self.tasks[subtask_id] = subtask
        self._save_progress()
        
        return subtask

    def complete_task(self,
                     task_id: str,
                     status: TaskStatus = TaskStatus.COMPLETED,
                     metadata: Optional[Dict[str, Any]] = None) -> None:
        """Mark task as complete"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        task = self.tasks[task_id]
        task.status = status
        task.progress = 100.0
        task.end_time = datetime.now()
        
        if metadata:
            task.metadata.update(metadata)
            
        if self.active_task == task_id:
            self.active_task = None
            
        self._save_progress()

    def get_task_progress(self, task_id: str) -> TaskProgress:
        """Get progress information for a task"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        return self.tasks[task_id]

    def get_all_tasks(self) -> List[TaskProgress]:
        """Get all tracked tasks"""
        return list(self.tasks.values())

    def get_active_tasks(self) -> List[TaskProgress]:
        """Get all currently active tasks"""
        return [
            task for task in self.tasks.values()
            if task.status == TaskStatus.IN_PROGRESS
        ]

    def calculate_overall_progress(self, task_id: str) -> float:
        """Calculate overall progress including subtasks"""
        task = self.tasks.get(task_id)
        if not task:
            return 0.0

        if not task.subtasks:
            return task.progress

        subtask_progress = sum(self.calculate_overall_progress(st.task_id) 
                             for st in task.subtasks)
        return (task.progress + subtask_progress) / (len(task.subtasks) + 1)

    def _save_progress(self) -> None:
        """Save progress to storage"""
        if not self.storage_path:
            return

        data = {
            task_id: {
                "name": task.name,
                "status": task.status.value,
                "progress": task.progress,
                "start_time": task.start_time.isoformat(),
                "end_time": task.end_time.isoformat() if task.end_time else None,
                "metadata": task.metadata,
                "subtasks": [
                    {
                        "task_id": st.task_id,
                        "name": st.name,
                        "status": st.status.value,
                        "progress": st.progress,
                        "start_time": st.start_time.isoformat(),
                        "end_time": st.end_time.isoformat() if st.end_time else None,
                        "metadata": st.metadata
                    }
                    for st in task.subtasks
                ]
            }
            for task_id, task in self.tasks.items()
        }

        with open(self.storage_path / "progress.json", 'w') as f:
            json.dump(data, f, indent=2)

    def _load_progress(self) -> None:
        """Load progress from storage"""
        progress_file = self.storage_path / "progress.json"
        if not progress_file.exists():
            return

        try:
            with open(progress_file) as f:
                data = json.load(f)

            for task_id, task_data in data.items():
                task = TaskProgress(
                    task_id=task_id,
                    name=task_data["name"],
                    status=TaskStatus(task_data["status"]),
                    progress=task_data["progress"],
                    start_time=datetime.fromisoformat(task_data["start_time"]),
                    end_time=datetime.fromisoformat(task_data["end_time"])
                    if task_data.get("end_time") else None,
                    metadata=task_data.get("metadata", {})
                )

                for st_data in task_data.get("subtasks", []):
                    subtask = TaskProgress(
                        task_id=st_data["task_id"],
                        name=st_data["name"],
                        status=TaskStatus(st_data["status"]),
                        progress=st_data["progress"],
                        start_time=datetime.fromisoformat(st_data["start_time"]),
                        end_time=datetime.fromisoformat(st_data["end_time"])
                        if st_data.get("end_time") else None,
                        metadata=st_data.get("metadata", {})
                    )
                    task.subtasks.append(subtask)
                    self.tasks[subtask.task_id] = subtask

                self.tasks[task_id] = task

        except Exception as e:
            print(f"Error loading progress data: {str(e)}")