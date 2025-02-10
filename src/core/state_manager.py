# src/core/state_manager.py
"""
state_manager.py

Hanterar agentens state, sparar historik och medger observerande.
Här definieras även AgentState som nu inkluderar extra states:
CODING, WRITING_TESTS, EMBEDDING och NAVIGATION.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional
from enum import Enum
from dataclasses import dataclass, field

# Fil för att spara state-historiken
STATE_HISTORY_FILE = Path("temp/state_history.json")


class AgentState(Enum):
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    TESTING = "testing"
    CODING = "coding"
    WRITING_TESTS = "writing_tests"
    EMBEDDING = "embedding"
    NAVIGATION = "navigation"
    ERROR = "error"
    WAITING_USER = "waiting_user"
    CONTEXT_SWITCHING = "context_switching"


@dataclass
class StateMetadata:
    """Metadata for tracking state details."""
    last_user_request: Optional[str] = None
    current_task: Optional[str] = None
    error_count: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class ContextWindow:
    """Enkel context window för att lagra content och hålla koll på token-antal."""
    content: List[Dict[str, Any]] = field(default_factory=list)
    total_tokens: int = 0
    max_tokens: int = 60000

    def add_content(self, content: Dict[str, Any], token_count: int) -> bool:
        """
        Lägger till nytt content i contexten och ökar total_tokens.
        Trimmar vid behov om vi överskrider max_tokens.
        """
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
        """
        Trimmar bort äldsta content i context-fönstret 
        tills vi har plats för needed_tokens.
        """
        while self.content and self.total_tokens + needed_tokens > self.max_tokens:
            removed = self.content.pop(0)
            self.total_tokens -= removed["tokens"]


class StateManager:
    """
    Hanterar agentens state.

    - Håller koll på current_state (AgentState)
    - Sparar state-historik (state_history)
    - Håller en context_window där man kan lägga in content (t.ex. promptar)
    - Har stöd för observer-pattern (så man kan lyssna på stateförändringar)
    - Vid uppdatering av state så sparas detta i en JSON-fil (STATE_HISTORY_FILE)
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_state: AgentState = AgentState.IDLE
        self.metadata: StateMetadata = StateMetadata()
        self.context_window: ContextWindow = ContextWindow()
        self.state_history: List[Dict[str, Any]] = []
        self.active_files: List[str] = []
        self.temporary_memory: Dict[str, Any] = {}
        self.observers: List[Callable[[Dict[str, Any]], None]] = []
        self._load_state_history()

    def update_state(self, new_state: AgentState, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Uppdaterar agentens nuvarande state och kan även ta emot valfri metadata.
        Ex: update_state(AgentState.CODING, {"user_request": "Skapa en ny funktion"})
        """
        self.current_state = new_state
        self.metadata.last_updated = datetime.now()

        if metadata:
            if "user_request" in metadata:
                self.metadata.last_user_request = metadata["user_request"]
            if "current_task" in metadata:
                self.metadata.current_task = metadata["current_task"]

        # Logga och spara i historiken
        self._record_state_change(new_state, metadata)
        # Notifiera eventuella observers
        self._notify_observers(self.state_history[-1])
        self.logger.info(f"State updated to {new_state.value} with metadata: {metadata}")

    def add_to_context(self, content: Dict[str, Any], token_count: int) -> bool:
        """Lägg till content i context-fönstret."""
        return self.context_window.add_content(content, token_count)

    def update_active_files(self, files: List[str]) -> None:
        """Uppdaterar listan med aktiva filer som agenten jobbar med."""
        self.active_files = files
        self._record_state_change(self.current_state, {"active_files": files})
        self._notify_observers(self.state_history[-1])
        self.logger.info(f"Active files updated: {files}")

    def record_error(self, error: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Logga ett fel och sätt agentens state till ERROR.
        error: Strängbeskrivning av felet.
        context: Ev. extra info.
        """
        self.metadata.error_count += 1
        error_data = {
            "error": error,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "state": self.current_state.value
        }
        # Registrera state = ERROR i historiken
        self._record_state_change(AgentState.ERROR, error_data)
        self._notify_observers(self.state_history[-1])
        self.logger.error(f"Error recorded: {error} with context: {context}")

    def get_current_context(self) -> List[Dict[str, Any]]:
        """
        Hämtar nuvarande contextfönstrets content.
        Returnerar en lista med dictionary (data + tokens + timestamp).
        """
        return [item["data"] for item in self.context_window.content]

    def register_observer(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Registrera en observer-funktion som anropas vid state-förändringar."""
        self.observers.append(callback)

    def _notify_observers(self, state_entry: Dict[str, Any]) -> None:
        """Kör observer-callbacks med den nya state_entryn."""
        for callback in self.observers:
            try:
                callback(state_entry)
            except Exception as e:
                self.logger.error(f"Error notifying observer: {str(e)}")

    def _record_state_change(self, state: AgentState, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Lagra en stateändring i self.state_history och
        persistera sedan genom _persist_state_history().
        """
        entry = {
            "state": state.value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "error_count": self.metadata.error_count
        }
        self.state_history.append(entry)
        self._persist_state_history()

    def _persist_state_history(self) -> None:
        """
        Sparar self.state_history i en JSON-fil (STATE_HISTORY_FILE).
        Skapar katalogen om den inte finns.
        """
        try:
            if not STATE_HISTORY_FILE.parent.exists():
                STATE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(STATE_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.state_history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error persisting state history: {str(e)}")

    def _load_state_history(self) -> None:
        """Ladda tidigare state_history från JSON-fil om den existerar."""
        if STATE_HISTORY_FILE.exists():
            try:
                with open(STATE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.state_history = json.load(f)
                self.logger.info("State history loaded successfully.")
            except Exception as e:
                self.logger.error(f"Error loading state history: {str(e)}")
