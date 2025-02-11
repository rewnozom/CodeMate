# src/core/memory_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4

class MemoryType(Enum):
    """Types of agent memory"""
    SHORT_TERM = "short_term"
    WORKING = "working"
    LONG_TERM = "long_term"
    PERSISTENT = "persistent"

@dataclass
class MemoryItem:
    """Individual memory item"""
    id: UUID
    content: Any
    type: MemoryType
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    importance: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    expires_at: Optional[datetime] = None

class MemoryManager:
    """Manages different types of agent memory"""
    
    def __init__(self):
        self.memories: Dict[UUID, MemoryItem] = {}
        self.type_limits: Dict[MemoryType, int] = {
            MemoryType.SHORT_TERM: 100,
            MemoryType.WORKING: 50,
            MemoryType.LONG_TERM: 1000,
            MemoryType.PERSISTENT: 500
        }
        self.cleanup_thresholds: Dict[MemoryType, timedelta] = {
            MemoryType.SHORT_TERM: timedelta(minutes=30),
            MemoryType.WORKING: timedelta(hours=2),
            MemoryType.LONG_TERM: timedelta(days=7),
            MemoryType.PERSISTENT: timedelta(days=30)
        }

    def store(self, 
             content: Any,
             memory_type: MemoryType,
             importance: int = 0,
             metadata: Optional[Dict[str, Any]] = None,
             expires_in: Optional[timedelta] = None) -> UUID:
        """Store new memory item"""
        # Create memory item
        item = MemoryItem(
            id=uuid4(),
            content=content,
            type=memory_type,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            importance=importance,
            metadata=metadata or {},
            expires_at=datetime.now() + expires_in if expires_in else None
        )
        
        # Check and maintain limits
        self._check_type_limit(memory_type)
        
        # Store item
        self.memories[item.id] = item
        return item.id

    def retrieve(self, 
                memory_id: UUID,
                update_access: bool = True) -> Optional[Any]:
        """Retrieve memory content"""
        item = self.memories.get(memory_id)
        if item:
            if update_access:
                item.last_accessed = datetime.now()
                item.access_count += 1
            return item.content
        return None

    def search(self,
              memory_type: Optional[MemoryType] = None,
              importance_threshold: int = 0,
              metadata_filter: Optional[Dict[str, Any]] = None) -> List[MemoryItem]:
        """Search memories with filters"""
        results = []
        
        for item in self.memories.values():
            if (memory_type is None or item.type == memory_type) and \
               item.importance >= importance_threshold and \
               self._matches_metadata(item, metadata_filter):
                results.append(item)
                
        return sorted(results, key=lambda x: (-x.importance, -x.access_count))

    def update(self,
              memory_id: UUID,
              content: Optional[Any] = None,
              importance: Optional[int] = None,
              metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update memory item"""
        if memory_id in self.memories:
            item = self.memories[memory_id]
            
            if content is not None:
                item.content = content
            if importance is not None:
                item.importance = importance
            if metadata:
                item.metadata.update(metadata)
                
            item.last_accessed = datetime.now()
            return True
        return False

    def forget(self, memory_id: UUID) -> bool:
        """Remove memory item"""
        return bool(self.memories.pop(memory_id, None))

    def cleanup(self) -> int:
        """Clean up expired and old memories"""
        now = datetime.now()
        removed_count = 0
        
        items_to_remove = []
        for item in self.memories.values():
            # Check expiration
            if item.expires_at and now > item.expires_at:
                items_to_remove.append(item.id)
                continue
                
            # Check age threshold
            age_threshold = self.cleanup_thresholds[item.type]
            if (now - item.last_accessed) > age_threshold and item.importance < 5:
                items_to_remove.append(item.id)
                
        for item_id in items_to_remove:
            self.forget(item_id)
            removed_count += 1
            
        return removed_count

    def _check_type_limit(self, memory_type: MemoryType) -> None:
        """Check and maintain memory type limits"""
        type_memories = [m for m in self.memories.values() if m.type == memory_type]
        limit = self.type_limits[memory_type]
        
        if len(type_memories) >= limit:
            # Sort by importance and access patterns
            to_remove = sorted(
                type_memories,
                key=lambda x: (x.importance, x.access_count, x.last_accessed.timestamp())
            )
            
            # Remove oldest, least important items
            while len(type_memories) >= limit:
                item = to_remove.pop(0)
                self.forget(item.id)

    def _matches_metadata(self, item: MemoryItem, metadata_filter: Optional[Dict[str, Any]] = None) -> bool:
        """Check if item matches metadata filter"""
        if not metadata_filter:
            return True
            
        for key, value in metadata_filter.items():
            if key not in item.metadata or item.metadata[key] != value:
                return False
        return True

    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics"""
        stats = {
            "total_memories": len(self.memories),
            "by_type": {
                memory_type: len([m for m in self.memories.values() if m.type == memory_type])
                for memory_type in MemoryType
            },
            "average_importance": sum(m.importance for m in self.memories.values()) / len(self.memories) if self.memories else 0,
            "average_access_count": sum(m.access_count for m in self.memories.values()) / len(self.memories) if self.memories else 0
        }
        return stats

    def consolidate_memories(self, threshold: int = 5) -> None:
        """Consolidate frequently accessed short-term memories to long-term"""
        for item in list(self.memories.values()):
            if item.type == MemoryType.SHORT_TERM and item.access_count >= threshold:
                # Create new long-term memory
                self.store(
                    content=item.content,
                    memory_type=MemoryType.LONG_TERM,
                    importance=item.importance + 1,
                    metadata={**item.metadata, "consolidated_from": str(item.id)}
                )
                # Remove old short-term memory
                self.forget(item.id)

