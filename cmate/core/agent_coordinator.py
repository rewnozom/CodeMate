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
