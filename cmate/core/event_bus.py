# src/core/event_bus.py
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import logging
from uuid import UUID, uuid4

@dataclass
class EventSubscription:
    """Event subscription details"""
    id: UUID
    event_type: str
    callback: Callable
    filters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

class EventBus:
    """Handles event distribution and management"""
    
    def __init__(self):
        self._subscriptions: Dict[str, List[EventSubscription]] = {}
        self._event_history: List[Dict[str, Any]] = []
        self._max_history = 1000
        self.logger = logging.getLogger(__name__)

    async def publish(self, event_type: str, data: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Publish an event to all subscribers"""
        try:
            event_data = {
                "id": str(uuid4()),
                "type": event_type,
                "data": data,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }
            
            self._record_event(event_data)
            
            if event_type in self._subscriptions:
                subscriber_tasks = []
                for subscription in self._subscriptions[event_type]:
                    if subscription.is_active and self._matches_filters(data, subscription.filters):
                        task = asyncio.create_task(self._notify_subscriber(subscription, event_data))
                        subscriber_tasks.append(task)
                
                if subscriber_tasks:
                    await asyncio.gather(*subscriber_tasks, return_exceptions=True)
                    
        except Exception as e:
            self.logger.error(f"Error publishing event {event_type}: {str(e)}")
            raise

    def subscribe(self, event_type: str, callback: Callable, filters: Optional[Dict[str, Any]] = None) -> UUID:
        """Subscribe to an event type"""
        subscription = EventSubscription(
            id=uuid4(),
            event_type=event_type,
            callback=callback,
            filters=filters or {}
        )
        
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = []
            
        self._subscriptions[event_type].append(subscription)
        return subscription.id

    def unsubscribe(self, subscription_id: UUID) -> bool:
        """Unsubscribe from an event"""
        for subs in self._subscriptions.values():
            for sub in subs:
                if sub.id == subscription_id:
                    sub.is_active = False
                    return True
        return False

    async def _notify_subscriber(self, subscription: EventSubscription, event_data: Dict[str, Any]) -> None:
        """Notify a subscriber of an event"""
        try:
            await subscription.callback(event_data)
        except Exception as e:
            self.logger.error(f"Error notifying subscriber {subscription.id}: {str(e)}")
            # Don't re-raise to prevent affecting other subscribers

    def _matches_filters(self, data: Any, filters: Dict[str, Any]) -> bool:
        """Check if event data matches subscription filters"""
        try:
            for key, value in filters.items():
                if isinstance(data, dict):
                    if key not in data or data[key] != value:
                        return False
                else:
                    return False
            return True
        except Exception:
            return False

    def _record_event(self, event_data: Dict[str, Any]) -> None:
        """Record event in history"""
        self._event_history.append(event_data)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)

    def get_event_history(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get event history, optionally filtered by type"""
        if event_type:
            return [event for event in self._event_history if event["type"] == event_type]
        return self._event_history.copy()
