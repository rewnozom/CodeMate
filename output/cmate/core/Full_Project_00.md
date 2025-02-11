# Project Details

# Table of Contents
- [..\cmate\core\agent_coordinator.py](#-cmate-core-agent_coordinatorpy)
- [..\cmate\core\context_manager.py](#-cmate-core-context_managerpy)
- [..\cmate\core\event_bus.py](#-cmate-core-event_buspy)
- [..\cmate\core\memory_manager.py](#-cmate-core-memory_managerpy)
- [..\cmate\core\prompt_manager.py](#-cmate-core-prompt_managerpy)
- [..\cmate\core\state_manager.py](#-cmate-core-state_managerpy)
- [..\cmate\core\workflow_manager.py](#-cmate-core-workflow_managerpy)
- [..\cmate\core\__init__.py](#-cmate-core-__init__py)


# ..\..\cmate\core\agent_coordinator.py
## File: ..\..\cmate\core\agent_coordinator.py

```py
# ..\..\cmate\core\agent_coordinator.py
"""
src/core/agent_coordinator.py

Main Agent Module (Main_Agent)

This module integrates and orchestrates all subsystems of the CodeMate Project:
  - LLM integration: Provides language model capabilities via llm_agent, llm_manager, conversation_manager, etc.
  - State and Workflow Management: Manages the current state (with transitions, validations, and recovery)
    and orchestrates workflows using WorkflowManager.
  - Prompt Management: Loads and formats prompts for guiding the agent’s behavior.
  - Memory and Context: Manages short- and long-term memory and organizes context for LLM interactions.
  - Event Bus: Publishes and subscribes to events across the system.
  - Request/Response: Provides a unified interface for handling requests and formatting responses.
  - Terminal: Provides command execution and session management.
  - Storage: Manages caches and persistent storage.
  - Task Management: Handles checklists, process management, progress tracking, and task prioritization.
  - Utilities: Logging, prompt templates, system metrics, token counting, log analysis.
  - Validation: Backend, frontend, implementation validation and test management.
  - Error Handling: Centralized error tracking, reporting, and recovery.

In addition to the basic functions, this module implements extra helper methods to:
  - Refresh LLM context from memory.
  - Generate new code based on prompts.
  - Visualize the current workflow.
  - Integrate with external systems such as Git.
  - Run system diagnostics.
  - Update configuration dynamically.
  - Persist audit logs.
  - Execute code modifications in a complete workflow cycle.

This module also implements a recovery mechanism (_attempt_recovery) that utilizes the ErrorHandler to
log errors and attempt a recovery strategy.
"""

import asyncio
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Callable, List, Optional

# --------------------------------------------------
# Import core subsystems
# --------------------------------------------------
from ..core.state_manager import StateManager, AgentState
from ..core.workflow_manager import WorkflowManager
from ..core.prompt_manager import PromptManager
from ..core.memory_manager import MemoryManager
from ..core.event_bus import EventBus
from ..core.context_manager import ContextManager

# --------------------------------------------------
# Import LLM-related modules (assumed complete)
# --------------------------------------------------
from ..llm.llm_agent import llm_agent
from ..llm.llm_manager import llm_manager
from ..llm.conversation import conversation_manager

# --------------------------------------------------
# Import interface modules
# --------------------------------------------------
from ..interfaces.request_handler import RequestHandler
from ..interfaces.response_formatter import ResponseFormatter
from ..interfaces.terminal_manager import TerminalManager

# --------------------------------------------------
# Import storage modules
# --------------------------------------------------
from ..storage.cache_manager import CacheManager
from ..storage.persistence_manager import PersistenceManager

# --------------------------------------------------
# Import task management modules
# --------------------------------------------------
from ..task_management.checklist_manager import ChecklistManager
from ..task_management.process_manager import ProcessManager
from ..task_management.progress_tracker import ProgressTracker
from ..task_management.task_prioritizer import TaskPrioritizer

# --------------------------------------------------
# Import utility modules
# --------------------------------------------------
from ..utils.logger import get_logger
from ..utils.prompt_templates import PromptTemplateManager
from ..utils.system_metrics import MetricsCollector
from ..utils.token_counter import TokenCounter
from ..utils.log_analyzer import LogAnalyzer
from ..utils.error_handler import ErrorHandler, ErrorSeverity

# --------------------------------------------------
# Import validation modules
# --------------------------------------------------
from ..validation.backend_validator import BackendValidator
from ..validation.frontend_validator import FrontendValidator
from ..validation.implementation_validator import ImplementationValidator
from ..validation.test_manager import TestManager
from ..validation.validation_rules import ValidationRules


# --------------------------------------------------
# Data class for agent configuration
# --------------------------------------------------
@dataclass
class AgentConfig:
    """
    Configuration for the AgentCoordinator.
    
    Attributes:
        workspace_path (str): The directory where the agent operates.
        max_files_per_scan (int): Maximum number of files to process per workspace scan.
        context_window_size (int): Maximum token count for context windows.
        auto_test (bool): Whether to run automated tests after operations.
        debug_mode (bool): Enable debug-level logging and additional diagnostics.
    """
    workspace_path: str = "./Workspace"
    max_files_per_scan: int = 10
    context_window_size: int = 60000
    auto_test: bool = True
    debug_mode: bool = False
    # Additional configuration fields can be added here as needed.


# --------------------------------------------------
# Main AgentCoordinator class that integrates everything.
# --------------------------------------------------
class AgentCoordinator:
    """
    Main Agent Integration Module.
    
    This class is the central orchestrator of the system. It is responsible for:
      - Processing incoming requests and delegating them to proper subsystems.
      - Coordinating workflows and managing state transitions.
      - Integrating LLM services, prompt management, memory and context management.
      - Handling events, errors, logging, and system metrics.
      - Integrating storage and task management systems.
      - Supporting external integrations and dynamic configuration updates.
    
    In addition, it provides helper methods for code generation, workflow visualization,
    system diagnostics, and persistent audit logging.
    """

    def __init__(
        self,
        config: AgentConfig,
        state_manager: StateManager,
        workflow_manager: WorkflowManager
    ):
        """
        Initialize the AgentCoordinator with configuration and core modules.
        
        Args:
            config (AgentConfig): The agent configuration settings.
            state_manager (StateManager): Manages the agent's current state and history.
            workflow_manager (WorkflowManager): Manages creation and execution of workflows.
        """
        self.config = config
        self.state_manager = state_manager
        self.workflow_manager = workflow_manager
        self.logger = get_logger(__name__)
        self.start_time = datetime.now()

        # Audit log to record processed requests.
        self.audit_log: List[Dict[str, Any]] = []

        # Subscribers for agent events.
        self.event_subscribers: List[Callable[[Dict[str, Any]], None]] = []

        # --------------------------------------------------
        # Initialize additional subsystems
        # --------------------------------------------------
        self.prompt_manager = PromptManager()               # Handles prompt formatting and loading.
        self.memory_manager = MemoryManager()               # Manages short-, working-, and long-term memory.
        self.context_manager = ContextManager(max_tokens=config.context_window_size)
        self.event_bus = EventBus()                         # Global event distribution system.
        
        self.request_handler = RequestHandler(self.state_manager, self.workflow_manager)
        self.response_formatter = ResponseFormatter()
        self.terminal_manager = TerminalManager(workspace_path=config.workspace_path)

        self.cache_manager = CacheManager()
        self.persistence_manager = PersistenceManager()

        self.checklist_manager = ChecklistManager()
        self.process_manager = ProcessManager(workspace_path=config.workspace_path)
        self.progress_tracker = ProgressTracker()
        self.task_prioritizer = TaskPrioritizer()

        self.metrics_collector = MetricsCollector()
        self.token_counter = TokenCounter()
        self.log_analyzer = LogAnalyzer()

        self.error_handler = ErrorHandler()

        self.backend_validator = BackendValidator()
        self.frontend_validator = FrontendValidator()
        self.implementation_validator = ImplementationValidator()
        self.test_manager = TestManager()
        self.validation_rules = ValidationRules()

        # --------------------------------------------------
        # LLM Integration – using singleton instances.
        # --------------------------------------------------
        self.llm_agent = llm_agent
        self.llm_manager = llm_manager
        self.conversation = conversation_manager

        # Prompt templates manager for dynamic prompt loading.
        self.prompt_template_manager = PromptTemplateManager()

        # Subscribe to state change events via the event bus.
        self.event_bus.subscribe("state_changed", self._handle_state_change)

        self.logger.info("AgentCoordinator initialized with all subsystems integrated.")

    # --------------------------------------------------
    # Event subscription and publishing
    # --------------------------------------------------
    def subscribe_event(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Subscribe an external callback to receive agent events.
        
        Args:
            callback (Callable[[Dict[str, Any]], None]): A function that receives event data.
        """
        self.event_subscribers.append(callback)
        self.logger.debug("New event subscriber added.")

    def _publish_event(self, event: Dict[str, Any]) -> None:
        """
        Publish an event to all local subscribers and the global EventBus.
        
        Args:
            event (Dict[str, Any]): A dictionary containing event information.
        """
        for callback in self.event_subscribers:
            try:
                callback(event)
            except Exception as e:
                self.logger.error(f"Error in event subscriber callback: {str(e)}")
        asyncio.create_task(self.event_bus.publish(event.get("event", "unknown"), event))
        self.logger.debug(f"Event published: {event.get('event', 'unknown')}")

    # --------------------------------------------------
    # Request processing
    # --------------------------------------------------
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming request by updating state, logging, and delegating to the RequestHandler.
        
        The request must include:
          - 'type': A string indicating the type of the request.
          - 'data': A dictionary containing request-specific data.
        
        Returns:
            A dictionary with keys 'success', 'result' (if successful) or 'error' (if not), and 'request_id'.
        """
        request_id = str(uuid.uuid4())
        self.audit_log.append({
            "request_id": request_id,
            "request": request,
            "timestamp": datetime.now().isoformat()
        })
        self.logger.info(f"Processing request {request_id}: {request}")

        try:
            request_type = request.get("type")
            data = request.get("data", {})

            if not request_type:
                raise ValueError("Request must contain a 'type' field.")

            # Update state to processing.
            self.state_manager.update_state(AgentState.ANALYZING, {"request_id": request_id, "request_type": request_type})

            self._publish_event({
                "event": "request_started",
                "request_id": request_id,
                "request_type": request_type,
                "timestamp": datetime.now().isoformat()
            })

            # Delegate to RequestHandler.
            result = await self.request_handler.handle_request(request)

            # Update state to idle.
            self.state_manager.update_state(AgentState.IDLE, {"last_request": request_type})
            self._publish_event({
                "event": "request_completed",
                "request_id": request_id,
                "request_type": request_type,
                "timestamp": datetime.now().isoformat(),
                "result": result.data
            })

            self.logger.info(f"Request {request_id} processed successfully.")
            return {"success": True, "result": result.data, "request_id": request_id}

        except Exception as e:
            self.logger.error(f"Error processing request {request_id}: {str(e)}")
            self.state_manager.update_state(AgentState.ERROR, {"request_id": request_id, "error": str(e)})
            self._publish_event({
                "event": "request_failed",
                "request_id": request_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            recovered = await self._attempt_recovery(e, {"request_id": request_id})
            return {"success": False, "error": str(e), "recovered": recovered, "request_id": request_id}

    # --------------------------------------------------
    # Error recovery method
    # --------------------------------------------------
    async def _attempt_recovery(self, error: Exception, context: Dict[str, Any]) -> bool:
        """
        Attempt to recover from an error using the ErrorHandler.
        
        Logs the error, calls the recovery strategies, and updates the state if successful.
        
        Args:
            error (Exception): The exception to recover from.
            context (Dict[str, Any]): Additional context for the error.
        
        Returns:
            True if recovery was attempted successfully; otherwise, False.
        """
        try:
            recovery_report = self.error_handler.handle_error(error, severity=ErrorSeverity.ERROR, metadata=context)
            if recovery_report and recovery_report.recovery_steps:
                self.logger.info("Recovery attempted with steps: " + ", ".join(recovery_report.recovery_steps))
                self.state_manager.update_state(AgentState.IDLE, {"recovered": True})
                return True
        except Exception as recovery_error:
            self.logger.error(f"Recovery attempt failed: {str(recovery_error)}")
        return False

    # --------------------------------------------------
    # Status and shutdown methods
    # --------------------------------------------------
    async def check_status(self) -> Dict[str, Any]:
        """
        Retrieve the current status of the agent.
        
        Returns a dictionary containing:
          - Current state.
          - Active workflow (if any).
          - Uptime.
          - Recent audit log entries.
          - Collected system metrics.
        """
        state = self.state_manager.current_state.value
        active_workflow = self.workflow_manager.get_active_workflow()
        uptime = (datetime.now() - self.start_time).total_seconds()
        metrics = self.metrics_collector.collect_metrics().__dict__
        return {
            "state": state,
            "active_workflow": active_workflow,
            "uptime": uptime,
            "audit_log": self.audit_log[-10:],  # Last 10 entries.
            "metrics": metrics
        }

    async def shutdown(self) -> None:
        """
        Gracefully shut down the agent.
        
        This involves:
          - Logging shutdown.
          - Updating state.
          - Shutting down the WorkflowManager.
          - Publishing an "agent_shutdown" event.
        """
        self.logger.info("Shutting down agent...")
        self.state_manager.update_state(AgentState.CONTEXT_SWITCHING, {"timestamp": datetime.now().isoformat()})
        await self.workflow_manager.shutdown()
        await self.event_bus.publish("agent_shutdown", {"timestamp": datetime.now().isoformat()})
        self.state_manager.update_state(AgentState.SHUTDOWN, {"timestamp": datetime.now().isoformat()})
        self._publish_event({"event": "agent_shutdown", "timestamp": datetime.now().isoformat()})
        self.logger.info("Agent shutdown completed.")

    # --------------------------------------------------
    # Event callback handlers
    # --------------------------------------------------
    def _handle_state_change(self, event: Dict[str, Any]) -> None:
        """
        Handle state change events received via the EventBus.
        
        Args:
            event (Dict[str, Any]): The state change event.
        """
        self.logger.debug(f"Received state change event: {event}")

    # --------------------------------------------------
    # Additional Helper Methods for Extended Functionality
    # --------------------------------------------------

    async def refresh_llm_context(self) -> None:
        """
        Refresh the LLM conversation context using data from the MemoryManager and ContextManager.
        
        This method fetches relevant memory items and updates the conversation history,
        ensuring that the LLM has the most up-to-date context.
        """
        self.logger.info("Refreshing LLM context from memory and context manager...")
        # Example: retrieve recent memory items (dummy implementation)
        recent_context = self.context_manager.get_context()
        # Append each context item to the conversation history.
        for item in recent_context:
            self.conversation.add_message("system", str(item))
        self.logger.info("LLM context refreshed.")

    async def generate_code(self, prompt: str) -> str:
        """
        Generate code based on a given prompt using the LLM agent.
        
        This method calls the LLM agent's ask() method and returns the generated code.
        
        Args:
            prompt (str): A description or prompt for the desired code.
            
        Returns:
            str: The generated code (as a string).
        """
        self.logger.info("Generating code for prompt...")
        response = await self.llm_agent.ask(prompt)
        generated_code = response.get("parsed_content") or response.get("content", "")
        self.logger.info("Code generation complete.")
        return generated_code

    def visualize_workflow(self) -> str:
        """
        Generate a textual visualization of the current active workflow.
        
        This method returns a string summary (or ASCII diagram) of the workflow steps,
        their status, and any dependencies.
        
        Returns:
            str: A textual representation of the active workflow.
        """
        workflow = self.workflow_manager.get_active_workflow()
        if not workflow:
            return "No active workflow."
        # Dummy implementation: iterate through workflow steps and print details.
        lines = ["Current Active Workflow:"]
        for step in self.workflow_manager.workflows.get(workflow, {}).get("steps", []):
            line = f"Step {step.get('id')}: {step.get('type')} - Status: {step.get('completed')}"
            lines.append(line)
        visualization = "\n".join(lines)
        self.logger.debug("Workflow visualization generated.")
        return visualization

    async def integrate_with_git(self) -> Dict[str, Any]:
        """
        Simulate integration with a version control system (e.g., Git).
        
        This method checks for changes in the workspace and, if found,
        commits the changes with a generated commit message.
        
        Returns:
            Dict[str, Any]: A dictionary containing details of the git integration.
        """
        self.logger.info("Integrating with Git (simulation)...")
        # Dummy implementation – in practice, you'd call Git commands via subprocess.
        commit_message = "Auto-generated commit by CodeMate at " + datetime.now().isoformat()
        result = {
            "changes_detected": True,
            "commit_message": commit_message,
            "commit_id": str(uuid.uuid4())
        }
        self.logger.info("Git integration simulated with commit ID " + result["commit_id"])
        return result

    async def run_diagnostics(self) -> Dict[str, Any]:
        """
        Run system diagnostics including resource usage, process metrics, and log analysis.
        
        This method aggregates data from the MetricsCollector, LogAnalyzer, and
        ProcessManager, returning a comprehensive diagnostic report.
        
        Returns:
            Dict[str, Any]: A dictionary with diagnostic information.
        """
        self.logger.info("Running system diagnostics...")
        diagnostics = {}
        diagnostics["system_metrics"] = self.metrics_collector.collect_metrics().__dict__
        diagnostics["process_info"] = self.process_manager.get_active_processes()
        diagnostics["log_analysis"] = self.log_analyzer.find_error_patterns()
        self.logger.info("Diagnostics complete.")
        return diagnostics

    def update_configuration(self, new_config: Dict[str, Any]) -> None:
        """
        Dynamically update the agent's configuration.
        
        This method allows changing certain configuration parameters at runtime.
        It updates the AgentConfig object and notifies relevant subsystems of the change.
        
        Args:
            new_config (Dict[str, Any]): A dictionary with configuration keys and new values.
        """
        self.logger.info("Updating configuration...")
        for key, value in new_config.items():
            setattr(self.config, key, value)
        # Notify subsystems if necessary (e.g., update context window size)
        self.context_manager.max_tokens = self.config.context_window_size
        self.logger.info("Configuration updated.")

    def persist_audit_log(self) -> None:
        """
        Persist the audit log to persistent storage.
        
        This method writes the audit log to a file using the PersistenceManager.
        """
        self.logger.info("Persisting audit log...")
        try:
            # Here we use the persistence manager to store the audit log under a fixed key.
            self.persistence_manager.store("audit_log", self.audit_log)
            self.logger.info("Audit log persisted successfully.")
        except Exception as e:
            self.logger.error(f"Error persisting audit log: {str(e)}")

    async def execute_code_modification(self, prompt: str) -> Dict[str, Any]:
        """
        Execute a complete code modification cycle:
          1. Generate code from the given prompt.
          2. Validate the generated code using the ImplementationValidator.
          3. Run tests using the TestManager.
          4. If tests pass, integrate changes; otherwise, attempt recovery.
        
        Args:
            prompt (str): The natural language description of the desired code change.
            
        Returns:
            Dict[str, Any]: A dictionary containing the result of the modification process.
        """
        self.logger.info("Starting code modification process...")
        # Step 1: Generate code.
        generated_code = await self.generate_code(prompt)
        
        # Step 2: Validate code syntax and quality.
        validation_result = self.implementation_validator.validate_implementation(generated_code, "python")
        if not validation_result.valid:
            self.logger.error("Generated code validation failed with errors: " + ", ".join(validation_result.errors))
            return {"success": False, "error": "Validation failed", "details": validation_result.errors}
        
        # Step 3: Run tests (dummy example using TestManager).
        test_result = await self.test_manager.run_all_tests()
        diagnostics = await self.test_manager.analyze_results(test_result)
        if diagnostics.get("failed_tests", 0) > 0:
            self.logger.error("Some tests failed during code modification.")
            await self._attempt_recovery(Exception("Test failures during code modification"), {"prompt": prompt})
            return {"success": False, "error": "Tests failed", "details": diagnostics}
        
        # If all steps pass, consider the modification successful.
        self.logger.info("Code modification executed successfully.")
        return {"success": True, "generated_code": generated_code, "validation": validation_result, "tests": diagnostics}

# End of AgentCoordinator module.

```

---

# ..\..\cmate\core\context_manager.py
## File: ..\..\cmate\core\context_manager.py

```py
# ..\..\cmate\core\context_manager.py
# src/core/context_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
from uuid import UUID, uuid4

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
    """Manages agent's context window and context organization"""
    
    def __init__(self, max_tokens: int = 60000):
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.context_items: Dict[UUID, ContextItem] = {}
        self.context_groups: Dict[UUID, ContextGroup] = {}
        self.active_group: Optional[UUID] = None

    def add_context(self, 
                   content: Any,
                   type: str,
                   priority: int = 0,
                   group_id: Optional[UUID] = None,
                   token_count: Optional[int] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Add new context item"""
        # Create context item
        item = ContextItem(
            id=uuid4(),
            content=content,
            type=type,
            priority=priority,
            created_at=datetime.now(),
            metadata=metadata or {},
            token_count=token_count or self._estimate_tokens(content)
        )
        
        # Check token limit
        if not self._check_token_limit(item.token_count):
            self._trim_context(item.token_count)
            
        # Add to storage
        self.context_items[item.id] = item
        self.current_tokens += item.token_count
        
        # Add to group if specified
        if group_id and group_id in self.context_groups:
            self.context_groups[group_id].items.append(item)
            
        return item.id

    def create_group(self, name: str, priority: int = 0, metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Create new context group"""
        group = ContextGroup(
            id=uuid4(),
            name=name,
            priority=priority,
            metadata=metadata or {}
        )
        self.context_groups[group.id] = group
        return group.id

    def set_active_group(self, group_id: UUID) -> None:
        """Set active context group"""
        if group_id in self.context_groups:
            self.active_group = group_id

    def get_context(self, 
                   type: Optional[str] = None,
                   group_id: Optional[UUID] = None,
                   min_priority: int = 0) -> List[ContextItem]:
        """Get context items with optional filtering"""
        items = []
        
        if group_id:
            group = self.context_groups.get(group_id)
            if group:
                items = group.items
        else:
            items = list(self.context_items.values())
            
        # Apply filters
        filtered_items = [
            item for item in items
            if item.priority >= min_priority and
               (type is None or item.type == type)
        ]
        
        return sorted(filtered_items, key=lambda x: (-x.priority, x.created_at))

    def remove_context(self, item_id: UUID) -> bool:
        """Remove context item"""
        if item_id in self.context_items:
            item = self.context_items[item_id]
            self.current_tokens -= item.token_count
            
            # Remove from groups
            for group in self.context_groups.values():
                group.items = [i for i in group.items if i.id != item_id]
                
            del self.context_items[item_id]
            return True
        return False

    def _check_token_limit(self, new_tokens: int) -> bool:
        """Check if new tokens would exceed limit"""
        return self.current_tokens + new_tokens <= self.max_tokens

    def _trim_context(self, needed_tokens: int) -> None:
        """Trim context to make room for new tokens"""
        # Sort items by priority and age
        items = sorted(
            self.context_items.values(),
            key=lambda x: (x.priority, -x.created_at.timestamp())
        )
        
        # Remove items until we have enough space
        freed_tokens = 0
        items_to_remove = []
        
        for item in items:
            if self.current_tokens - freed_tokens + needed_tokens <= self.max_tokens:
                break
            freed_tokens += item.token_count
            items_to_remove.append(item.id)
            
        # Remove identified items
        for item_id in items_to_remove:
            self.remove_context(item_id)

    def _estimate_tokens(self, content: Any) -> int:
        """Estimate token count for content"""
        if isinstance(content, str):
            # Rough estimation: ~4 characters per token
            return len(content) // 4
        elif isinstance(content, dict):
            return self._estimate_tokens(json.dumps(content))
        elif isinstance(content, list):
            return sum(self._estimate_tokens(item) for item in content)
        return 1

```

---

# ..\..\cmate\core\event_bus.py
## File: ..\..\cmate\core\event_bus.py

```py
# ..\..\cmate\core\event_bus.py
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

```

---

# ..\..\cmate\core\memory_manager.py
## File: ..\..\cmate\core\memory_manager.py

```py
# ..\..\cmate\core\memory_manager.py
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


```

---

# ..\..\cmate\core\prompt_manager.py
## File: ..\..\cmate\core\prompt_manager.py

```py
# ..\..\cmate\core\prompt_manager.py
"""
prompt_manager.py

Hanterar systemets promptmallar. Laddar promptar från konfigurationsfiler
(i YAML-format) och möjliggör att lägga till, uppdatera och hämta formaterade promptar.
För att undvika förvirring hos agenten innehåller varje prompt utförlig vägledning.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import os

# För att ladda YAML-filer
try:
    import yaml
except ImportError:
    yaml = None
    print("Varning: PyYAML saknas. Installera med 'pip install pyyaml' för att ladda YAML-promptar.")

@dataclass
class PromptTemplate:
    name: str
    content: str
    variables: List[str]
    description: str
    category: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_used: Optional[datetime] = None
    usage_count: int = 0

class PromptManager:
    def __init__(self, prompt_dir: Optional[str] = None):
        self.prompt_dir = Path(prompt_dir) if prompt_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        # Ladda från filer och eventuella default promptar
        self._load_prompts()
        self._load_default_prompts()

    def _load_prompts(self) -> None:
        """Ladda promptar från YAML-filer i prompt_dir."""
        if self.prompt_dir.exists():
            for prompt_file in self.prompt_dir.glob("*.yaml"):
                try:
                    with open(prompt_file, 'r', encoding='utf-8') as f:
                        if yaml:
                            data = yaml.safe_load(f)
                        else:
                            data = {}  # Om yaml saknas, hoppa över
                        for name, template_data in data.items():
                            self.templates[name] = PromptTemplate(
                                name=name,
                                content=template_data["content"],
                                variables=template_data.get("variables", []),
                                description=template_data.get("description", ""),
                                category=template_data.get("category", "general"),
                                metadata=template_data.get("metadata", {})
                            )
                except Exception as e:
                    print(f"Error loading prompt file {prompt_file}: {str(e)}")

    def _load_default_prompts(self) -> None:
        """
        Om inga promptar laddats in, eller för att komplettera,
        lägg in några standardpromptar med utförlig vägledning.
        """
        defaults = {
            "system_prompt": PromptTemplate(
                name="system_prompt",
                content=(
                    "Du är en semi-autonom agent specialiserad på att analysera, modifiera och testa kod. "
                    "Arbeta systematiskt: analysera läget, planera noggrant, implementera med hänsyn till kodstil, "
                    "och testa utförligt. Använd endast filer i ./Workspace. Var noggrann med dokumentation och "
                    "felsökning vid behov."
                ),
                variables=[],
                description="Basprompt för agentinitialisering med tydlig vägledning",
                category="system"
            ),
            "analysis_prompt": PromptTemplate(
                name="analysis_prompt",
                content=(
                    "Analysera följande filer och ge en översikt av strukturen, identifiera nyckelkomponenter, "
                    "potentiella problem och beroenden. Förbered en lista med rekommenderade åtgärder.\nFiler: {files}"
                ),
                variables=["files"],
                description="Detaljerad prompt för filanalys med stegvis vägledning",
                category="analysis"
            ),
            "implementation_prompt": PromptTemplate(
                name="implementation_prompt",
                content=(
                    "Implementera de begärda ändringarna enligt följande riktlinjer:\n"
                    "1. Följ den befintliga kodstilen noggrant.\n"
                    "2. Lägg till lämplig dokumentation i koden.\n"
                    "3. Skriv enhetstester för att validera ändringarna.\n"
                    "4. Inför robust felhantering.\n\n"
                    "Ändringar: {changes}\nPåverkade filer: {files}"
                ),
                variables=["changes", "files"],
                description="Prompt för implementeringssteg med tydliga anvisningar",
                category="implementation"
            ),
            "test_prompt": PromptTemplate(
                name="test_prompt",
                content=(
                    "Skapa tester för de följande ändringarna:\n"
                    "1. Enhetstester för ny funktionalitet.\n"
                    "2. Integrationstester där det är nödvändigt.\n"
                    "3. Täckning av kantfall och felhantering.\n\n"
                    "Implementering: {implementation}\nFiler att testa: {files}"
                ),
                variables=["implementation", "files"],
                description="Prompt för teststeg med detaljerade krav",
                category="testing"
            )
        }
        # Lägg in defaults om de inte redan finns
        for key, prompt in defaults.items():
            if key not in self.templates:
                self.templates[key] = prompt

    def get_prompt(self, name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        if name not in self.templates:
            raise KeyError(f"Prompt template '{name}' not found")
        template = self.templates[name]
        content = template.content
        if variables:
            try:
                content = content.format(**variables)
            except KeyError as e:
                raise ValueError(f"Missing required variable {str(e)}")
        template.last_used = datetime.now()
        template.usage_count += 1
        return content

    def add_template(self, 
                     name: str,
                     content: str,
                     variables: List[str],
                     description: str = "",
                     category: str = "custom",
                     metadata: Optional[Dict[str, Any]] = None) -> None:
        if name in self.templates:
            raise ValueError(f"Template '{name}' already exists")
        self.templates[name] = PromptTemplate(
            name=name,
            content=content,
            variables=variables,
            description=description,
            category=category,
            metadata=metadata or {}
        )

    def update_template(self,
                        name: str,
                        content: Optional[str] = None,
                        variables: Optional[List[str]] = None,
                        metadata: Optional[Dict[str, Any]] = None) -> None:
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found")
        template = self.templates[name]
        if content is not None:
            template.content = content
        if variables is not None:
            template.variables = variables
        if metadata is not None:
            template.metadata.update(metadata)

    def get_templates_by_category(self, category: str) -> List[PromptTemplate]:
        return [t for t in self.templates.values() if t.category == category]

    def get_template_variables(self, name: str) -> List[str]:
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found")
        return self.templates[name].variables.copy()

```

---

# ..\..\cmate\core\state_manager.py
## File: ..\..\cmate\core\state_manager.py

```py
# ..\..\cmate\core\state_manager.py
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

```

---

# ..\..\cmate\core\workflow_manager.py
## File: ..\..\cmate\core\workflow_manager.py

```py
# ..\..\cmate\core\workflow_manager.py
"""
workflow_manager.py

Hanterar skapande, köning och stegbaserad exekvering av workflows.
Inkluderar stöd för asynkrona steg med tidsmätning och felhantering.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from pathlib import Path

# Fil för att spara workflows
WORKFLOWS_FILE = Path("temp/workflows.json")


class WorkflowStepType(Enum):
    FILE_ANALYSIS = "file_analysis"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    VALIDATION = "validation"
    USER_INTERACTION = "user_interaction"


@dataclass
class WorkflowStep:
    """Enstaka steg i en workflow."""
    id: UUID
    type: WorkflowStepType
    action: Callable[..., Any]
    description: str
    required: bool = True
    dependencies: List[UUID] = field(default_factory=list)
    completed: bool = False
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3
    execution_time: Optional[float] = None  # Nytt fält för att mäta tiden för steget


@dataclass
class Workflow:
    """Hela workflow-definitionen."""
    id: UUID
    name: str
    description: str
    steps: List[WorkflowStep]
    current_step: Optional[UUID] = None
    status: str = "pending"  # pending, in_progress, completed, error
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkflowManager:
    """
    Hanterar skapande, köning och exekvering av workflows.
    Använder en asynkron kö och stödjer felhantering samt tidsmätning per steg.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.workflows: Dict[UUID, Workflow] = {}
        self.active_workflow: Optional[UUID] = None
        self.workflow_queue: asyncio.Queue = asyncio.Queue()
        self._worker_task: Optional[asyncio.Task] = None
        self.step_handlers: Dict[WorkflowStepType, Callable[..., Any]] = {}
        self._initialize_handlers()
        self._load_workflows()

    def _initialize_handlers(self) -> None:
        """Initierar standardstegshanterare."""
        self.step_handlers.update({
            WorkflowStepType.FILE_ANALYSIS: self._handle_file_analysis,
            WorkflowStepType.PLANNING: self._handle_planning,
            WorkflowStepType.IMPLEMENTATION: self._handle_implementation,
            WorkflowStepType.TESTING: self._handle_testing,
            WorkflowStepType.VALIDATION: self._handle_validation,
            WorkflowStepType.USER_INTERACTION: self._handle_user_interaction
        })

    async def start_worker(self) -> None:
        """Starta workflow-arbetaren om den inte redan är igång."""
        if not self._worker_task:
            self._worker_task = asyncio.create_task(self._workflow_worker())
            self.logger.info("Workflow worker started.")

    async def shutdown(self) -> None:
        """Stäng ner workflow manager på ett graciöst sätt."""
        self.logger.info("Shutting down workflow manager...")
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                self.logger.info("Workflow worker cancelled.")
            self._worker_task = None
        self._persist_workflows()

    async def create_workflow(self, request: Dict[str, Any]) -> Workflow:
        """
        Skapa en ny workflow utifrån en request.
        Requesten bör innehålla t.ex. 'name', 'description' och flaggor (ex. 'analyze_files')
        för att bygga workflow-steget.
        """
        workflow_id = uuid4()
        steps = self._create_steps_from_request(request)
        workflow = Workflow(
            id=workflow_id,
            name=request.get("name", "Unnamed Workflow"),
            description=request.get("description", ""),
            steps=steps,
            metadata=request
        )
        self.workflows[workflow_id] = workflow
        await self.workflow_queue.put(workflow)
        self.logger.info(f"Workflow {workflow_id} created and queued.")
        self._persist_workflows()
        await self.start_worker()
        return workflow

    async def execute_workflow(self, workflow_id: UUID) -> Dict[str, Any]:
        """
        Exekvera workflow med givet ID.
        Väntar tills workflow-processen (av arbetaren) är klar.
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")

        while self.workflows[workflow_id].status in ["pending", "in_progress"]:
            await asyncio.sleep(0.5)
        return {"workflow_id": workflow_id, "status": self.workflows[workflow_id].status}

    async def _workflow_worker(self) -> None:
        """Arbetsloop som hanterar workflows från kön."""
        while True:
            try:
                workflow: Workflow = await self.workflow_queue.get()
                self.active_workflow = workflow.id
                workflow.status = "in_progress"
                self.logger.info(f"Executing workflow {workflow.id}: {workflow.name}")
                await self._execute_workflow(workflow)
                self.active_workflow = None
                self.workflow_queue.task_done()
                self._persist_workflows()
            except asyncio.CancelledError:
                self.logger.info("Workflow worker received cancellation.")
                break
            except Exception as e:
                self.logger.error(f"Error in workflow worker: {str(e)}")
                await asyncio.sleep(1)

    async def _execute_workflow(self, workflow: Workflow) -> None:
        """Exekvera varje steg i workflow med beroendehantering och tidsmätning."""
        try:
            for step in workflow.steps:
                if step.dependencies:
                    await self._check_dependencies(step, workflow)
                workflow.current_step = step.id
                step_start = datetime.now()
                handler = self.step_handlers.get(step.type)
                if handler:
                    step.result = await handler(step, workflow)
                else:
                    step.result = await step.action()
                step.completed = True
                step.execution_time = (datetime.now() - step_start).total_seconds()
                self.logger.info(f"Step {step.id} ({step.type.value}) completed in {step.execution_time:.2f} seconds.")
            workflow.status = "completed"
            workflow.completed_at = datetime.now()
            self.logger.info(f"Workflow {workflow.id} completed.")
        except Exception as e:
            workflow.status = "error"
            self.logger.error(f"Workflow {workflow.id} failed: {str(e)}")
            raise

    async def _check_dependencies(self, step: WorkflowStep, workflow: Workflow) -> None:
        """Säkerställ att alla beroenden för ett steg är uppfyllda innan exekvering."""
        for dep_id in step.dependencies:
            dep_step = next((s for s in workflow.steps if s.id == dep_id), None)
            if not dep_step or not dep_step.completed:
                raise Exception(f"Dependency {dep_id} not met for step {step.id}")

    def _create_steps_from_request(self, request: Dict[str, Any]) -> List[WorkflowStep]:
        """
        Skapa workflow-steg baserat på request.
        Exempel: om request innehåller "analyze_files" läggs ett FILE_ANALYSIS-steg till.
        Du kan utöka denna logik med fler flaggor (t.ex. plan, implement, test).
        """
        steps = []
        if request.get("analyze_files"):
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.FILE_ANALYSIS,
                action=self._handle_file_analysis,
                description="Analyze workspace files"
            ))
        if request.get("plan_workflow"):
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.PLANNING,
                action=self._handle_planning,
                description="Plan the workflow tasks"
            ))
        if request.get("implement_changes"):
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.IMPLEMENTATION,
                action=self._handle_implementation,
                description="Implement requested changes"
            ))
        if request.get("run_tests"):
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.TESTING,
                action=self._handle_testing,
                description="Execute tests"
            ))
        # Ytterligare steg kan läggas till här…
        return steps

    # Standard stegshanterare (simulerar arbete med asyncio.sleep)
    async def _handle_file_analysis(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling file analysis for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "File analysis completed", "details": workflow.metadata}

    async def _handle_planning(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling planning for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "Planning completed"}

    async def _handle_implementation(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling implementation for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "Implementation completed"}

    async def _handle_testing(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling testing for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "Testing completed"}

    async def _handle_validation(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling validation for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "Validation completed"}

    async def _handle_user_interaction(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        self.logger.info(f"Handling user interaction for step {step.id}")
        await asyncio.sleep(1)
        return {"message": "User interaction completed"}

    def _persist_workflows(self) -> None:
        """Spara alla workflows i en JSON-fil."""
        try:
            if not WORKFLOWS_FILE.parent.exists():
                WORKFLOWS_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {}
            for wf_id, wf in self.workflows.items():
                data[str(wf_id)] = {
                    "id": str(wf.id),
                    "name": wf.name,
                    "description": wf.description,
                    "steps": [
                        {
                            "id": str(step.id),
                            "type": step.type.value,
                            "description": step.description,
                            "completed": step.completed,
                            "result": step.result,
                            "error": step.error,
                            "retries": step.retries,
                            "max_retries": step.max_retries,
                            "dependencies": [str(dep) for dep in step.dependencies],
                            "execution_time": step.execution_time
                        } for step in wf.steps
                    ],
                    "current_step": str(wf.current_step) if wf.current_step else None,
                    "status": wf.status,
                    "created_at": wf.created_at.isoformat(),
                    "completed_at": wf.completed_at.isoformat() if wf.completed_at else None,
                    "metadata": wf.metadata
                }
            with open(WORKFLOWS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error persisting workflows: {str(e)}")

    def _load_workflows(self) -> None:
        """Ladda sparade workflows från JSON-fil om den finns."""
        if WORKFLOWS_FILE.exists():
            try:
                with open(WORKFLOWS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for wf_id_str, wf_data in data.items():
                    wf_id = UUID(wf_data["id"])
                    steps = []
                    for step_data in wf_data["steps"]:
                        steps.append(WorkflowStep(
                            id=UUID(step_data["id"]),
                            type=WorkflowStepType(step_data["type"]),
                            action=self.step_handlers.get(WorkflowStepType(step_data["type"]), lambda: None),
                            description=step_data["description"],
                            required=True,
                            dependencies=[UUID(dep) for dep in step_data["dependencies"]],
                            completed=step_data["completed"],
                            result=step_data["result"],
                            error=step_data["error"],
                            retries=step_data["retries"],
                            max_retries=step_data["max_retries"],
                            execution_time=step_data.get("execution_time")
                        ))
                    workflow = Workflow(
                        id=wf_id,
                        name=wf_data["name"],
                        description=wf_data["description"],
                        steps=steps,
                        current_step=UUID(wf_data["current_step"]) if wf_data["current_step"] else None,
                        status=wf_data["status"],
                        created_at=datetime.fromisoformat(wf_data["created_at"]),
                        completed_at=datetime.fromisoformat(wf_data["completed_at"]) if wf_data["completed_at"] else None,
                        metadata=wf_data["metadata"]
                    )
                    self.workflows[wf_id] = workflow
                self.logger.info("Workflows loaded successfully.")
            except Exception as e:
                self.logger.error(f"Error loading workflows: {str(e)}")

```

---

# ..\..\cmate\core\__init__.py
## File: ..\..\cmate\core\__init__.py

```py
# ..\..\cmate\core\__init__.py
# Auto-generated __init__.py file

```

---

