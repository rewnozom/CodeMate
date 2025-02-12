# ..\..\cmate\core\event_bus.py
# cmate/core/event_bus.py
"""
cmate/core/event_bus.py

Enhanced event bus with support for:
- Navigation event chains
- Event prioritization
- Event correlation
- Advanced filtering
"""

from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import asyncio
import logging
from uuid import UUID, uuid4
from enum import Enum

class EventPriority(Enum):
    """Event priority levels"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class EventCategory(Enum):
    """Event categories"""
    NAVIGATION = "navigation"
    IMPLEMENTATION = "implementation"
    STATE = "state"
    ERROR = "error"
    SYSTEM = "system"
    USER = "user"

@dataclass
class EventSubscription:
    """Enhanced event subscription details"""
    id: UUID
    event_type: str
    callback: Callable
    priority: EventPriority = EventPriority.NORMAL
    category: Optional[EventCategory] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventChain:
    """Represents a chain of related events"""
    id: UUID
    category: EventCategory
    events: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

class EventBus:
    """Enhanced event bus with navigation support"""
    
    def __init__(self):
        self._subscriptions: Dict[str, List[EventSubscription]] = {}
        self._event_history: List[Dict[str, Any]] = []
        self._event_chains: Dict[UUID, EventChain] = {}
        self._active_chains: Set[UUID] = set()
        self._max_history = 1000
        self.logger = logging.getLogger(__name__)
        self.logger.info("EventBus initialized with max history %d", self._max_history)
        self.logger.success("EventBus initialized successfully with max history %d", self._max_history)

        # Prioritized event queues
        self._event_queues: Dict[EventPriority, asyncio.Queue] = {
            priority: asyncio.Queue() for priority in EventPriority
        }

        # Initialize workers
        self._workers: Dict[EventPriority, asyncio.Task] = {}
        self._is_running = True

    async def start(self) -> None:
        """Start event processing workers"""
        self.logger.info("Starting event processing workers.")
        for priority in EventPriority:
            self._workers[priority] = asyncio.create_task(
                self._process_event_queue(priority)
            )
        self.logger.success("Event processing workers started successfully.")

    async def stop(self) -> None:
        """Stop event processing"""
        self.logger.info("Stopping event processing workers.")
        self._is_running = False
        
        # Cancel all workers with protection for closed loop errors
        for worker in self._workers.values():
            try:
                worker.cancel()
            except RuntimeError:
                pass
        await asyncio.gather(*self._workers.values(), return_exceptions=True)
        self.logger.success("Event processing workers stopped successfully.")

    async def publish(
        self,
        event_type: str,
        data: Any,
        priority: EventPriority = EventPriority.NORMAL,
        category: Optional[EventCategory] = None,
        chain_id: Optional[UUID] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Publish an event with enhanced metadata"""
        try:
            event_id = uuid4()
            event_data = {
                "id": str(event_id),
                "type": event_type,
                "data": data,
                "priority": priority,
                "category": category.value if category else None,
                "chain_id": str(chain_id) if chain_id else None,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }
            self.logger.debug("Publishing event '%s' with data: %s", event_type, event_data)
            # Add to history
            self._record_event(event_data)
            
            # Add to event chain if part of one
            if chain_id:
                await self._add_to_chain(chain_id, event_data)
            
            # Add to appropriate priority queue
            await self._event_queues[priority].put(event_data)
            self.logger.debug("Event '%s' published successfully.", event_type)
        except Exception as e:
            self.logger.error("Error publishing event '%s': %s", event_type, str(e))
            raise

    async def _process_event_queue(self, priority: EventPriority) -> None:
        """Process events from a priority queue"""
        queue = self._event_queues[priority]
        self.logger.debug("Started processing event queue for priority: %s", priority.name)
        
        while self._is_running:
            try:
                event_data = await queue.get()
                self.logger.debug("Processing event: %s", event_data)
                
                if event_data["type"] in self._subscriptions:
                    subscriber_tasks = []
                    for subscription in self._subscriptions[event_data["type"]]:
                        if subscription.is_active and self._matches_filters(event_data, subscription.filters):
                            task = asyncio.create_task(self._notify_subscriber(subscription, event_data))
                            subscriber_tasks.append(task)
                    if subscriber_tasks:
                        await asyncio.gather(*subscriber_tasks, return_exceptions=True)
                
                queue.task_done()
                
            except asyncio.CancelledError:
                self.logger.debug("Event queue processing cancelled for priority: %s", priority.name)
                break
            except Exception as e:
                self.logger.error("Error processing event queue: %s", str(e))
                await asyncio.sleep(1)

    def subscribe(
        self,
        event_type: str,
        callback: Callable,
        priority: EventPriority = EventPriority.NORMAL,
        category: Optional[EventCategory] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> UUID:
        """Subscribe to events with priority and category"""
        subscription = EventSubscription(
            id=uuid4(),
            event_type=event_type,
            callback=callback,
            priority=priority,
            category=category,
            filters=filters or {}
        )
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = []
        self._subscriptions[event_type].append(subscription)
        self.logger.info("New subscription added for event type '%s' with id %s", event_type, subscription.id)
        self.logger.success("Subscription %s for event type '%s' registered successfully.", subscription.id, event_type)
        return subscription.id

    def unsubscribe(self, subscription_id: UUID) -> bool:
        """Unsubscribe from events"""
        for subs in self._subscriptions.values():
            for sub in subs:
                if sub.id == subscription_id:
                    sub.is_active = False
                    self.logger.info("Unsubscribed subscription id %s", subscription_id)
                    self.logger.success("Subscription %s unsubscribed successfully.", subscription_id)
                    return True
        self.logger.warning("Subscription id %s not found for unsubscription", subscription_id)
        return False

    async def start_event_chain(
        self,
        category: EventCategory,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UUID:
        """Start a new event chain"""
        chain_id = uuid4()
        chain = EventChain(
            id=chain_id,
            category=category,
            metadata=metadata or {}
        )
        self._event_chains[chain_id] = chain
        self._active_chains.add(chain_id)
        self.logger.info("Started new event chain %s for category %s", chain_id, category.value)
        self.logger.success("Event chain %s started successfully.", chain_id)
        return chain_id

    async def complete_event_chain(self, chain_id: UUID) -> None:
        """Mark an event chain as completed"""
        if chain_id in self._event_chains:
            self._event_chains[chain_id].completed = True
            self._active_chains.remove(chain_id)
            self.logger.info("Completed event chain %s", chain_id)
            self.logger.success("Event chain %s completed successfully.", chain_id)

    async def _add_to_chain(self, chain_id: UUID, event_data: Dict[str, Any]) -> None:
        """Add event to a chain"""
        if chain_id in self._event_chains:
            chain = self._event_chains[chain_id]
            chain.events.append(event_data)
            self.logger.debug("Added event %s to chain %s", event_data.get("id"), chain_id)

    async def _notify_subscriber(
        self,
        subscription: EventSubscription,
        event_data: Dict[str, Any]
    ) -> None:
        """Notify a subscriber of an event"""
        try:
            if asyncio.iscoroutinefunction(subscription.callback):
                await subscription.callback(event_data)
            else:
                subscription.callback(event_data)
            self.logger.debug("Notified subscriber %s for event %s", subscription.id, event_data.get("id"))
        except Exception as e:
            self.logger.error("Error notifying subscriber %s: %s", subscription.id, str(e))

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
        self.logger.debug("Recorded event %s", event_data.get("id"))
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)

    def get_event_history(
        self,
        event_type: Optional[str] = None,
        category: Optional[EventCategory] = None,
        chain_id: Optional[UUID] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get filtered event history"""
        self.logger.debug("Retrieving event history with filters: event_type=%s, category=%s, chain_id=%s", event_type, category, chain_id)
        history = self._event_history
        
        if event_type:
            history = [e for e in history if e["type"] == event_type]
        if category:
            history = [e for e in history if e["category"] == category.value]
        if chain_id:
            history = [e for e in history if e["chain_id"] == str(chain_id)]
        if start_time:
            history = [e for e in history if datetime.fromisoformat(e["timestamp"]) >= start_time]
        if end_time:
            history = [e for e in history if datetime.fromisoformat(e["timestamp"]) <= end_time]
        if limit:
            history = history[-limit:]
        return history

    def get_active_chains(self) -> List[EventChain]:
        """Get all active event chains"""
        self.logger.debug("Retrieving active event chains.")
        return [self._event_chains[chain_id] for chain_id in self._active_chains]

    def get_chain_events(self, chain_id: UUID, include_metadata: bool = False) -> Optional[List[Dict[str, Any]]]:
        """Get all events in a chain"""
        chain = self._event_chains.get(chain_id)
        if not chain:
            self.logger.warning("No chain found for id %s", chain_id)
            return None
        if include_metadata:
            return chain.events
        return [{k: v for k, v in event.items() if k != "metadata"} for event in chain.events]

    def analyze_event_patterns(self, category: Optional[EventCategory] = None, window_minutes: int = 60) -> Dict[str, Any]:
        """Analyze event patterns"""
        self.logger.debug("Analyzing event patterns for category %s over the last %d minutes", category.value if category else "all", window_minutes)
        window_start = datetime.now() - timedelta(minutes=window_minutes)
        events = [e for e in self._event_history if datetime.fromisoformat(e["timestamp"]) >= window_start and (not category or e["category"] == category.value)]
        analysis = {
            "total_events": len(events),
            "events_by_type": self._count_by_field(events, "type"),
            "events_by_priority": self._count_by_field(events, "priority"),
            "average_chain_length": self._calculate_avg_chain_length(events),
            "common_sequences": self._find_common_sequences(events)
        }
        self.logger.info("Event pattern analysis complete: %s", analysis)
        self.logger.success("Event pattern analysis completed successfully.")
        return analysis

    def _count_by_field(self, events: List[Dict[str, Any]], field: str) -> Dict[str, int]:
        """Count events by field value"""
        counts = {}
        for event in events:
            value = str(event.get(field, "unknown"))
            counts[value] = counts.get(value, 0) + 1
        return counts

    def _calculate_avg_chain_length(self, events: List[Dict[str, Any]]) -> float:
        """Calculate average event chain length"""
        chain_lengths = {}
        for event in events:
            if event["chain_id"]:
                chain_lengths[event["chain_id"]] = chain_lengths.get(event["chain_id"], 0) + 1
        if not chain_lengths:
            return 0
        return sum(chain_lengths.values()) / len(chain_lengths)

    def _find_common_sequences(self, events: List[Dict[str, Any]], sequence_length: int = 3) -> List[List[str]]:
        """Find common event type sequences"""
        sequences = []
        current_sequence = []
        for event in events:
            current_sequence.append(event["type"])
            if len(current_sequence) >= sequence_length:
                sequences.append(current_sequence[-sequence_length:])
        sequence_counts = {}
        for seq in sequences:
            key = tuple(seq)
            sequence_counts[key] = sequence_counts.get(key, 0) + 1
        common = [list(seq) for seq, count in sorted(sequence_counts.items(), key=lambda x: x[1], reverse=True)[:5]]
        self.logger.debug("Common event sequences: %s", common)
        return common
