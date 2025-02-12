# ..\..\cmate\core\state_manager.py
# cmate/core/state_manager.py
"""
cmate/core/state_manager.py

Enhanced state manager with navigation states and context handling.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional, Set
from enum import Enum
from dataclasses import dataclass, field
from uuid import UUID, uuid4

# File for persisting state history
STATE_HISTORY_FILE = Path("temp/state_history.json")

class AgentState(Enum):
    # Basic states
    IDLE = "idle"
    ERROR = "error"
    WAITING_USER = "waiting_user"
    CONTEXT_SWITCHING = "context_switching"
    SHUTDOWN = "shutdown"

    # Analysis states
    ANALYZING = "analyzing"
    PLANNING = "planning"

    # Navigation states
    NAVIGATING = "navigating"
    SCANNING_WORKSPACE = "scanning_workspace"
    ANALYZING_COMPONENT = "analyzing_component"
    ANALYZING_DEPENDENCIES = "analyzing_dependencies"
    PATH_TRANSITIONING = "path_transitioning"

    # Implementation states
    IMPLEMENTING = "implementing"
    CODING = "coding"
    WRITING_TESTS = "writing_tests"
    
    # Testing states
    TESTING = "testing"
    VALIDATING = "validating"
    
    # Embedding and special states
    EMBEDDING = "embedding"
    RECOVERY = "recovery"

@dataclass
class NavigationStateContext:
    """Context specific for navigation states"""
    current_path: Optional[Path] = None
    target_path: Optional[Path] = None
    components_analyzed: Set[Path] = field(default_factory=set)
    dependency_chain: List[Path] = field(default_factory=list)
    navigation_history: List[str] = field(default_factory=list)

@dataclass
class StateMetadata:
    """Extended metadata for state tracking"""
    last_user_request: Optional[str] = None
    current_task: Optional[str] = None
    error_count: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    navigation_context: Optional[NavigationStateContext] = None

@dataclass
class StateTransition:
    """Information about state transition"""
    from_state: AgentState
    to_state: AgentState
    timestamp: datetime
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContextWindow:
    """Context window with token tracking"""
    content: List[Dict[str, Any]] = field(default_factory=list)
    total_tokens: int = 0
    max_tokens: int = 60000

    def add_content(self, content: Dict[str, Any], token_count: int) -> bool:
        """Add content to the context window"""
        if self.total_tokens + token_count > self.max_tokens:
            self._trim_context(token_count)
        self.content.append({
            "data": content,
            "tokens": token_count,
            "timestamp": datetime.now().isoformat()
        })
        self.total_tokens += token_count
        return True

    def _trim_context(self, needed_tokens: int) -> None:
        """Trim context to make room for new tokens"""
        items = sorted(self.content, key=lambda x: x["timestamp"])
        freed_tokens = 0
        while items and self.total_tokens - freed_tokens + needed_tokens > self.max_tokens:
            removed = items.pop(0)
            freed_tokens += removed["tokens"]
        self.total_tokens -= freed_tokens
        self.content = items

class StateManager:
    """
    Enhanced state manager with navigation support.
    
    Features:
    - Validated state transitions
    - Navigation context tracking
    - State history and persistence
    - Observer notifications
    - Context window management
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_state: AgentState = AgentState.IDLE
        self.metadata: StateMetadata = StateMetadata(
            navigation_context=NavigationStateContext()
        )
        self.context_window: ContextWindow = ContextWindow()
        self.state_history: List[Dict[str, Any]] = []
        self.transition_history: List[StateTransition] = []
        self.active_files: List[str] = []
        self.temporary_memory: Dict[str, Any] = {}
        self.observers: List[Callable[[Dict[str, Any]], None]] = []
        
        self.valid_transitions = self._initialize_valid_transitions()
        self._load_state_history()
        self.logger.success("StateManager initialized successfully.")

    def _initialize_valid_transitions(self) -> Dict[AgentState, Set[AgentState]]:
        """Initialize valid state transitions"""
        transitions = {}
        for state in AgentState:
            transitions[state] = set()

        transitions[AgentState.IDLE].update([AgentState.SCANNING_WORKSPACE, AgentState.ANALYZING, AgentState.NAVIGATING])
        transitions[AgentState.SCANNING_WORKSPACE].update([AgentState.ANALYZING_COMPONENT, AgentState.ERROR])
        transitions[AgentState.ANALYZING_COMPONENT].update([AgentState.ANALYZING_DEPENDENCIES, AgentState.IMPLEMENTING, AgentState.ERROR])
        transitions[AgentState.ANALYZING_DEPENDENCIES].update([AgentState.PATH_TRANSITIONING, AgentState.IMPLEMENTING, AgentState.ERROR])
        transitions[AgentState.PATH_TRANSITIONING].update([AgentState.ANALYZING_COMPONENT, AgentState.IMPLEMENTING, AgentState.ERROR])
        transitions[AgentState.ANALYZING].update([AgentState.ERROR, AgentState.IDLE])
        transitions[AgentState.IMPLEMENTING].update([AgentState.CODING, AgentState.WRITING_TESTS, AgentState.ERROR])
        transitions[AgentState.CODING].update([AgentState.TESTING, AgentState.WRITING_TESTS, AgentState.ERROR])
        transitions[AgentState.WRITING_TESTS].update([AgentState.TESTING, AgentState.ERROR])
        transitions[AgentState.ERROR].update([AgentState.RECOVERY, AgentState.IDLE])
        transitions[AgentState.RECOVERY].update([state for state in AgentState if state not in {AgentState.ERROR, AgentState.SHUTDOWN}])
        
        self.logger.debug("Initialized valid state transitions: %s", transitions)
        return transitions

    def update_state(self, new_state: AgentState, metadata: Optional[Dict[str, Any]] = None, reason: Optional[str] = None) -> None:
        """Update agent state with validation and navigation tracking"""
        self.logger.debug("Attempting to update state from %s to %s with metadata: %s and reason: %s",
                          self.current_state.value, new_state.value, metadata, reason)
        if not self._is_valid_transition(new_state):
            error_msg = f"Invalid state transition from {self.current_state.value} to {new_state.value}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        transition = StateTransition(
            from_state=self.current_state,
            to_state=new_state,
            timestamp=datetime.now(),
            reason=reason or "State update requested",
            metadata=metadata or {}
        )
        self.transition_history.append(transition)
        self.logger.debug("Recorded state transition: %s", transition)

        if metadata:
            self._update_navigation_context(new_state, metadata)

        old_state = self.current_state
        self.current_state = new_state
        self.metadata.last_updated = datetime.now()

        if metadata:
            if "user_request" in metadata:
                self.metadata.last_user_request = metadata["user_request"]
            if "current_task" in metadata:
                self.metadata.current_task = metadata["current_task"]

        self._record_state_change(new_state, metadata)
        self._notify_observers({
            "type": "state_changed",
            "old_state": old_state.value,
            "new_state": new_state.value,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        })
        self.logger.success("State updated successfully from %s to %s", old_state.value, new_state.value)

    def _update_navigation_context(self, new_state: AgentState, metadata: Dict[str, Any]) -> None:
        """Update navigation context based on state change"""
        if not self.metadata.navigation_context:
            self.metadata.navigation_context = NavigationStateContext()
        nav_context = self.metadata.navigation_context

        if "current_path" in metadata:
            nav_context.current_path = Path(metadata["current_path"])
        if "target_path" in metadata:
            nav_context.target_path = Path(metadata["target_path"])

        if new_state == AgentState.ANALYZING_COMPONENT and nav_context.current_path:
            nav_context.components_analyzed.add(nav_context.current_path)
            self.logger.debug("Added to components_analyzed: %s", nav_context.current_path)

        if new_state == AgentState.ANALYZING_DEPENDENCIES:
            if "dependencies" in metadata:
                nav_context.dependency_chain = [Path(p) for p in metadata["dependencies"]]
                self.logger.debug("Updated dependency_chain: %s", nav_context.dependency_chain)

        nav_context.navigation_history.append(f"{datetime.now().isoformat()}: {new_state.value}")
        self.logger.debug("Updated navigation history: %s", nav_context.navigation_history)

    def _is_valid_transition(self, new_state: AgentState) -> bool:
        """Check if state transition is valid"""
        if self.current_state == AgentState.RECOVERY:
            return True
        is_valid = new_state in self.valid_transitions[self.current_state]
        self.logger.debug("Transition from %s to %s is valid: %s", self.current_state.value, new_state.value, is_valid)
        return is_valid

    def get_navigation_context(self) -> Optional[NavigationStateContext]:
        """Get current navigation context"""
        return self.metadata.navigation_context

    def get_navigation_history(self) -> List[str]:
        """Get navigation history"""
        if self.metadata.navigation_context:
            return self.metadata.navigation_context.navigation_history
        return []

    def add_to_context(self, content: Dict[str, Any], token_count: int) -> bool:
        """Add content to context window"""
        result = self.context_window.add_content(content, token_count)
        self.logger.debug("Added content to context window. New total tokens: %d", self.context_window.total_tokens)
        return result

    def get_current_context(self) -> List[Dict[str, Any]]:
        """Get current context window content"""
        return [item["data"] for item in self.context_window.content]

    def register_observer(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register observer for state changes"""
        self.observers.append(callback)
        self.logger.debug("Registered a new observer.")

    def _notify_observers(self, state_entry: Dict[str, Any]) -> None:
        """Notify all observers"""
        for callback in self.observers:
            try:
                callback(state_entry)
            except Exception as e:
                self.logger.error("Error notifying observer: %s", str(e))

    def _record_state_change(self, state: AgentState, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record state change and persist"""
        entry = {
            "state": state.value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "error_count": self.metadata.error_count
        }
        self.state_history.append(entry)
        self.logger.debug("Recorded state change: %s", entry)
        self._persist_state_history()

    def _persist_state_history(self) -> None:
        """Persist state history to file"""
        try:
            if not STATE_HISTORY_FILE.parent.exists():
                STATE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(STATE_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.state_history, f, indent=2)
            self.logger.debug("Persisted state history to file: %s", STATE_HISTORY_FILE)
        except Exception as e:
            self.logger.error("Error persisting state history: %s", str(e))

    def _load_state_history(self) -> None:
        """Load state history from file"""
        if STATE_HISTORY_FILE.exists():
            try:
                with open(STATE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.state_history = json.load(f)
                self.logger.success("State history loaded successfully.")
            except Exception as e:
                self.logger.error("Error loading state history: %s", str(e))

    def get_state_statistics(self) -> Dict[str, Any]:
        """Get statistics about state transitions"""
        stats = {
            "total_transitions": len(self.transition_history),
            "state_counts": {},
            "average_state_duration": {},
            "error_rate": 0,
            "most_common_transitions": self._get_common_transitions()
        }
        
        for transition in self.transition_history:
            stats["state_counts"][transition.from_state.value] = stats["state_counts"].get(transition.from_state.value, 0) + 1
            if transition.to_state == AgentState.ERROR:
                stats["error_rate"] += 1
        
        if self.transition_history:
            stats["error_rate"] /= len(self.transition_history)
        
        self.logger.debug("State statistics: %s", stats)
        return stats

    def _get_common_transitions(self) -> Dict[str, int]:
        """Get most common state transitions"""
        transition_counts = {}
        for transition in self.transition_history:
            key = f"{transition.from_state.value} -> {transition.to_state.value}"
            transition_counts[key] = transition_counts.get(key, 0) + 1
        common = dict(sorted(transition_counts.items(), key=lambda x: x[1], reverse=True)[:5])
        self.logger.debug("Common transitions: %s", common)
        return common

    def clear_state_history(self) -> None:
        """Clear the state history in memory and on disk."""
        self.state_history.clear()
        if STATE_HISTORY_FILE.exists():
            STATE_HISTORY_FILE.unlink()
        self.logger.success("Cleared state history successfully.")
