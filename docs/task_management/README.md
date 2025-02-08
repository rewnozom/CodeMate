# docs/task_management/README.md
# Task Management Documentation

## Overview
Task management handles workflow planning, execution, and monitoring.

### Components
- task_planner.py
- checklist_manager.py
- progress_tracker.py
- process_manager.py

## Task Planning Example
```python
from task_management.task_planner import TaskPlanner

planner = TaskPlanner()
plan = await planner.create_plan("Update function name in example.py")
```

## Progress Tracking
```python
from task_management.progress_tracker import ProgressTracker

tracker = ProgressTracker()
tracker.start_task("code_modification", "Updating function names")
```

[More task management details...](./tasks.md)
