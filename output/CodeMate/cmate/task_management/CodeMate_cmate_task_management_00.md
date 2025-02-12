# Project Details

# Table of Contents
- [..\CodeMate\cmate\task_management\__init__.py](#-CodeMate-cmate-task_management-__init__py)
- [..\CodeMate\cmate\task_management\checklist_manager.py](#-CodeMate-cmate-task_management-checklist_managerpy)
- [..\CodeMate\cmate\task_management\process_manager.py](#-CodeMate-cmate-task_management-process_managerpy)
- [..\CodeMate\cmate\task_management\progress_tracker.py](#-CodeMate-cmate-task_management-progress_trackerpy)
- [..\CodeMate\cmate\task_management\task_prioritizer.py](#-CodeMate-cmate-task_management-task_prioritizerpy)


# ..\..\CodeMate\cmate\task_management\__init__.py
## File: ..\..\CodeMate\cmate\task_management\__init__.py

```py
# ..\..\CodeMate\cmate\task_management\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\cmate\task_management\checklist_manager.py
## File: ..\..\CodeMate\cmate\task_management\checklist_manager.py

```py
# ..\..\CodeMate\cmate\task_management\checklist_manager.py
# src/task_management/checklist_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

class ChecklistItemStatus(Enum):
    """Status for checklist items"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    FAILED = "failed"

@dataclass
class ChecklistItem:
    """Individual checklist item"""
    id: UUID
    title: str
    description: str
    status: ChecklistItemStatus
    priority: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    dependencies: List[UUID] = field(default_factory=list)
    subtasks: List['ChecklistItem'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Checklist:
    """Complete checklist"""
    id: UUID
    name: str
    description: str
    items: List[ChecklistItem]
    created_at: datetime
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class ChecklistManager:
    """Manages task checklists"""
    
    def __init__(self):
        self.checklists: Dict[UUID, Checklist] = {}
        self.active_checklist: Optional[UUID] = None
        self.templates: Dict[str, Checklist] = {}

    def create_checklist(self,
                       name: str,
                       description: str,
                       items: Optional[List[Dict[str, Any]]] = None,
                       template: Optional[str] = None) -> UUID:
        """Create new checklist"""
        checklist_id = uuid4()
        
        if template and template in self.templates:
            # Clone template
            template_list = self.templates[template]
            checklist = Checklist(
                id=checklist_id,
                name=name,
                description=description,
                items=[self._clone_item(item) for item in template_list.items],
                created_at=datetime.now(),
                metadata={}
            )
        else:
            # Create new checklist
            checklist_items = []
            if items:
                for item in items:
                    item_id = uuid4()
                    checklist_items.append(ChecklistItem(
                        id=item_id,
                        title=item["title"],
                        description=item.get("description", ""),
                        status=ChecklistItemStatus.PENDING,
                        priority=item.get("priority", 0),
                        created_at=datetime.now(),
                        dependencies=[UUID(dep) for dep in item.get("dependencies", [])],
                        metadata=item.get("metadata", {})
                    ))
            
            checklist = Checklist(
                id=checklist_id,
                name=name,
                description=description,
                items=checklist_items,
                created_at=datetime.now(),
                metadata={}
            )
        
        self.checklists[checklist_id] = checklist
        return checklist_id

    def add_item(self,
                checklist_id: UUID,
                title: str,
                description: str = "",
                priority: int = 0,
                dependencies: Optional[List[UUID]] = None) -> UUID:
        """Add item to checklist"""
        if checklist_id not in self.checklists:
            raise ValueError(f"Checklist not found: {checklist_id}")
            
        item_id = uuid4()
        item = ChecklistItem(
            id=item_id,
            title=title,
            description=description,
            status=ChecklistItemStatus.PENDING,
            priority=priority,
            created_at=datetime.now(),
            dependencies=dependencies or []
        )
        
        self.checklists[checklist_id].items.append(item)
        return item_id

    def update_item_status(self,
                          checklist_id: UUID,
                          item_id: UUID,
                          status: ChecklistItemStatus) -> None:
        """Update item status"""
        checklist = self.checklists.get(checklist_id)
        if not checklist:
            raise ValueError(f"Checklist not found: {checklist_id}")
            
        item = self._find_item(checklist, item_id)
        if not item:
            raise ValueError(f"Item not found: {item_id}")
            
        # Check dependencies
        if status == ChecklistItemStatus.IN_PROGRESS:
            blocked = self._check_dependencies(checklist, item)
            if blocked:
                raise ValueError(f"Item blocked by dependencies: {blocked}")
            
        item.status = status

        
        if status in [ChecklistItemStatus.COMPLETED, ChecklistItemStatus.FAILED]:
            item.completed_at = datetime.now()
            
        # Check if checklist is complete
        if all(item.status in [ChecklistItemStatus.COMPLETED, ChecklistItemStatus.SKIPPED]
               for item in checklist.items):
            checklist.completed_at = datetime.now()

    def get_checklist(self, checklist_id: UUID) -> Checklist:
        """Get checklist by ID"""
        if checklist_id not in self.checklists:
            raise ValueError(f"Checklist not found: {checklist_id}")
        return self.checklists[checklist_id]

    def get_item(self, checklist_id: UUID, item_id: UUID) -> ChecklistItem:
        """Get checklist item by ID"""
        checklist = self.get_checklist(checklist_id)
        item = self._find_item(checklist, item_id)
        if not item:
            raise ValueError(f"Item not found: {item_id}")
        return item

    def delete_item(self, checklist_id: UUID, item_id: UUID) -> None:
        """Delete checklist item"""
        checklist = self.get_checklist(checklist_id)
        item = self._find_item(checklist, item_id)
        if not item:
            raise ValueError(f"Item not found: {item_id}")
            
        # Remove from main items list
        checklist.items = [i for i in checklist.items if i.id != item_id]
        
        # Remove from subtasks
        for i in checklist.items:
            i.subtasks = [st for st in i.subtasks if st.id != item_id]

    def add_subtask(self,
                   checklist_id: UUID,
                   parent_id: UUID,
                   title: str,
                   description: str = "",
                   priority: int = 0) -> UUID:
        """Add subtask to checklist item"""
        checklist = self.get_checklist(checklist_id)
        parent = self._find_item(checklist, parent_id)
        if not parent:
            raise ValueError(f"Parent item not found: {parent_id}")
            
        subtask_id = uuid4()
        subtask = ChecklistItem(
            id=subtask_id,
            title=title,
            description=description,
            status=ChecklistItemStatus.PENDING,
            priority=priority,
            created_at=datetime.now()
        )
        
        parent.subtasks.append(subtask)
        return subtask_id

    def save_template(self, name: str, checklist_id: UUID) -> None:
        """Save checklist as template"""
        if checklist_id not in self.checklists:
            raise ValueError(f"Checklist not found: {checklist_id}")
            
        self.templates[name] = self.checklists[checklist_id]

    def get_templates(self) -> Dict[str, Checklist]:
        """Get all templates"""
        return self.templates.copy()

    def _find_item(self, checklist: Checklist, item_id: UUID) -> Optional[ChecklistItem]:
        """Find item in checklist by ID"""
        for item in checklist.items:
            if item.id == item_id:
                return item
            for subtask in item.subtasks:
                if subtask.id == item_id:
                    return subtask
        return None

    def _check_dependencies(self, checklist: Checklist, item: ChecklistItem) -> List[UUID]:
        """Check if item dependencies are met"""
        blocked = []
        for dep_id in item.dependencies:
            dep_item = self._find_item(checklist, dep_id)
            if dep_item and dep_item.status != ChecklistItemStatus.COMPLETED:
                blocked.append(dep_id)
        return blocked

    def _clone_item(self, item: ChecklistItem) -> ChecklistItem:
        """Create copy of checklist item"""
        return ChecklistItem(
            id=uuid4(),
            title=item.title,
            description=item.description,
            status=ChecklistItemStatus.PENDING,
            priority=item.priority,
            created_at=datetime.now(),
            dependencies=[],
            subtasks=[self._clone_item(st) for st in item.subtasks],
            metadata=item.metadata.copy()
        )

    def get_progress(self, checklist_id: UUID) -> Dict[str, Any]:
        """Get checklist progress statistics"""
        checklist = self.get_checklist(checklist_id)
        total_items = len(checklist.items)
        completed_items = len([
            item for item in checklist.items
            if item.status == ChecklistItemStatus.COMPLETED
        ])
        
        return {
            "total_items": total_items,
            "completed_items": completed_items,
            "progress_percentage": (completed_items / total_items * 100) if total_items > 0 else 0,
            "status": {
                status.value: len([
                    item for item in checklist.items
                    if item.status == status
                ])
                for status in ChecklistItemStatus
            }
        }

```

---

# ..\..\CodeMate\cmate\task_management\process_manager.py
## File: ..\..\CodeMate\cmate\task_management\process_manager.py

```py
# ..\..\CodeMate\cmate\task_management\process_manager.py
# cmate/task_management/process_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import psutil
from pathlib import Path
from uuid import UUID, uuid4

@dataclass
class ProcessInfo:
    """Information about a running process"""
    id: UUID
    name: str
    command: str
    pid: int
    start_time: datetime
    status: str
    cpu_percent: float
    memory_percent: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class ProcessManager:
    """Manages external process execution and monitoring"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.active_processes: Dict[UUID, ProcessInfo] = {}
        self.completed_processes: Dict[UUID, ProcessInfo] = {}
        self._monitoring = False
        self._monitor_task: Optional[asyncio.Task] = None

    async def start_process(self,
                          name: str,
                          command: Union[str, List[str]],
                          metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Start new process"""
        if isinstance(command, str):
            # Use shell to support built-in commands on Windows
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace)
            )
        else:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace)
            )
        
        process_id = uuid4()
        process_info = ProcessInfo(
            id=process_id,
            name=name,
            command=command if isinstance(command, str) else ' '.join(command),
            pid=process.pid,
            start_time=datetime.now(),
            status="running",
            cpu_percent=0.0,
            memory_percent=0.0,
            metadata=metadata or {}
        )
        
        self.active_processes[process_id] = process_info
        
        # Start monitoring if not already running
        if not self._monitoring:
            await self.start_monitoring()
            
        return process_id

    async def stop_process(self, process_id: UUID) -> bool:
        """Stop running process"""
        if process_id not in self.active_processes:
            return False
            
        process_info = self.active_processes[process_id]
        try:
            process = psutil.Process(process_info.pid)
            process.terminate()
            
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()
                
            process_info.status = "terminated"
            self.completed_processes[process_id] = process_info
            del self.active_processes[process_id]
            return True
            
        except psutil.NoSuchProcess:
            return False

    async def start_monitoring(self) -> None:
        """Start process monitoring"""
        if self._monitoring:
            return
            
        self._monitoring = True
        self._monitor_task = asyncio.create_task(self._monitor_processes())

    async def stop_monitoring(self) -> None:
        """Stop process monitoring"""
        self._monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            self._monitor_task = None

    async def _monitor_processes(self) -> None:
        """Monitor active processes"""
        while self._monitoring:
            for process_id, info in list(self.active_processes.items()):
                try:
                    process = psutil.Process(info.pid)
                    info.cpu_percent = process.cpu_percent()
                    info.memory_percent = process.memory_percent()
                    
                    if not process.is_running():
                        info.status = "completed"
                        self.completed_processes[process_id] = info
                        del self.active_processes[process_id]
                        
                except psutil.NoSuchProcess:
                    info.status = "terminated"
                    self.completed_processes[process_id] = info
                    del self.active_processes[process_id]
                    
            await asyncio.sleep(1)

    async def get_process_output(self, process_id: UUID) -> Dict[str, str]:
        """Get process output streams"""
        if process_id not in self.active_processes:
            raise ValueError(f"Process not found: {process_id}")
            
        # In practice, you would track the output from the asyncio subprocess.
        return {
            "stdout": "",
            "stderr": ""
        }

    def get_active_processes(self) -> List[ProcessInfo]:
        """Get list of active processes"""
        return list(self.active_processes.values())

    def get_completed_processes(self) -> List[ProcessInfo]:
        """Get list of completed processes"""
        return list(self.completed_processes.values())

    def get_process_info(self, process_id: UUID) -> Optional[ProcessInfo]:
        """Get information about specific process"""
        return self.active_processes.get(process_id) or self.completed_processes.get(process_id)

```

---

# ..\..\CodeMate\cmate\task_management\progress_tracker.py
## File: ..\..\CodeMate\cmate\task_management\progress_tracker.py

```py
# ..\..\CodeMate\cmate\task_management\progress_tracker.py
# src/task_management/progress_tracker.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
import json
from pathlib import Path

# Import logger and configuration loader
from cmate.utils.logger import get_logger
from cmate.utils.config import load_config

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

```

---

# ..\..\CodeMate\cmate\task_management\task_prioritizer.py
## File: ..\..\CodeMate\cmate\task_management\task_prioritizer.py

```py
# ..\..\CodeMate\cmate\task_management\task_prioritizer.py
# src/task_management/task_prioritizer.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

class PriorityLevel(Enum):
    """Task priority levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    TRIVIAL = 1

@dataclass
class TaskPriority:
    """Task priority information"""
    task_id: UUID
    base_priority: PriorityLevel
    dynamic_priority: float
    last_updated: datetime
    factors: Dict[str, float]

class TaskPrioritizer:
    """Manages task prioritization"""
    
    def __init__(self):
        self.task_priorities: Dict[UUID, TaskPriority] = {}
        self.priority_factors = {
            "age": 0.1,           # Age of task
            "complexity": 0.2,    # Task complexity
            "dependencies": 0.3,  # Number of dependencies
            "urgency": 0.4       # Business urgency
        }

    def set_task_priority(self,
                         task_id: UUID,
                         priority: PriorityLevel,
                         factors: Optional[Dict[str, float]] = None) -> None:
        """Set task priority"""
        self.task_priorities[task_id] = TaskPriority(
            task_id=task_id,
            base_priority=priority,
            dynamic_priority=priority.value,
            last_updated=datetime.now(),
            factors=factors or {}
        )
        self._update_dynamic_priority(task_id)

    def update_factors(self, task_id: UUID, factors: Dict[str, float]) -> None:
        """Update task priority factors"""
        if task_id not in self.task_priorities:
            raise ValueError(f"Task not found: {task_id}")
            
        priority = self.task_priorities[task_id]
        priority.factors.update(factors)
        priority.last_updated = datetime.now()
        self._update_dynamic_priority(task_id)

    def get_priority(self, task_id: UUID) -> Optional[TaskPriority]:
        """Get task priority information"""
        return self.task_priorities.get(task_id)

    def get_prioritized_tasks(self) -> List[UUID]:
        """Get tasks sorted by priority"""
        return sorted(
            self.task_priorities.keys(),
            key=lambda x: self.task_priorities[x].dynamic_priority,
            reverse=True
        )

    def _update_dynamic_priority(self, task_id: UUID) -> None:
        """Update dynamic priority based on factors"""
        priority = self.task_priorities[task_id]
        base = priority.base_priority.value
        
        # Calculate factor adjustments
        factor_sum = 0
        for factor, weight in self.priority_factors.items():
            if factor in priority.factors:
                factor_sum += priority.factors[factor] * weight
                
        # Update dynamic priority
        priority.dynamic_priority = base * (1 + factor_sum)
```

---

