# Project Details

# Table of Contents
- [..\CodeMate\cmate\core\__init__.py](#-CodeMate-cmate-core-__init__py)
- [..\CodeMate\cmate\core\agent_coordinator.py](#-CodeMate-cmate-core-agent_coordinatorpy)
- [..\CodeMate\cmate\core\context_manager.py](#-CodeMate-cmate-core-context_managerpy)
- [..\CodeMate\cmate\core\dependency_analyzer.py](#-CodeMate-cmate-core-dependency_analyzerpy)
- [..\CodeMate\cmate\core\event_bus.py](#-CodeMate-cmate-core-event_buspy)
- [..\CodeMate\cmate\core\memory_manager.py](#-CodeMate-cmate-core-memory_managerpy)
- [..\CodeMate\cmate\core\navigation_executor.py](#-CodeMate-cmate-core-navigation_executorpy)
- [..\CodeMate\cmate\core\navigation_system.py](#-CodeMate-cmate-core-navigation_systempy)
- [..\CodeMate\cmate\core\prompt_manager.py](#-CodeMate-cmate-core-prompt_managerpy)
- [..\CodeMate\cmate\core\state_manager.py](#-CodeMate-cmate-core-state_managerpy)
- [..\CodeMate\cmate\core\workflow_manager.py](#-CodeMate-cmate-core-workflow_managerpy)


# ..\..\CodeMate\cmate\core\__init__.py
## File: ..\..\CodeMate\cmate\core\__init__.py

```py
# ..\..\CodeMate\cmate\core\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\cmate\core\agent_coordinator.py
## File: ..\..\CodeMate\cmate\core\agent_coordinator.py

```py
# ..\..\CodeMate\cmate\core\agent_coordinator.py
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
# NEW MODULE INTEGRATION:
# --------------------------------------------------
# Navigation & Analysis modules
from ..core.navigation_system import NavigationDecisionSystem
from ..core.navigation_executor import NavigationActionExecutor
# Assumed WorkspaceAnalyzer (for analyzing workspace based on user's request)
from ..file_services.workspace_analyzer import WorkspaceAnalyzer

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
    def __init__(self, config: AgentConfig, state_manager: StateManager, workflow_manager: WorkflowManager):
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

        self.logger.info("Initializing AgentCoordinator with workspace: %s", self.config.workspace_path)

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

        # NEW: Instantiate WorkspaceAnalyzer for analyzing workspace based on user's request.
        self.workspace_analyzer = WorkspaceAnalyzer(self.config.workspace_path)

        # NEW: Instantiate NavigationDecisionSystem for handling navigation & analysis flow.
        self.navigation_system = NavigationDecisionSystem(self.config.workspace_path)
        
        # NEW: Instantiate NavigationActionExecutor for executing navigation actions.
        self.navigation_executor = NavigationActionExecutor(self.config.workspace_path)

        # Subscribe to state change events via the event bus.
        self.event_bus.subscribe("state_changed", self._handle_state_change)

        self.logger.info("AgentCoordinator initialized with all subsystems integrated.")
        self.logger.success("AgentCoordinator fully initialized with all subsystems integrated.")

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
        self.logger.debug("Publishing event: %s", event)
        for callback in self.event_subscribers:
            try:
                callback(event)
            except Exception as e:
                self.logger.error("Error in event subscriber callback: %s", str(e))
        asyncio.create_task(self.event_bus.publish(event.get("event", "unknown"), event))
        self.logger.debug("Event published: %s", event.get("event", "unknown"))

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
        self.logger.info("Processing request %s: %s", request_id, request)

        try:
            request_type = request.get("type")
            data = request.get("data", {})

            if not request_type:
                raise ValueError("Request must contain a 'type' field.")

            # Update state to processing.
            self.state_manager.update_state(AgentState.ANALYZING, {"request_id": request_id, "request_type": request_type})
            self.logger.debug("State updated to ANALYZING for request %s", request_id)

            self._publish_event({
                "event": "request_started",
                "request_id": request_id,
                "request_type": request_type,
                "timestamp": datetime.now().isoformat()
            })

            # Delegate to RequestHandler.
            self.logger.debug("Delegating request %s to RequestHandler.", request_id)
            result = await self.request_handler.handle_request(request)

            # Update state to idle.
            self.state_manager.update_state(AgentState.IDLE, {"last_request": request_type})
            self.logger.debug("State updated to IDLE after processing request %s", request_id)
            self._publish_event({
                "event": "request_completed",
                "request_id": request_id,
                "request_type": request_type,
                "timestamp": datetime.now().isoformat(),
                "result": result.data
            })

            self.logger.info("Request %s processed successfully.", request_id)
            self.logger.success("Request %s processed successfully.", request_id)
            return {"success": True, "result": result.data, "request_id": request_id}

        except Exception as e:
            self.logger.error("Error processing request %s: %s", request_id, str(e))
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
    # NEW: Navigation handling
    # --------------------------------------------------
    async def handle_navigation(self, request: Dict[str, Any]) -> Any:
        """
        Handle a navigation request.
        
        This method integrates the NavigationDecisionSystem and WorkspaceAnalyzer:
          1. Analyze the workspace based on the user's request.
          2. Prepare the navigation context.
          3. Obtain a navigation decision from the LLM.
          4. Execute the navigation action.
        
        Returns:
            NavigationResult: The result of the navigation action.
        """
        self.logger.info("Handling navigation request with content: %s", request.get("content"))
        # 1. Use the navigation system.
        nav_system = self.navigation_system

        # 2. Analyze workspace for the request.
        workspace_data = await self.workspace_analyzer.analyze_for_request(
            request["content"],
            self.config.workspace_path
        )
        self.logger.debug("Workspace analysis complete for navigation request.")

        # 3. Prepare navigation context.
        nav_context = await nav_system.prepare_decision_context(
            request["content"],
            workspace_data,
            self.state_manager.current_state
        )
        self.logger.debug("Navigation context prepared: %s", nav_context)

        # 4. Get available navigation actions.
        available_actions = nav_system.get_available_actions(nav_context)
        self.logger.debug("Available navigation actions: %s", available_actions)

        # 5. Request a navigation decision from the LLM.
        navigation_decision = await self.llm_manager.get_navigation_decision(
            nav_context,
            available_actions=available_actions
        )
        self.logger.info("Navigation decision received: %s", navigation_decision.action)

        # 6. Execute navigation.
        result = await nav_system.execute_navigation(navigation_decision.action, nav_context)
        self.logger.info("Navigation executed with result: %s", result)
        self.logger.success("Navigation executed successfully with result: %s", result)
        return result

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
        self.logger.info("Attempting recovery for error: %s", str(error))
        try:
            recovery_report = self.error_handler.handle_error(error, severity=ErrorSeverity.ERROR, metadata=context)
            if recovery_report and recovery_report.recovery_steps:
                self.logger.info("Recovery attempted with steps: %s", ", ".join(recovery_report.recovery_steps))
                self.state_manager.update_state(AgentState.IDLE, {"recovered": True})
                return True
        except Exception as recovery_error:
            self.logger.error("Recovery attempt failed: %s", str(recovery_error))
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
        status_report = {
            "state": state,
            "active_workflow": active_workflow,
            "uptime": uptime,
            "audit_log": self.audit_log[-10:],  # Last 10 entries.
            "metrics": metrics
        }
        self.logger.info("Status check: %s", status_report)
        return status_report

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
        self.logger.success("Agent shutdown completed successfully.")

    # --------------------------------------------------
    # Event callback handlers
    # --------------------------------------------------
    def _handle_state_change(self, event: Dict[str, Any]) -> None:
        """
        Handle state change events received via the EventBus.
        
        Args:
            event (Dict[str, Any]): The state change event.
        """
        self.logger.debug("Received state change event: %s", event)

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
        recent_context = self.context_manager.get_context()
        for item in recent_context:
            self.conversation.add_message("system", str(item))
        self.logger.info("LLM context refreshed.")
        self.logger.success("LLM context refreshed successfully.")

    async def generate_code(self, prompt: str) -> str:
        """
        Generate code based on a given prompt using the LLM agent.
        
        This method calls the LLM agent's ask() method and returns the generated code.
        
        Args:
            prompt (str): A description or prompt for the desired code.
            
        Returns:
            str: The generated code (as a string).
        """
        self.logger.info("Generating code for prompt: %s", prompt)
        response = await self.llm_agent.ask(prompt)
        generated_code = response.get("parsed_content") or response.get("content", "")
        self.logger.info("Code generation complete.")
        self.logger.success("Code generated successfully.")
        return generated_code

    def visualize_workflow(self) -> str:
        """
        Generate a textual visualization of the current active workflow.
        
        Returns a string summary (or ASCII diagram) of the workflow steps,
        their status, and any dependencies.
        
        Returns:
            str: A textual representation of the active workflow.
        """
        workflow = self.workflow_manager.get_active_workflow()
        if not workflow:
            self.logger.debug("No active workflow to visualize.")
            return "No active workflow."
        lines = ["Current Active Workflow:"]
        for step in self.workflow_manager.workflows.get(workflow, {}).get("steps", []):
            line = f"Step {step.get('id')}: {step.get('type')} - Status: {step.get('completed')}"
            lines.append(line)
        visualization = "\n".join(lines)
        self.logger.debug("Workflow visualization generated.")
        self.logger.success("Workflow visualization generated successfully.")
        return visualization

    async def integrate_with_git(self) -> Dict[str, Any]:
        """
        Simulate integration with a version control system (e.g., Git).
        
        Checks for changes in the workspace and, if found, commits the changes with a generated commit message.
        
        Returns:
            Dict[str, Any]: Details of the git integration.
        """
        self.logger.info("Integrating with Git (simulation)...")
        commit_message = "Auto-generated commit by CodeMate at " + datetime.now().isoformat()
        result = {
            "changes_detected": True,
            "commit_message": commit_message,
            "commit_id": str(uuid.uuid4())
        }
        self.logger.info("Git integration simulated with commit ID %s", result["commit_id"])
        self.logger.success("Git integration simulated successfully with commit ID %s", result["commit_id"])
        return result

    async def run_diagnostics(self) -> Dict[str, Any]:
        """
        Run system diagnostics including resource usage, process metrics, and log analysis.
        
        Returns:
            Dict[str, Any]: Diagnostic information.
        """
        self.logger.info("Running system diagnostics...")
        diagnostics = {}
        diagnostics["system_metrics"] = self.metrics_collector.collect_metrics().__dict__
        diagnostics["process_info"] = self.process_manager.get_active_processes()
        diagnostics["log_analysis"] = self.log_analyzer.find_error_patterns()
        self.logger.info("Diagnostics complete.")
        self.logger.success("Diagnostics completed successfully.")
        return diagnostics

    def update_configuration(self, new_config: Dict[str, Any]) -> None:
        """
        Dynamically update the agent's configuration.
        
        Args:
            new_config (Dict[str, Any]): A dictionary with configuration keys and new values.
        """
        self.logger.info("Updating configuration with: %s", new_config)
        for key, value in new_config.items():
            setattr(self.config, key, value)
        self.context_manager.max_tokens = self.config.context_window_size
        self.logger.info("Configuration updated successfully.")
        self.logger.success("Configuration updated successfully.")

    def persist_audit_log(self) -> None:
        """
        Persist the audit log to persistent storage.
        
        Writes the audit log to a file using the PersistenceManager.
        """
        self.logger.info("Persisting audit log...")
        try:
            self.persistence_manager.store("audit_log", self.audit_log)
            self.logger.info("Audit log persisted successfully.")
            self.logger.success("Audit log persisted successfully.")
        except Exception as e:
            self.logger.error("Error persisting audit log: %s", str(e))

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
            Dict[str, Any]: The result of the modification process.
        """
        self.logger.info("Starting code modification process with prompt: %s", prompt)
        generated_code = await self.generate_code(prompt)
        validation_result = self.implementation_validator.validate_implementation(generated_code, "python")
        if not validation_result.valid:
            self.logger.error("Generated code validation failed with errors: %s", ", ".join(validation_result.errors))
            return {"success": False, "error": "Validation failed", "details": validation_result.errors}
        test_result = await self.test_manager.run_all_tests()
        diagnostics = await self.test_manager.analyze_results(test_result)
        if diagnostics.get("failed_tests", 0) > 0:
            self.logger.error("Some tests failed during code modification. Initiating recovery.")
            await self._attempt_recovery(Exception("Test failures during code modification"), {"prompt": prompt})
            return {"success": False, "error": "Tests failed", "details": diagnostics}
        self.logger.info("Code modification executed successfully.")
        self.logger.success("Code modification executed successfully.")
        return {"success": True, "generated_code": generated_code, "validation": validation_result, "tests": diagnostics}

```

---

# ..\..\CodeMate\cmate\core\context_manager.py
## File: ..\..\CodeMate\cmate\core\context_manager.py

```py
# ..\..\CodeMate\cmate\core\context_manager.py
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

```

---

# ..\..\CodeMate\cmate\core\dependency_analyzer.py
## File: ..\..\CodeMate\cmate\core\dependency_analyzer.py

```py
# ..\..\CodeMate\cmate\core\dependency_analyzer.py
# ..\..\cmate\core\dependency_analyzer.py
# cmate/core/dependency_analyzer.py
"""
cmate/core/dependency_analyzer.py

Implements advanced dependency analysis for different component types,
handling both direct and indirect dependencies with support for:
- Python imports and module dependencies
- Frontend dependencies (CSS, JS, templates)
- Configuration file relationships
- Circular dependency detection
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
from datetime import datetime
import ast
import re
import logging

from ..file_services.file_analyzer import FileAnalyzer, CodeAnalysis
from ..utils.error_handler import ErrorHandler

logger = logging.getLogger(__name__)
logger.info("Initializing ComponentDependencyAnalyzer.")

@dataclass
class DependencyInfo:
    """Information about a component's dependencies"""
    direct_deps: List[Path]
    indirect_deps: List[Path]
    reverse_deps: List[Path]  # Components that depend on this one
    circular_deps: List[List[Path]]  # Lists of circular dependency chains
    weight: int  # Dependency complexity weight
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class DependencyGraph:
    """Represents the project's dependency structure"""
    nodes: Dict[Path, Set[Path]]  # Direct dependencies
    reverse_nodes: Dict[Path, Set[Path]]  # Reverse dependencies
    weights: Dict[Path, int]  # Node weights
    metadata: Dict[str, Any] = field(default_factory=dict)

class ComponentDependencyAnalyzer:
    """Analyzes component dependencies across the project"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.file_analyzer = FileAnalyzer()
        self.error_handler = ErrorHandler()
        self.dependency_cache: Dict[Path, DependencyInfo] = {}
        self.graph = DependencyGraph(
            nodes={},
            reverse_nodes={},
            weights={},
            metadata={"last_update": datetime.now()}
        )
        logger.info("ComponentDependencyAnalyzer initialized with workspace: %s", self.workspace)
        logger.success("ComponentDependencyAnalyzer initialized successfully with workspace: %s", self.workspace)

    async def analyze_dependencies(self, component_path: Path) -> DependencyInfo:
        """Analyze all dependencies for a component"""
        logger.info("Starting dependency analysis for component: %s", component_path)
        try:
            # Check cache first
            if component_path in self.dependency_cache:
                if self._is_cache_valid(component_path):
                    logger.debug("Cache hit for component: %s", component_path)
                    logger.success("Using cached dependency analysis for %s", component_path)
                    return self.dependency_cache[component_path]

            # Get file analysis
            analysis = await self.file_analyzer.analyze_file(component_path)
            logger.debug("File analysis completed for component: %s, file type: %s", component_path, analysis.file_type)
            
            # Extract direct dependencies
            direct_deps = await self._get_direct_dependencies(component_path, analysis)
            logger.debug("Direct dependencies for %s: %s", component_path, direct_deps)
            
            # Build dependency graph for this component
            self._update_graph(component_path, direct_deps)
            logger.debug("Dependency graph updated for component: %s", component_path)
            
            # Get indirect dependencies
            indirect_deps = self._get_indirect_dependencies(component_path)
            # Find reverse dependencies
            reverse_deps = list(self.graph.reverse_nodes.get(component_path, set()))
            # Detect circular dependencies
            circular_deps = self._detect_circular_dependencies(component_path)
            # Calculate dependency weight
            weight = self._calculate_dependency_weight(component_path, direct_deps, indirect_deps, circular_deps)
            logger.info("Dependency analysis complete for %s; weight: %d", component_path, weight)
            
            dep_info = DependencyInfo(
                direct_deps=direct_deps,
                indirect_deps=indirect_deps,
                reverse_deps=reverse_deps,
                circular_deps=circular_deps,
                weight=weight,
                metadata={
                    "file_type": analysis.file_type,
                    "complexity": analysis.code_analysis.complexity if analysis.code_analysis else 0
                }
            )
            self.dependency_cache[component_path] = dep_info
            logger.success("Dependency analysis stored successfully for %s", component_path)
            return dep_info
        except Exception as e:
            self.error_handler.handle_error(e, severity=self.error_handler.logger.level, metadata={"component": str(component_path)})
            raise

    async def _get_direct_dependencies(self, component_path: Path, analysis: CodeAnalysis) -> List[Path]:
        """Get direct dependencies based on file type"""
        deps = set()
        if component_path.suffix == '.py':
            deps.update(await self._analyze_python_deps(component_path, analysis))
        elif component_path.suffix in {'.html', '.js'}:
            deps.update(await self._analyze_frontend_deps(component_path, analysis))
        elif component_path.suffix in {'.yaml', '.yml', '.json'}:
            deps.update(await self._analyze_config_deps(component_path, analysis))
        return list(deps)

    async def _analyze_python_deps(self, file_path: Path, analysis: CodeAnalysis) -> Set[Path]:
        """Analyze Python file dependencies"""
        deps = set()
        logger.debug("Analyzing Python dependencies for file: %s", file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        dep_path = self._resolve_import(name.name)
                        if dep_path:
                            deps.add(dep_path)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dep_path = self._resolve_import(node.module)
                        if dep_path:
                            deps.add(dep_path)
        except Exception as e:
            self.error_handler.handle_error(e, metadata={"file": str(file_path)})
        return deps

    async def _analyze_frontend_deps(self, file_path: Path, analysis: CodeAnalysis) -> Set[Path]:
        """Analyze frontend file dependencies"""
        deps = set()
        logger.debug("Analyzing frontend dependencies for file: %s", file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            css_deps = re.findall(r'href=[\'"]([^\'"]+\.css)[\'"]', content)
            deps.update(self._resolve_frontend_paths(file_path, css_deps))
            js_deps = re.findall(r'src=[\'"]([^\'"]+\.js)[\'"]', content)
            deps.update(self._resolve_frontend_paths(file_path, js_deps))
            template_deps = re.findall(r'{%\s*include\s+[\'"]([^\'"]+)[\'"]', content)
            deps.update(self._resolve_frontend_paths(file_path, template_deps))
        except Exception as e:
            self.error_handler.handle_error(e, metadata={"file": str(file_path)})
        return deps

    async def _analyze_config_deps(self, file_path: Path, analysis: CodeAnalysis) -> Set[Path]:
        """Analyze configuration file dependencies"""
        deps = set()
        logger.debug("Analyzing configuration dependencies for file: %s", file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            file_refs = re.findall(r'file:\s*[\'"]([^\'"]+)[\'"]', content)
            deps.update(self._resolve_config_paths(file_path, file_refs))
            path_refs = re.findall(r'path:\s*[\'"]([^\'"]+)[\'"]', content)
            deps.update(self._resolve_config_paths(file_path, path_refs))
        except Exception as e:
            self.error_handler.handle_error(e, metadata={"file": str(file_path)})
        return deps

    def _resolve_import(self, import_name: str) -> Optional[Path]:
        """Resolve Python import to actual file path"""
        parts = import_name.split('.')
        possible_paths = [
            self.workspace / '/'.join(parts) / '__init__.py',
            self.workspace / '/'.join(parts) + '.py'
        ]
        for path in possible_paths:
            if path.exists():
                logger.debug("Resolved import '%s' to path: %s", import_name, path)
                return path
        logger.debug("Could not resolve import: %s", import_name)
        return None

    def _resolve_frontend_paths(self, source_file: Path, references: List[str]) -> Set[Path]:
        """Resolve frontend file references to actual paths"""
        resolved = set()
        source_dir = source_file.parent
        for ref in references:
            if ref.startswith('./') or ref.startswith('../'):
                path = (source_dir / ref).resolve()
            else:
                path = (self.workspace / ref.lstrip('/')).resolve()
            if path.exists():
                resolved.add(path)
        return resolved

    def _resolve_config_paths(self, config_file: Path, references: List[str]) -> Set[Path]:
        """Resolve config file references to actual paths"""
        resolved = set()
        config_dir = config_file.parent
        for ref in references:
            path = (config_dir / ref).resolve()
            if not path.exists():
                path = (self.workspace / ref).resolve()
            if path.exists():
                resolved.add(path)
        return resolved

    def _update_graph(self, source: Path, dependencies: List[Path]) -> None:
        """Update dependency graph with new information"""
        if source not in self.graph.nodes:
            self.graph.nodes[source] = set()
        self.graph.nodes[source].update(dependencies)
        for dep in dependencies:
            if dep not in self.graph.reverse_nodes:
                self.graph.reverse_nodes[dep] = set()
            self.graph.reverse_nodes[dep].add(source)
        logger.debug("Updated dependency graph for component: %s", source)

    def _get_indirect_dependencies(self, component_path: Path) -> List[Path]:
        """Get all indirect dependencies"""
        indirect = set()
        visited = {component_path}
        def visit(path: Path):
            for dep in self.graph.nodes.get(path, set()):
                if dep not in visited:
                    visited.add(dep)
                    indirect.add(dep)
                    visit(dep)
        visit(component_path)
        return list(indirect)

    def _detect_circular_dependencies(self, start_path: Path) -> List[List[Path]]:
        """Detect circular dependencies starting from a component"""
        circular_deps = []
        visited = set()
        path_stack = []
        def visit(current_path: Path):
            if current_path in path_stack:
                cycle_start = path_stack.index(current_path)
                circular_deps.append(path_stack[cycle_start:] + [current_path])
                return
            if current_path in visited:
                return
            visited.add(current_path)
            path_stack.append(current_path)
            for dep in self.graph.nodes.get(current_path, set()):
                visit(dep)
            path_stack.pop()
        visit(start_path)
        return circular_deps

    def _calculate_dependency_weight(self, component_path: Path, direct_deps: List[Path], indirect_deps: List[Path], circular_deps: List[List[Path]]) -> int:
        """Calculate dependency complexity weight"""
        weight = 0
        weight += len(direct_deps) * 2
        weight += len(indirect_deps)
        weight += len(circular_deps) * 5
        if component_path.suffix == '.py':
            weight += 2
        elif component_path.suffix in {'.html', '.js'}:
            weight += 1
        return weight

    def _is_cache_valid(self, component_path: Path) -> bool:
        """Check if cached dependency info is still valid"""
        if component_path not in self.dependency_cache:
            return False
        cache_entry = self.dependency_cache[component_path]
        file_mtime = datetime.fromtimestamp(component_path.stat().st_mtime)
        valid = (file_mtime < cache_entry.timestamp and (datetime.now() - cache_entry.timestamp).total_seconds() < 3600)
        logger.debug("Cache valid for %s: %s", component_path, valid)
        return valid

    def get_dependency_stats(self) -> Dict[str, Any]:
        """Get statistics about project dependencies"""
        stats = {
            "total_components": len(self.graph.nodes),
            "total_dependencies": sum(len(deps) for deps in self.graph.nodes.values()),
            "circular_dependencies": sum(1 for deps in self.graph.nodes.values() if any(node in deps for node in deps)),
            "max_weight": max(self.graph.weights.values()) if self.graph.weights else 0,
            "isolated_components": sum(1 for deps in self.graph.nodes.values() if not deps and not self.graph.reverse_nodes.get(deps)),
            "last_update": self.graph.metadata["last_update"].isoformat()
        }
        logger.info("Dependency stats: %s", stats)
        return stats

    def clear_cache(self) -> None:
        """Clear dependency cache"""
        self.dependency_cache.clear()
        self.graph.metadata["last_update"] = datetime.now()
        logger.info("Cleared dependency cache.")
        logger.success("Dependency cache cleared successfully.")

```

---

# ..\..\CodeMate\cmate\core\event_bus.py
## File: ..\..\CodeMate\cmate\core\event_bus.py

```py
# ..\..\CodeMate\cmate\core\event_bus.py
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

```

---

# ..\..\CodeMate\cmate\core\memory_manager.py
## File: ..\..\CodeMate\cmate\core\memory_manager.py

```py
# ..\..\CodeMate\cmate\core\memory_manager.py
# ..\..\cmate\core\memory_manager.py
# src/core/memory_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)

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
        logger.success("MemoryManager initialized successfully.")

    def store(self, 
              content: Any,
              memory_type: MemoryType,
              importance: int = 0,
              metadata: Optional[Dict[str, Any]] = None,
              ttl: Optional[int] = None) -> UUID:
        """Store new memory item.
        ttl: time-to-live in seconds."""
        expires_at = datetime.now() + timedelta(seconds=ttl) if ttl is not None else None
        # Create memory item
        item = MemoryItem(
            id=uuid4(),
            content=content,
            type=memory_type,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            importance=importance,
            metadata=metadata or {},
            expires_at=expires_at
        )
        
        # Check and maintain limits
        self._check_type_limit(memory_type)
        
        # Store item
        self.memories[item.id] = item
        logger.success("Stored memory item with id: %s", item.id)
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
            logger.success("Updated memory item with id: %s", memory_id)
            return True
        return False

    def forget(self, memory_id: UUID) -> bool:
        """Remove memory item"""
        removed = bool(self.memories.pop(memory_id, None))
        if removed:
            logger.success("Forgot memory item with id: %s", memory_id)
        return removed

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
            
        if removed_count:
            logger.success("Cleaned up %d memory items.", removed_count)
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
            while len(type_memories) >= limit and to_remove:
                item = to_remove.pop(0)
                self.forget(item.id)
                type_memories.remove(item)

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
        consolidated = 0
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
                consolidated += 1
        if consolidated:
            logger.success("Consolidated %d memory items from short-term memory.", consolidated)

```

---

# ..\..\CodeMate\cmate\core\navigation_executor.py
## File: ..\..\CodeMate\cmate\core\navigation_executor.py

```py
# ..\..\CodeMate\cmate\core\navigation_executor.py
# ..\..\cmate\core\navigation_executor.py
"""
cmate/core/navigation_executor.py

Handles execution of navigation actions including:
- File creation and modification
- Directory structure management
- Safe file operations with backup/rollback
- Multi-file operations
"""

import shutil
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from uuid import UUID, uuid4
import logging

from ..utils.error_handler import ErrorHandler
from ..core.dependency_analyzer import ComponentDependencyAnalyzer
from ..file_services.file_analyzer import FileAnalyzer

logger = logging.getLogger(__name__)
logger.success("NavigationActionExecutor module loaded successfully.")

class NavigationActionType(Enum):
    """Types of navigation actions"""
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
    MOVE = "move"
    BACKUP = "backup"
    RESTORE = "restore"

@dataclass
class NavigationAction:
    """Represents a navigation action to be executed"""
    id: UUID
    action_type: NavigationActionType
    source_path: Path
    target_path: Optional[Path] = None
    content: Optional[str] = None
    backup_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ActionResult:
    """Result of an executed navigation action"""
    action_id: UUID
    success: bool
    source_path: Path
    target_path: Optional[Path]
    backup_created: bool
    error: Optional[str] = None
    changes_made: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class NavigationActionExecutor:
    """Executes navigation actions with safety checks and rollback capability"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.backup_dir = self.workspace / ".backups"
        self.error_handler = ErrorHandler()
        self.dependency_analyzer = ComponentDependencyAnalyzer(str(self.workspace))
        self.file_analyzer = FileAnalyzer()
        
        # Initialize backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Track active operations
        self.active_operations: Dict[UUID, NavigationAction] = {}
        self.operation_results: Dict[UUID, ActionResult] = {}
        logger.success("NavigationActionExecutor initialized successfully.")

    async def execute_action(self, action: NavigationAction) -> ActionResult:
        """Execute a navigation action with safety checks"""
        try:
            # Register active operation
            self.active_operations[action.id] = action
            
            # Validate paths
            await self._validate_paths(action)
            
            # Create backup if needed
            if action.action_type in [NavigationActionType.MODIFY, NavigationActionType.DELETE]:
                action.backup_path = await self._create_backup(action.source_path)
            
            # Execute appropriate action
            if action.action_type == NavigationActionType.CREATE:
                result = await self._execute_create(action)
            elif action.action_type == NavigationActionType.MODIFY:
                result = await self._execute_modify(action)
            elif action.action_type == NavigationActionType.DELETE:
                result = await self._execute_delete(action)
            elif action.action_type == NavigationActionType.MOVE:
                result = await self._execute_move(action)
            else:
                raise ValueError(f"Unsupported action type: {action.action_type}")
            
            # Store and return result
            self.operation_results[action.id] = result
            logger.success("Navigation action %s executed successfully.", action.id)
            return result
            
        except Exception as e:
            error_msg = str(e)
            self.error_handler.handle_error(e, metadata={
                "action_id": str(action.id),
                "action_type": action.action_type.value
            })
            
            # Attempt recovery if backup exists
            if action.backup_path:
                await self._restore_backup(action)
                error_msg += " (Backup restored)"
            
            result = ActionResult(
                action_id=action.id,
                success=False,
                source_path=action.source_path,
                target_path=action.target_path,
                backup_created=bool(action.backup_path),
                error=error_msg,
                changes_made={}
            )
            
            self.operation_results[action.id] = result
            return result
            
        finally:
            # Cleanup active operation
            self.active_operations.pop(action.id, None)

    async def _validate_paths(self, action: NavigationAction) -> None:
        """Validate source and target paths"""
        # Check paths are within workspace
        if not str(action.source_path).startswith(str(self.workspace)):
            raise ValueError(f"Source path must be within workspace: {action.source_path}")
        
        if action.target_path and not str(action.target_path).startswith(str(self.workspace)):
            raise ValueError(f"Target path must be within workspace: {action.target_path}")
        
        # Check source exists for appropriate actions
        if action.action_type in [NavigationActionType.MODIFY, NavigationActionType.DELETE, NavigationActionType.MOVE]:
            if not action.source_path.exists():
                raise FileNotFoundError(f"Source path does not exist: {action.source_path}")
        
        # Check target doesn't exist for create/move
        if action.action_type in [NavigationActionType.CREATE, NavigationActionType.MOVE]:
            if action.target_path and action.target_path.exists():
                raise FileExistsError(f"Target path already exists: {action.target_path}")

    async def _create_backup(self, path: Path) -> Path:
        """Create backup of a file"""
        if not path.exists():
            return None
            
        # Create timestamp-based backup path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"{path.name}.{timestamp}.bak"
        
        # Copy file to backup
        shutil.copy2(path, backup_path)
        logger.success("Backup created for file %s at %s", path, backup_path)
        return backup_path

    async def _restore_backup(self, action: NavigationAction) -> None:
        """Restore from backup"""
        if not action.backup_path or not action.backup_path.exists():
            return
            
        # Restore original file
        shutil.copy2(action.backup_path, action.source_path)
        
        # Clean up backup
        action.backup_path.unlink()
        logger.success("Backup restored for action %s", action.id)

    async def _execute_create(self, action: NavigationAction) -> ActionResult:
        """Execute file creation"""
        target_path = action.target_path or action.source_path
        
        # Create parent directories if needed
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        if action.content:
            target_path.write_text(action.content)
        else:
            target_path.touch()
        
        logger.success("File created successfully at %s", target_path)
        return ActionResult(
            action_id=action.id,
            success=True,
            source_path=action.source_path,
            target_path=target_path,
            backup_created=False,
            changes_made={"operation": "create", "path": str(target_path)}
        )

    async def _execute_modify(self, action: NavigationAction) -> ActionResult:
        """Execute file modification"""
        if not action.content:
            raise ValueError("Content required for modify action")
        
        # Write new content
        action.source_path.write_text(action.content)
        
        # Analyze changes
        original_content = ""
        if action.backup_path:
            original_content = action.backup_path.read_text()
        
        changes = self._analyze_changes(original_content, action.content)
        logger.success("File modified successfully at %s", action.source_path)
        return ActionResult(
            action_id=action.id,
            success=True,
            source_path=action.source_path,
            target_path=None,
            backup_created=bool(action.backup_path),
            changes_made=changes
        )

    async def _execute_delete(self, action: NavigationAction) -> ActionResult:
        """Execute file deletion"""
        # Delete file
        action.source_path.unlink()
        logger.success("File deleted successfully: %s", action.source_path)
        return ActionResult(
            action_id=action.id,
            success=True,
            source_path=action.source_path,
            target_path=None,
            backup_created=bool(action.backup_path),
            changes_made={"operation": "delete", "path": str(action.source_path)}
        )

    async def _execute_move(self, action: NavigationAction) -> ActionResult:
        """Execute file move"""
        if not action.target_path:
            raise ValueError("Target path required for move action")
        
        # Create parent directories if needed
        action.target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.move(str(action.source_path), str(action.target_path))
        logger.success("File moved successfully from %s to %s", action.source_path, action.target_path)
        return ActionResult(
            action_id=action.id,
            success=True,
            source_path=action.source_path,
            target_path=action.target_path,
            backup_created=False,
            changes_made={
                "operation": "move",
                "source": str(action.source_path),
                "target": str(action.target_path)
            }
        )

    def _analyze_changes(self, original: str, modified: str) -> Dict[str, Any]:
        """Analyze changes between original and modified content"""
        changes = {
            "operation": "modify",
            "lines_changed": 0,
            "additions": 0,
            "deletions": 0
        }
        
        original_lines = original.splitlines()
        modified_lines = modified.splitlines()
        
        # Simple line-based diff
        changes["lines_changed"] = abs(len(modified_lines) - len(original_lines))
        changes["additions"] = sum(1 for line in modified_lines if line not in original_lines)
        changes["deletions"] = sum(1 for line in original_lines if line not in modified_lines)
        
        return changes

    async def cleanup_backups(self, max_age_hours: int = 24) -> int:
        """Clean up old backup files"""
        cleanup_count = 0
        current_time = datetime.now()
        
        for backup_file in self.backup_dir.glob("*.bak"):
            try:
                # Parse timestamp from filename
                timestamp_str = backup_file.stem.split(".")[-1]
                backup_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                # Check age
                age_hours = (current_time - backup_time).total_seconds() / 3600
                if age_hours > max_age_hours:
                    backup_file.unlink()
                    cleanup_count += 1
                    
            except Exception as e:
                self.error_handler.handle_error(e, metadata={
                    "backup_file": str(backup_file)
                })
                
        if cleanup_count:
            logger.success("Cleaned up %d backup files.", cleanup_count)
        return cleanup_count

    def get_operation_history(self, limit: Optional[int] = None) -> List[ActionResult]:
        """Get history of operations"""
        history = sorted(
            self.operation_results.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return history[:limit] if limit else history

    def get_active_operations(self) -> List[NavigationAction]:
        """Get list of currently active operations"""
        return list(self.active_operations.values())

```

---

# ..\..\CodeMate\cmate\core\navigation_system.py
## File: ..\..\CodeMate\cmate\core\navigation_system.py

```py
# ..\..\CodeMate\cmate\core\navigation_system.py
# ..\..\cmate\core\navigation_system.py
"""
cmate/core/navigation_system.py

Implements the NavigationDecisionSystem responsible for:
- Analyzing the workspace and files
- Classifying components
- Making navigation decisions
- Handling multi-component navigation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from uuid import UUID, uuid4
import logging

from ..core.state_manager import AgentState
from ..file_services.file_analyzer import FileAnalyzer
from ..file_services.workspace_scanner import WorkspaceScanner

logger = logging.getLogger(__name__)
logger.success("NavigationDecisionSystem module loaded successfully.")

@dataclass
class NavigationContext:
    """Context for navigation decisions"""
    request_id: UUID
    user_request: str
    current_path: Path
    target_components: List[Path]
    dependencies: Dict[Path, List[Path]]
    state_history: List[AgentState]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NavigationResult:
    """Result of a navigation decision"""
    success: bool
    chosen_path: Optional[Path]
    component_type: str
    dependencies: List[Path]
    action_taken: str
    navigation_history: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class ComponentClassifier:
    """Classifies components based on content and structure"""
    
    def __init__(self):
        self.file_analyzer = FileAnalyzer()
        logger.debug("ComponentClassifier initialized.")

    async def classify_component(self, file_path: Path) -> str:
        """Classify a component based on its content and file path"""
        logger.debug("Classifying component: %s", file_path)
        analysis = await self.file_analyzer.analyze_file(file_path)
        if "test" in file_path.stem.lower():
            logger.debug("Component classified as TEST based on filename.")
            return "TEST"
        elif analysis.file_type == ".py":
            if self._is_backend_code(analysis):
                logger.debug("Component classified as BACKEND.")
                return "BACKEND"
            elif self._is_frontend_code(analysis):
                logger.debug("Component classified as FRONTEND.")
                return "FRONTEND"
        elif analysis.file_type in [".html", ".css", ".js"]:
            logger.debug("Component classified as FRONTEND based on file type.")
            return "FRONTEND"
        elif analysis.file_type in [".json", ".yaml", ".yml"]:
            logger.debug("Component classified as CONFIG based on file type.")
            return "CONFIG"
        logger.debug("Component classified as UNKNOWN.")
        return "UNKNOWN"
        
    def _is_backend_code(self, analysis: Any) -> bool:
        """Check if the code is backend-related"""
        backend_indicators = [
            "django", "flask", "fastapi", "sqlalchemy",
            "database", "model", "schema", "api"
        ]
        return any(ind in str(analysis.imports).lower() for ind in backend_indicators)
        
    def _is_frontend_code(self, analysis: Any) -> bool:
        """Check if the code is frontend-related"""
        frontend_indicators = [
            "template", "html", "css", "javascript",
            "react", "vue", "angular", "dom"
        ]
        return any(ind in str(analysis.imports).lower() for ind in frontend_indicators)

class NavigationDecisionSystem:
    """Main system for making navigation decisions"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.scanner = WorkspaceScanner(str(self.workspace))
        self.classifier = ComponentClassifier()
        self.current_context: Optional[NavigationContext] = None
        logger.info("NavigationDecisionSystem initialized with workspace: %s", self.workspace)
        logger.success("NavigationDecisionSystem initialized successfully.")

    async def prepare_decision_context(
        self,
        request: str,
        workspace_data: dict,
        current_state: AgentState
    ) -> NavigationContext:
        """
        Prepare the navigation decision context based on:
          - The user's request
          - Workspace analysis
          - Current state
        """
        logger.info("Preparing navigation context for request: %s", request)
        context_id = uuid4()
        current_path = self.workspace
        
        # Scan the workspace
        scan_result = await self.scanner.scan_workspace()
        logger.debug("Workspace scan complete. Total files found: %d", len(scan_result.files))
        
        # Identify target components
        target_components = []
        for file_info in scan_result.files:
            if self._is_relevant_for_request(file_info, request):
                target_components.append(file_info.path)
        logger.debug("Target components identified: %s", target_components)
        
        # Analyze dependencies for each target component
        dependencies = {}
        for component in target_components:
            deps = await self._analyze_dependencies(component)
            dependencies[component] = deps
            logger.debug("Dependencies for %s: %s", component, deps)
            
        context = NavigationContext(
            request_id=context_id,
            user_request=request,
            current_path=current_path,
            target_components=target_components,
            dependencies=dependencies,
            state_history=[current_state],
            metadata=workspace_data
        )
        logger.info("Navigation context prepared with request_id: %s", context_id)
        logger.success("Navigation context prepared successfully with request_id: %s", context_id)
        return context
        
    def get_available_actions(self, context: NavigationContext) -> List[str]:
        """
        Return available navigation actions based on the context.
        For example: ['ANALYZE_FILE', 'CREATE_NEW', 'MODIFY_EXISTING']
        """
        actions = ["ANALYZE_FILE", "SCAN_DEPENDENCIES"]
        if context.target_components:
            actions.append("MODIFY_EXISTING")
        else:
            actions.append("CREATE_NEW")
        if len(context.target_components) > 1:
            actions.append("HANDLE_MULTIPLE")
        logger.debug("Available actions based on context: %s", actions)
        return actions
        
    async def execute_navigation(
        self,
        chosen_action: str,
        context: NavigationContext
    ) -> NavigationResult:
        """Execute the chosen navigation action"""
        logger.info("Executing navigation action: %s", chosen_action)
        try:
            if chosen_action == "ANALYZE_FILE":
                result = await self._execute_analysis(context)
            elif chosen_action == "CREATE_NEW":
                result = await self._execute_creation(context)
            elif chosen_action == "MODIFY_EXISTING":
                result = await self._execute_modification(context)
            elif chosen_action == "HANDLE_MULTIPLE":
                result = await self._execute_multi_handling(context)
            else:
                raise ValueError(f"Unknown action: {chosen_action}")
            logger.info("Navigation action '%s' executed successfully.", chosen_action)
            logger.success("Navigation action '%s' executed successfully.", chosen_action)
            return result
        except Exception as e:
            logger.error("Error executing navigation action '%s': %s", chosen_action, str(e))
            return NavigationResult(
                success=False,
                chosen_path=None,
                component_type="ERROR",
                dependencies=[],
                action_taken=chosen_action,
                navigation_history=[f"Error: {str(e)}"],
                metadata={"error": str(e)}
            )
            
    async def _execute_analysis(self, context: NavigationContext) -> NavigationResult:
        """Perform file analysis"""
        if not context.target_components:
            raise ValueError("No target components for analysis")
        target = context.target_components[0]
        component_type = await self.classifier.classify_component(target)
        logger.debug("Analysis executed on %s; classified as %s", target, component_type)
        logger.success("Analysis executed successfully on %s", target)
        return NavigationResult(
            success=True,
            chosen_path=target,
            component_type=component_type,
            dependencies=context.dependencies.get(target, []),
            action_taken="ANALYZE_FILE",
            navigation_history=[f"Analyzed {target}"],
            metadata={"analysis_type": component_type, "file_count": len(context.target_components)}
        )
        
    async def _execute_creation(self, context: NavigationContext) -> NavigationResult:
        """Prepare to create a new file"""
        target_path = self._determine_new_file_path(context.user_request)
        logger.debug("Determined new file path: %s", target_path)
        logger.success("Creation action prepared successfully with target path: %s", target_path)
        return NavigationResult(
            success=True,
            chosen_path=target_path,
            component_type="NEW",
            dependencies=[],
            action_taken="CREATE_NEW",
            navigation_history=[f"Preparing to create {target_path}"],
            metadata={"creation_type": self._determine_component_type(context.user_request)}
        )
        
    async def _execute_modification(self, context: NavigationContext) -> NavigationResult:
        """Prepare to modify an existing file"""
        target = context.target_components[0]
        component_type = await self.classifier.classify_component(target)
        logger.debug("Preparing to modify %s, classified as %s", target, component_type)
        logger.success("Modification action prepared successfully for %s", target)
        return NavigationResult(
            success=True,
            chosen_path=target,
            component_type=component_type,
            dependencies=context.dependencies.get(target, []),
            action_taken="MODIFY_EXISTING",
            navigation_history=[f"Preparing to modify {target}"],
            metadata={"modification_type": "UPDATE"}
        )
        
    async def _execute_multi_handling(self, context: NavigationContext) -> NavigationResult:
        """Handle multi-component navigation"""
        prioritized = self._prioritize_components(context.target_components)
        primary_target = prioritized[0]
        logger.debug("Multi-component handling: %d components, primary: %s", len(prioritized), primary_target)
        logger.success("Multi-component handling prepared successfully for primary target: %s", primary_target)
        return NavigationResult(
            success=True,
            chosen_path=primary_target,
            component_type="MULTI",
            dependencies=context.dependencies.get(primary_target, []),
            action_taken="HANDLE_MULTIPLE",
            navigation_history=[f"Multi-component handling: {len(prioritized)} files"],
            metadata={"component_count": len(prioritized), "components": [str(p) for p in prioritized]}
        )
        
    def _is_relevant_for_request(self, file_info: Any, request: str) -> bool:
        """Check if a file is relevant for the request"""
        request_lower = request.lower()
        file_name = file_info.path.name.lower()
        return any(keyword in file_name for keyword in request_lower.split())
        
    async def _analyze_dependencies(self, file_path: Path) -> List[Path]:
        """Analyze dependencies for a file"""
        logger.debug("Analyzing dependencies for: %s", file_path)
        analysis = await self.file_analyzer.analyze_file(file_path)
        dependencies = []
        if hasattr(analysis, 'imports'):
            for imp in analysis.imports:
                dep_path = self._import_to_path(imp)
                if dep_path and dep_path.exists():
                    dependencies.append(dep_path)
        logger.debug("Dependencies for %s: %s", file_path, dependencies)
        return dependencies
        
    def _import_to_path(self, import_name: str) -> Optional[Path]:
        """Convert an import name to a possible file path"""
        parts = import_name.split('.')
        possible_path = self.workspace.joinpath(*parts).with_suffix('.py')
        return possible_path if possible_path.exists() else None
        
    def _determine_new_file_path(self, request: str) -> Path:
        """Determine an appropriate path for a new file"""
        component_type = self._determine_component_type(request)
        base_name = self._generate_file_name(request)
        if component_type == "FRONTEND":
            return self.workspace / "frontend" / base_name
        elif component_type == "BACKEND":
            return self.workspace / "backend" / base_name
        elif component_type == "TEST":
            return self.workspace / "tests" / f"test_{base_name}"
        else:
            return self.workspace / base_name
            
    def _determine_component_type(self, request: str) -> str:
        """Determine component type based on the request"""
        request_lower = request.lower()
        if any(word in request_lower for word in ["test", "testing", "validate"]):
            return "TEST"
        elif any(word in request_lower for word in ["api", "database", "model", "backend"]):
            return "BACKEND"
        elif any(word in request_lower for word in ["ui", "interface", "frontend"]):
            return "FRONTEND"
        return "UNKNOWN"
        
    def _generate_file_name(self, request: str) -> str:
        """Generate a file name from the request"""
        words = request.lower().split()[:3]
        base_name = "_".join(word.strip() for word in words if word.isalnum())
        if self._determine_component_type(request) == "FRONTEND":
            return f"{base_name}.html"
        else:
            return f"{base_name}.py"
            
    def _prioritize_components(self, components: List[Path]) -> List[Path]:
        """Prioritize components for multi-handling"""
        def priority_score(path: Path) -> int:
            score = 0
            if path.suffix == ".py":
                score += 5
            if "test" in path.stem.lower():
                score -= 2
            if "main" in path.stem.lower():
                score += 3
            return score
        prioritized = sorted(components, key=priority_score, reverse=True)
        logger.debug("Prioritized components: %s", prioritized)
        return prioritized

```

---

# ..\..\CodeMate\cmate\core\prompt_manager.py
## File: ..\..\CodeMate\cmate\core\prompt_manager.py

```py
# ..\..\CodeMate\cmate\core\prompt_manager.py
# ..\..\cmate\core\prompt_manager.py
"""
prompt_manager.py

Manages the system's prompt templates. Loads prompts from configuration
files (in YAML format) and allows adding, updating, and retrieving formatted prompts.
To avoid confusion for the agent, each prompt contains detailed guidance.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import os
import logging

# For loading YAML files
try:
    import yaml
except ImportError:
    yaml = None
    print("Warning: PyYAML is missing. Install with 'pip install pyyaml' to load YAML prompts.")

logger = logging.getLogger(__name__)

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
    # Assuming version is needed for update_template (if not, you may remove it)
    version: str = "1.0.0"

class PromptManager:
    def __init__(self, prompt_dir: Optional[str] = None):
        self.prompt_dir = Path(prompt_dir) if prompt_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        logger.info("Initializing PromptManager with directory: %s", self.prompt_dir)
        self._load_prompts()
        self._load_default_prompts()
        logger.success("PromptManager loaded successfully with %d templates.", len(self.templates))

    def _load_prompts(self) -> None:
        """Load prompts from YAML files in prompt_dir."""
        if self.prompt_dir.exists():
            for prompt_file in self.prompt_dir.glob("*.yaml"):
                try:
                    with open(prompt_file, 'r', encoding='utf-8') as f:
                        if yaml:
                            data = yaml.safe_load(f)
                        else:
                            data = {}  # If YAML is missing, skip
                        for name, template_data in data.items():
                            self.templates[name] = PromptTemplate(
                                name=name,
                                content=template_data["content"],
                                variables=template_data.get("variables", []),
                                description=template_data.get("description", ""),
                                category=template_data.get("category", "general"),
                                metadata=template_data.get("metadata", {})
                            )
                    logger.debug("Loaded prompts from file: %s", prompt_file)
                except Exception as e:
                    logger.error("Error loading prompt file %s: %s", prompt_file, str(e))
        else:
            logger.warning("Prompt directory does not exist: %s", self.prompt_dir)

    def _load_default_prompts(self) -> None:
        """
        If no prompts have been loaded or to supplement them,
        load some default prompts with detailed guidance.
        """
        defaults = {
            "system_prompt": PromptTemplate(
                name="system_prompt",
                content=(
                    "You are a semi-autonomous agent specialized in analyzing, modifying, and testing code. "
                    "Work systematically: analyze the situation, plan carefully, implement with meticulous adherence "
                    "to coding style, and test thoroughly. Only use files in the ./Workspace directory. Be diligent with "
                    "documentation and debugging as needed."
                ),
                variables=[],
                description="Base prompt for agent initialization with clear guidance",
                category="system"
            ),
            "analysis_prompt": PromptTemplate(
                name="analysis_prompt",
                content=(
                    "Analyze the following files and provide an overview of the structure, identifying key components, "
                    "potential issues, and dependencies. Prepare a list of recommended actions.\nFiles: {files}"
                ),
                variables=["files"],
                description="Detailed prompt for file analysis with step-by-step guidance",
                category="analysis"
            ),
            "implementation_prompt": PromptTemplate(
                name="implementation_prompt",
                content=(
                    "Implement the requested changes according to the following guidelines:\n"
                    "1. Follow the existing coding style meticulously.\n"
                    "2. Add appropriate documentation to the code.\n"
                    "3. Write unit tests to validate the changes.\n"
                    "4. Incorporate robust error handling.\n\n"
                    "Changes: {changes}\nAffected files: {files}"
                ),
                variables=["changes", "files"],
                description="Prompt for implementation steps with clear instructions",
                category="implementation"
            ),
            "test_prompt": PromptTemplate(
                name="test_prompt",
                content=(
                    "Create tests for the following changes:\n"
                    "1. Unit tests for the new functionality.\n"
                    "2. Integration tests where necessary.\n"
                    "3. Coverage of edge cases and error handling.\n\n"
                    "Implementation: {implementation}\nFiles to test: {files}"
                ),
                variables=["implementation", "files"],
                description="Prompt for test development with detailed requirements",
                category="testing"
            )
        }
        for key, prompt in defaults.items():
            if key not in self.templates:
                self.templates[key] = prompt
                logger.debug("Default prompt added: %s", key)

    def get_prompt(self, name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        if name not in self.templates:
            error_msg = f"Prompt template '{name}' not found"
            logger.error(error_msg)
            raise KeyError(error_msg)
        template = self.templates[name]
        content = template.content
        if variables:
            try:
                content = content.format(**variables)
            except KeyError as e:
                error_msg = f"Missing required variable {str(e)} for template {name}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        template.last_used = datetime.now()
        template.usage_count += 1
        logger.debug("Retrieved prompt '%s' with variables: %s", name, variables)
        return content

    def add_template(self, name: str, content: str, variables: List[str], description: str = "", category: str = "custom", metadata: Optional[Dict[str, Any]] = None) -> None:
        if name in self.templates:
            error_msg = f"Template '{name}' already exists"
            logger.error(error_msg)
            raise ValueError(error_msg)
        self.templates[name] = PromptTemplate(
            name=name,
            content=content,
            variables=variables,
            description=description,
            category=category,
            metadata=metadata or {}
        )
        logger.success("Added new template: %s", name)

    def update_template(self, name: str, content: Optional[str] = None, variables: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        if name not in self.templates:
            error_msg = f"Template '{name}' not found"
            logger.error(error_msg)
            raise KeyError(error_msg)
        template = self.templates[name]
        if content is not None:
            template.content = content
        if variables is not None:
            template.variables = variables
        if metadata is not None:
            template.metadata.update(metadata)
        # Update version (simple increment)
        version_parts = template.version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        template.version = '.'.join(version_parts)
        logger.success("Updated template '%s' to version %s", name, template.version)

    def get_templates_by_category(self, category: str) -> List[PromptTemplate]:
        return [t for t in self.templates.values() if t.category == category]

    def get_template_variables(self, name: str) -> List[str]:
        if name not in self.templates:
            error_msg = f"Template '{name}' not found"
            logger.error(error_msg)
            raise KeyError(error_msg)
        return self.templates[name].variables.copy()

```

---

# ..\..\CodeMate\cmate\core\state_manager.py
## File: ..\..\CodeMate\cmate\core\state_manager.py

```py
# ..\..\CodeMate\cmate\core\state_manager.py
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

```

---

# ..\..\CodeMate\cmate\core\workflow_manager.py
## File: ..\..\CodeMate\cmate\core\workflow_manager.py

```py
# ..\..\CodeMate\cmate\core\workflow_manager.py
# ..\..\cmate\core\workflow_manager.py
"""
cmate/core/workflow_manager.py

Enhanced workflow manager with support for:
- Navigation workflows
- Multi-component operations
- Advanced state tracking
- Step-based validation
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from uuid import UUID, uuid4
import logging

from .state_manager import AgentState
from .event_bus import EventBus, EventCategory, EventPriority
from ..utils.logger import get_logger

logger = get_logger(__name__)

class WorkflowStepType(Enum):
    """Extended workflow step types"""
    WORKSPACE_SCAN = "workspace_scan"
    COMPONENT_ANALYSIS = "component_analysis"
    DEPENDENCY_ANALYSIS = "dependency_analysis"
    PATH_TRANSITION = "path_transition"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    CODE_GENERATION = "code_generation"
    CODE_MODIFICATION = "code_modification"
    TEST_GENERATION = "test_generation"
    TEST_EXECUTION = "test_execution"
    VALIDATION = "validation"
    ERROR_ANALYSIS = "error_analysis"
    RECOVERY = "recovery"

class WorkflowType(Enum):
    """Types of workflows"""
    NAVIGATION = "navigation"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    RECOVERY = "recovery"
    COMPOSITE = "composite"

@dataclass
class WorkflowStep:
    """Enhanced workflow step"""
    id: UUID
    type: WorkflowStepType
    action: Callable[..., Any]
    description: str
    required: bool = True
    dependencies: List[UUID] = field(default_factory=list)
    validation_steps: List[Callable] = field(default_factory=list)
    completed: bool = False
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3
    execution_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Workflow:
    """Enhanced workflow definition"""
    id: UUID
    type: WorkflowType
    name: str
    description: str
    steps: List[WorkflowStep]
    current_step: Optional[UUID] = None
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    parent_workflow: Optional[UUID] = None
    child_workflows: List[UUID] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowContext:
    """Context for workflow execution"""
    workflow_id: UUID
    current_path: Optional[Path] = None
    target_path: Optional[Path] = None
    components: List[Path] = field(default_factory=list)
    dependencies: Dict[Path, List[Path]] = field(default_factory=dict)
    state_history: List[AgentState] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowManager:
    """Enhanced workflow manager with navigation support"""
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        self.logger = get_logger(__name__)
        self.event_bus = event_bus or EventBus()
        self.workflows: Dict[UUID, Workflow] = {}
        self.contexts: Dict[UUID, WorkflowContext] = {}
        self.active_workflow: Optional[UUID] = None
        self._worker_task: Optional[asyncio.Task] = None
        self._running = False
        
        # Initialize step handlers
        self.step_handlers = {
            WorkflowStepType.WORKSPACE_SCAN: self._handle_workspace_scan,
            WorkflowStepType.COMPONENT_ANALYSIS: self._handle_component_analysis,
            WorkflowStepType.DEPENDENCY_ANALYSIS: self._handle_dependency_analysis,
            WorkflowStepType.PATH_TRANSITION: self._handle_path_transition,
            # Additional step handlers can be added here.
        }
        self.logger.info("WorkflowManager initialized.")
        self.logger.success("WorkflowManager initialized successfully.")

    async def start(self) -> None:
        """Start workflow processing"""
        if not self._running:
            self._running = True
            self._worker_task = asyncio.create_task(self._workflow_worker())
            self.logger.success("Workflow manager started successfully.")

    async def shutdown(self) -> None:
        """Gracefully shut down workflow processing"""
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
            self._worker_task = None
        self.logger.success("Workflow manager shut down successfully.")

    async def create_workflow(
        self,
        workflow_type: WorkflowType,
        name: str,
        description: str,
        context: Optional[Dict[str, Any]] = None,
        parent_id: Optional[UUID] = None
    ) -> Workflow:
        """Create a new workflow"""
        workflow_id = uuid4()
        self.logger.info("Creating workflow '%s' of type '%s' with id: %s", name, workflow_type.value, workflow_id)
        
        workflow_context = WorkflowContext(
            workflow_id=workflow_id,
            metadata=context or {}
        )
        self.contexts[workflow_id] = workflow_context
        
        steps = await self._create_workflow_steps(workflow_type, context or {})
        workflow = Workflow(
            id=workflow_id,
            type=workflow_type,
            name=name,
            description=description,
            steps=steps,
            parent_workflow=parent_id,
            metadata=context or {}
        )
        self.workflows[workflow_id] = workflow
        
        if parent_id and parent_id in self.workflows:
            self.workflows[parent_id].child_workflows.append(workflow_id)
            self.logger.debug("Linked workflow %s as child of %s", workflow_id, parent_id)
        
        await self.event_bus.publish(
            "workflow_created",
            {"workflow_id": str(workflow_id), "type": workflow_type.value, "name": name},
            category=EventCategory.SYSTEM
        )
        self.logger.success("Workflow '%s' created successfully.", name)
        return workflow

    async def _create_workflow_steps(
        self,
        workflow_type: WorkflowType,
        context: Dict[str, Any]
    ) -> List[WorkflowStep]:
        """Create appropriate steps for the workflow type"""
        steps = []
        if workflow_type == WorkflowType.NAVIGATION:
            steps.extend([
                WorkflowStep(
                    id=uuid4(),
                    type=WorkflowStepType.WORKSPACE_SCAN,
                    action=self.step_handlers[WorkflowStepType.WORKSPACE_SCAN],
                    description="Scan workspace for components"
                ),
                WorkflowStep(
                    id=uuid4(),
                    type=WorkflowStepType.COMPONENT_ANALYSIS,
                    action=self.step_handlers[WorkflowStepType.COMPONENT_ANALYSIS],
                    description="Analyze selected component"
                ),
                WorkflowStep(
                    id=uuid4(),
                    type=WorkflowStepType.DEPENDENCY_ANALYSIS,
                    action=self.step_handlers[WorkflowStepType.DEPENDENCY_ANALYSIS],
                    description="Analyze component dependencies"
                )
            ])
            if context.get("target_path"):
                steps.append(
                    WorkflowStep(
                        id=uuid4(),
                        type=WorkflowStepType.PATH_TRANSITION,
                        action=self.step_handlers[WorkflowStepType.PATH_TRANSITION],
                        description="Transition to target path"
                    )
                )
        # Additional workflow types can be handled here.
        self.logger.debug("Workflow steps created: %s", steps)
        return steps

    async def execute_workflow(self, workflow_id: UUID) -> Dict[str, Any]:
        """Execute a workflow and return the results"""
        if workflow_id not in self.workflows:
            error_msg = f"Workflow not found: {workflow_id}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
            
        workflow = self.workflows[workflow_id]
        context = self.contexts[workflow_id]
        self.active_workflow = workflow_id
        self.logger.info("Executing workflow %s (%s)", workflow.name, workflow_id)
        
        try:
            for step in workflow.steps:
                workflow.current_step = step.id
                await self._check_step_dependencies(step, workflow)
                total_execution_time = 0.0
                success = False
                while not success:
                    attempt_start = datetime.now()
                    try:
                        self.logger.debug("Executing step %s (%s)", step.id, step.description)
                        step.result = await step.action(context)
                        step.completed = True
                        success = True
                        self.logger.info("Step %s completed successfully.", step.id)
                    except Exception as e:
                        step.error = str(e)
                        step.retries += 1
                        self.logger.warning("Step %s failed on attempt %d: %s", step.id, step.retries, str(e))
                        if step.retries >= step.max_retries:
                            self.logger.error("Step %s exceeded maximum retries.", step.id)
                            raise
                    finally:
                        total_execution_time += (datetime.now() - attempt_start).total_seconds()
                step.execution_time = total_execution_time
                for validation in step.validation_steps:
                    await validation(step.result)
                await self._update_context(context, step)
            workflow.status = "completed"
            workflow.completed_at = datetime.now()
            self.logger.success("Workflow %s completed successfully in %s seconds.", workflow.name,
                             sum(s.execution_time or 0 for s in workflow.steps))
            return {
                "success": True,
                "workflow_id": str(workflow_id),
                "steps_completed": len(workflow.steps),
                "execution_time": sum(s.execution_time or 0 for s in workflow.steps)
            }
        except Exception as e:
            workflow.status = "error"
            self.logger.error("Workflow %s failed: %s", workflow.name, str(e))
            return {
                "success": False,
                "workflow_id": str(workflow_id),
                "error": str(e)
            }
        finally:
            if self.active_workflow == workflow_id:
                self.active_workflow = None

    async def _check_step_dependencies(self, step: WorkflowStep, workflow: Workflow) -> None:
        """Check if the dependencies for a step are met"""
        for dep_id in step.dependencies:
            dep_step = next((s for s in workflow.steps if s.id == dep_id), None)
            if not dep_step or not dep_step.completed:
                error_msg = f"Dependency {dep_id} not met for step {step.id}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

    async def _update_context(self, context: WorkflowContext, step: WorkflowStep) -> None:
        """Update the workflow context based on the step result"""
        if not step.result:
            return
        if step.type == WorkflowStepType.WORKSPACE_SCAN:
            context.components = step.result.get("components", [])
        elif step.type == WorkflowStepType.COMPONENT_ANALYSIS:
            context.metadata["component_info"] = step.result.get("component_info", {})
        elif step.type == WorkflowStepType.DEPENDENCY_ANALYSIS:
            context.dependencies.update(step.result.get("dependencies", {}))
        elif step.type == WorkflowStepType.PATH_TRANSITION:
            context.current_path = step.result.get("new_path")
        self.logger.debug("Workflow context updated after step %s", step.id)

    async def _workflow_worker(self) -> None:
        """Background worker for processing workflows"""
        self.logger.info("Workflow worker started.")
        while self._running:
            try:
                for workflow in list(self.workflows.values()):
                    if workflow.status == "pending":
                        self.logger.debug("Auto-executing pending workflow: %s", workflow.id)
                        await self.execute_workflow(workflow.id)
                await asyncio.sleep(1)
            except Exception as e:
                self.logger.error("Error in workflow worker: %s", str(e))
                await asyncio.sleep(1)

    # Step handler implementations
    async def _handle_workspace_scan(self, context: WorkflowContext) -> Dict[str, Any]:
        self.logger.debug("Handling workspace scan step.")
        # Implementation would use a workspace scanner
        return {"components": []}

    async def _handle_component_analysis(self, context: WorkflowContext) -> Dict[str, Any]:
        self.logger.debug("Handling component analysis step.")
        # Implementation would use a component analyzer
        return {"component_info": {}}

    async def _handle_dependency_analysis(self, context: WorkflowContext) -> Dict[str, Any]:
        self.logger.debug("Handling dependency analysis step.")
        # Implementation would use a dependency analyzer
        return {"dependencies": {}}

    async def _handle_path_transition(self, context: WorkflowContext) -> Dict[str, Any]:
        self.logger.debug("Handling path transition step.")
        # Implementation would handle path changes
        return {"new_path": context.target_path}

    def get_active_workflow(self) -> Optional[UUID]:
        """Get the ID of the currently active workflow"""
        return self.active_workflow

    def get_workflow_status(self, workflow_id: UUID) -> Optional[Dict[str, Any]]:
        """Get detailed status of a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        return {
            "id": str(workflow.id),
            "type": workflow.type.value,
            "status": workflow.status,
            "current_step": str(workflow.current_step) if workflow.current_step else None,
            "steps_total": len(workflow.steps),
            "steps_completed": len([s for s in workflow.steps if s.completed]),
            "created_at": workflow.created_at.isoformat(),
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None
        }

    def get_workflow_chain(self, workflow_id: UUID) -> List[UUID]:
        """Get the full chain of related workflows"""
        chain = []
        workflow = self.workflows.get(workflow_id)
        current = workflow
        while current and current.parent_workflow:
            chain.insert(0, current.parent_workflow)
            current = self.workflows.get(current.parent_workflow)
        if workflow:
            chain.append(workflow.id)
        if workflow:
            chain.extend(workflow.child_workflows)
        self.logger.debug("Workflow chain for %s: %s", workflow_id, chain)
        return chain

    def analyze_workflow_metrics(self, workflow_id: UUID) -> Dict[str, Any]:
        """Analyze execution metrics for a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {}
        completed_steps = [s for s in workflow.steps if s.completed]
        failed_steps = [s for s in workflow.steps if s.error]
        metrics = {
            "total_steps": len(workflow.steps),
            "completed_steps": len(completed_steps),
            "failed_steps": len(failed_steps),
            "total_execution_time": sum(s.execution_time or 0 for s in workflow.steps),
            "average_step_time": (sum(s.execution_time or 0 for s in completed_steps) / len(completed_steps)
                                  if completed_steps else 0),
            "retry_count": sum(s.retries for s in workflow.steps),
            "error_rate": (len(failed_steps) / len(workflow.steps)) if workflow.steps else 0,
            "steps_by_type": self._count_steps_by_type(workflow),
            "execution_timeline": self._generate_timeline(workflow),
            "bottlenecks": self._identify_bottlenecks(workflow)
        }
        if workflow.child_workflows:
            child_metrics = {}
            for child_id in workflow.child_workflows:
                child_metrics[str(child_id)] = self.analyze_workflow_metrics(child_id)
            metrics["child_workflows"] = child_metrics
        self.logger.debug("Workflow metrics for %s: %s", workflow_id, metrics)
        return metrics

    def _count_steps_by_type(self, workflow: Workflow) -> Dict[str, int]:
        type_counts = {}
        for step in workflow.steps:
            type_name = step.type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        return type_counts

    def _generate_timeline(self, workflow: Workflow) -> List[Dict[str, Any]]:
        timeline = []
        for step in workflow.steps:
            if step.completed and step.execution_time is not None:
                timeline.append({
                    "step_id": str(step.id),
                    "type": step.type.value,
                    "execution_time": step.execution_time,
                    "retries": step.retries,
                    "status": "completed" if step.completed else "failed" if step.error else "pending"
                })
        return timeline

    def _identify_bottlenecks(self, workflow: Workflow) -> List[Dict[str, Any]]:
        bottlenecks = []
        avg_time = (sum(s.execution_time or 0 for s in workflow.steps) / len(workflow.steps)
                    if workflow.steps else 0)
        for step in workflow.steps:
            if step.execution_time and step.execution_time > (avg_time * 1.5):
                bottlenecks.append({
                    "step_id": str(step.id),
                    "type": step.type.value,
                    "execution_time": step.execution_time,
                    "avg_time_ratio": (step.execution_time / avg_time) if avg_time else 0,
                    "retries": step.retries
                })
        return sorted(bottlenecks, key=lambda x: x["execution_time"], reverse=True)

    def clear_completed_workflows(self, max_age_hours: int = 24) -> int:
        threshold = datetime.now() - timedelta(hours=max_age_hours)
        removed = 0
        for workflow_id, workflow in list(self.workflows.items()):
            if (workflow.status == "completed" and 
                workflow.completed_at and 
                workflow.completed_at < threshold):
                del self.workflows[workflow_id]
                removed += 1
        self.logger.success("Cleared %d completed workflows older than %d hours.", removed, max_age_hours)
        return removed

```

---

