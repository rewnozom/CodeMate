# src/core/state_manager.py
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Callable

STATE_HISTORY_FILE = Path("temp/state_history.json")

class StateManager:
    """
    Manages the agent's state.
    
    Maintains a current state, persists state history, and notifies registered observers on state changes.
    """
    def __init__(self):
        self.current_state: str = "idle"
        self.state_history: List[Dict[str, Any]] = []
        self.observers: List[Callable[[Dict[str, Any]], None]] = []
        self.logger = logging.getLogger(__name__)
        # Load persisted state history if available
        self._load_state_history()

    def update_state(self, new_state: str, metadata: Dict[str, Any] = None) -> None:
        """
        Update the current state with optional metadata.
        Guard against transitioning from an 'error' state to 'processing'
        unless explicitly allowed via metadata (e.g., {"reset": True}).
        """
        metadata = metadata or {}
        if self.current_state == "error" and new_state == "processing" and not metadata.get("reset", False):
            self.logger.warning("Attempted transition from error to processing without reset flag; ignoring update.")
            return

        timestamp = datetime.now().isoformat()
        state_entry = {
            "state": new_state,
            "timestamp": timestamp,
            "metadata": metadata
        }
        self.current_state = new_state
        self.state_history.append(state_entry)
        self.logger.info(f"State updated to '{new_state}' at {timestamp} with metadata: {metadata}")
        self._persist_state_history()
        self._notify_observers(state_entry)

    def get_state(self) -> str:
        """Return the current state."""
        return self.current_state

    def get_state_history(self) -> List[Dict[str, Any]]:
        """Return the history of state changes."""
        return self.state_history

    def register_observer(self, observer_callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback to be notified when state changes."""
        self.observers.append(observer_callback)

    def _notify_observers(self, state_entry: Dict[str, Any]) -> None:
        """Notify all registered observers of a state change."""
        for callback in self.observers:
            try:
                callback(state_entry)
            except Exception as e:
                self.logger.error(f"Error notifying observer: {str(e)}")

    def _persist_state_history(self) -> None:
        """Persist the state history to a JSON file."""
        try:
            if not STATE_HISTORY_FILE.parent.exists():
                STATE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(STATE_HISTORY_FILE, 'w') as f:
                json.dump(self.state_history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error persisting state history: {str(e)}")

    def _load_state_history(self) -> None:
        """Load state history from a JSON file, if available."""
        if STATE_HISTORY_FILE.exists():
            try:
                with open(STATE_HISTORY_FILE, 'r') as f:
                    self.state_history = json.load(f)
                    if self.state_history:
                        self.current_state = self.state_history[-1]["state"]
            except Exception as e:
                self.logger.error(f"Error loading state history: {str(e)}")
