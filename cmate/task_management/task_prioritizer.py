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