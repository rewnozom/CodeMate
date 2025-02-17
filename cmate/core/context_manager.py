# ..\..\cmate\core\context_manager.py
# cmate/core/context_manager.py
"""
cmate/core/context_manager.py

Manages the agent's context window and context organization.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)
logger.info("ContextManager module loaded.")

@dataclass
class ContextItem:
    """Individual context item"""
    id: UUID
    content: Any
    type: str
    priority: int
    created_at: datetime
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    token_count: int = 0

@dataclass
class ContextGroup:
    """Group of related context items"""
    id: UUID
    name: str
    items: List[ContextItem] = field(default_factory=list)
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

class ContextManager:
    """Manages the agent's context window and context organization"""
    
    def __init__(self, max_tokens: int = 60000):
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.context_items: Dict[UUID, ContextItem] = {}
        self.context_groups: Dict[UUID, ContextGroup] = {}
        self.active_group: Optional[UUID] = None
        logger.info("ContextManager initialized with max_tokens=%d", self.max_tokens)
        logger.success("ContextManager initialized successfully with max_tokens=%d", self.max_tokens)

    def add_context(self, content: Any, type: str, priority: int = 0, group_id: Optional[UUID] = None, token_count: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Add a new context item"""
        item = ContextItem(
            id=uuid4(),
            content=content,
            type=type,
            priority=priority,
            created_at=datetime.now(),
            metadata=metadata or {},
            token_count=token_count or self._estimate_tokens(content)
        )
        logger.debug("Adding context item %s with estimated %d tokens", item.id, item.token_count)
        if not self._check_token_limit(item.token_count):
            logger.info("Token limit exceeded. Trimming context to free up %d tokens", item.token_count)
            self._trim_context(item.token_count)
        self.context_items[item.id] = item
        self.current_tokens += item.token_count
        logger.debug("Context item %s added. Current token count: %d", item.id, self.current_tokens)
        if group_id and group_id in self.context_groups:
            self.context_groups[group_id].items.append(item)
            logger.debug("Added context item %s to group %s", item.id, group_id)
        # Optionally, log a success message for adding an item
        logger.success("Context item %s stored successfully. Total tokens now: %d", item.id, self.current_tokens)
        return item.id

    def create_group(self, name: str, priority: int = 0, metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Create a new context group"""
        group = ContextGroup(
            id=uuid4(),
            name=name,
            priority=priority,
            metadata=metadata or {}
        )
        self.context_groups[group.id] = group
        logger.info("Created new context group '%s' with id %s", name, group.id)
        logger.success("Context group '%s' created successfully.", name)
        return group.id

    def set_active_group(self, group_id: UUID) -> None:
        """Set active context group"""
        if group_id in self.context_groups:
            self.active_group = group_id
            logger.debug("Active context group set to %s", group_id)

    def get_context(self, type: Optional[str] = None, group_id: Optional[UUID] = None, min_priority: int = 0) -> List[ContextItem]:
        """Get context items with optional filtering"""
        logger.debug("Retrieving context items with type=%s and group_id=%s", type, group_id)
        items = []
        if group_id:
            group = self.context_groups.get(group_id)
            if group:
                items = group.items
        else:
            items = list(self.context_items.values())
        filtered_items = [item for item in items if item.priority >= min_priority and (type is None or item.type == type)]
        sorted_items = sorted(filtered_items, key=lambda x: (-x.priority, x.created_at))
        logger.debug("Retrieved %d context items after filtering", len(sorted_items))
        return sorted_items

    def remove_context(self, item_id: UUID) -> bool:
        """Remove a context item"""
        if item_id in self.context_items:
            item = self.context_items[item_id]
            self.current_tokens -= item.token_count
            for group in self.context_groups.values():
                group.items = [i for i in group.items if i.id != item_id]
            del self.context_items[item_id]
            logger.debug("Removed context item %s. Current tokens: %d", item_id, self.current_tokens)
            logger.success("Context item %s removed successfully.", item_id)
            return True
        logger.warning("Attempted to remove non-existent context item %s", item_id)
        return False

    def _check_token_limit(self, new_tokens: int) -> bool:
        """Check if adding new tokens would exceed the limit"""
        return self.current_tokens + new_tokens <= self.max_tokens

    def _trim_context(self, needed_tokens: int) -> None:
        """Trim context to free up tokens for new content"""
        items = sorted(self.context_items.values(), key=lambda x: (x.priority, -x.created_at.timestamp()))
        freed_tokens = 0
        items_to_remove = []
        for item in items:
            if self.current_tokens - freed_tokens + needed_tokens <= self.max_tokens:
                break
            freed_tokens += item.token_count
            items_to_remove.append(item.id)
        for item_id in items_to_remove:
            self.remove_context(item_id)
        logger.info("Trimmed context and freed %d tokens", freed_tokens)
        logger.success("Context trimmed successfully. Freed %d tokens.", freed_tokens)

    def _estimate_tokens(self, content: Any) -> int:
        """Estimate token count for content"""
        if isinstance(content, str):
            estimated = len(content) // 4
            logger.debug("Estimated %d tokens for given content", estimated)
            return estimated
        elif isinstance(content, dict):
            return self._estimate_tokens(json.dumps(content))
        elif isinstance(content, list):
            return sum(self._estimate_tokens(item) for item in content)
        return 1
