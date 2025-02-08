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
