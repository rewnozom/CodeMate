# Project Details

# Table of Contents
- [..\src\main.py](#-src-mainpy)
- [..\src\__init__.py](#-src-__init__py)
- [..\src\config\prompts.py](#-src-config-promptspy)
- [..\src\config\__init__.py](#-src-config-__init__py)
- [..\src\core\agent_coordinator.py](#-src-core-agent_coordinatorpy)
- [..\src\core\context_manager.py](#-src-core-context_managerpy)
- [..\src\core\core-base.py](#-src-core-core-basepy)
- [..\src\core\event_bus.py](#-src-core-event_buspy)
- [..\src\core\memory_manager.py](#-src-core-memory_managerpy)
- [..\src\core\prompt_manager.py](#-src-core-prompt_managerpy)
- [..\src\core\state_manager.py](#-src-core-state_managerpy)
- [..\src\core\workflow_manager.py](#-src-core-workflow_managerpy)
- [..\src\core\__init__.py](#-src-core-__init__py)
- [..\src\file_services\file_analyzer.py](#-src-file_services-file_analyzerpy)
- [..\src\file_services\file_watcher.py](#-src-file_services-file_watcherpy)
- [..\src\file_services\workspace_scanner.py](#-src-file_services-workspace_scannerpy)
- [..\src\file_services\__init__.py](#-src-file_services-__init__py)
- [..\src\interfaces\cli_interface.py](#-src-interfaces-cli_interfacepy)
- [..\src\interfaces\request_handler.py](#-src-interfaces-request_handlerpy)
- [..\src\interfaces\response_formatter.py](#-src-interfaces-response_formatterpy)
- [..\src\interfaces\terminal_manager.py](#-src-interfaces-terminal_managerpy)
- [..\src\interfaces\__init__.py](#-src-interfaces-__init__py)
- [..\src\llm\conversation.py](#-src-llm-conversationpy)
- [..\src\llm\llm_agent.py](#-src-llm-llm_agentpy)
- [..\src\llm\llm_manager.py](#-src-llm-llm_managerpy)
- [..\src\llm\model_selector.py](#-src-llm-model_selectorpy)
- [..\src\llm\prompt_optimizer.py](#-src-llm-prompt_optimizerpy)
- [..\src\llm\response_parser.py](#-src-llm-response_parserpy)
- [..\src\storage\cache_manager.py](#-src-storage-cache_managerpy)
- [..\src\storage\persistence_manager.py](#-src-storage-persistence_managerpy)
- [..\src\storage\__init__.py](#-src-storage-__init__py)
- [..\src\task_management\checklist_manager.py](#-src-task_management-checklist_managerpy)
- [..\src\task_management\process_manager.py](#-src-task_management-process_managerpy)
- [..\src\task_management\progress_tracker copy.py](#-src-task_management-progress_tracker-copypy)
- [..\src\task_management\progress_tracker.py](#-src-task_management-progress_trackerpy)
- [..\src\task_management\task_prioritizer.py](#-src-task_management-task_prioritizerpy)
- [..\src\task_management\__init__.py](#-src-task_management-__init__py)
- [..\src\utils\config.py](#-src-utils-configpy)
- [..\src\utils\error_handler.py](#-src-utils-error_handlerpy)
- [..\src\utils\logger.py](#-src-utils-loggerpy)
- [..\src\utils\log_analyzer.py](#-src-utils-log_analyzerpy)
- [..\src\utils\prompt_templates.py](#-src-utils-prompt_templatespy)
- [..\src\utils\system_metrics.py](#-src-utils-system_metricspy)
- [..\src\utils\token_counter.py](#-src-utils-token_counterpy)
- [..\src\utils\__init__.py](#-src-utils-__init__py)
- [..\src\validation\backend_validator.py](#-src-validation-backend_validatorpy)
- [..\src\validation\frontend_validator.py](#-src-validation-frontend_validatorpy)
- [..\src\validation\implementation_validator.py](#-src-validation-implementation_validatorpy)
- [..\src\validation\test_manager.py](#-src-validation-test_managerpy)
- [..\src\validation\validation_rules.py](#-src-validation-validation_rulespy)
- [..\src\validation\__init__.py](#-src-validation-__init__py)
- [..\.env.example](#-envexample)
- [..\config\default.yaml](#-config-defaultyaml)
- [..\config\development.yaml](#-config-developmentyaml)
- [..\config\gunicorn.py](#-config-gunicornpy)
- [..\config\local.yaml](#-config-localyaml)
- [..\config\production.yaml](#-config-productionyaml)
- [..\config\prompts\base_prompts.yaml](#-config-prompts-base_promptsyaml)
- [..\config\prompts\error_prompts.yaml](#-config-prompts-error_promptsyaml)
- [..\config\prompts\workflow_prompts.yaml](#-config-prompts-workflow_promptsyaml)
- [..\.dockerignore](#-dockerignore)
- [..\.editorconfig](#-editorconfig)
- [..\.gitignore](#-gitignore)
- [..\.gitlab-ci.yml](#-gitlab-ciyml)
- [..\.pre-commit-config.yaml](#-pre-commit-configyaml)
- [..\__init__.py](#-__init__py)
- [..\cli_CodeMate.bat](#-cli_CodeMatebat)
- [..\deploy.sh](#-deploysh)
- [..\docker-compose.dev.yml](#-docker-composedevyml)
- [..\docker-compose.yml](#-docker-composeyml)
- [..\install_CodeMate.bat](#-install_CodeMatebat)
- [..\Makefile](#-Makefile)
- [..\pyproject.toml](#-pyprojecttoml)
- [..\pytest.ini](#-pytestini)
- [..\README.md](#-READMEmd)
- [..\run_tests.sh](#-run_testssh)
- [..\settings.toml](#-settingstoml)
- [..\setup.cfg](#-setupcfg)
- [..\setup.py](#-setuppy)
- [..\tox.ini](#-toxini)


# ..\..\src\main.py
## File: ..\..\src\main.py

```py
# ..\..\src\main.py
# src/cmate/main.py
import sys
import os
import asyncio
import logging
from pathlib import Path
import yaml
import typer
from rich.console import Console
from rich.logging import RichHandler
from typing import Optional, Dict, Any

from cmate.core.agent_coordinator import AgentCoordinator, AgentConfig
from cmate.core.state_manager import StateManager
from cmate.core.workflow_manager import WorkflowManager
from cmate.utils.logger import setup_logging
from cmate.utils.config import load_config
from cmate.interfaces.cli_interface import CLIInterface

app = typer.Typer(help="Semi-Autonomous Agent Assistant (CodeMate)")
console = Console()

def setup_system(config_path: Optional[str] = None) -> AgentCoordinator:
    """Setup and initialize system components."""
    config = load_config(config_path)
    setup_logging(
        log_level=config.get("general", {}).get("log_level", "INFO"),
        log_file=Path("logs/agent.log")
    )
    agent_config = AgentConfig(
        workspace_path=config.get("general", {}).get("workspace_path", "./Workspace"),
        max_files_per_scan=config.get("general", {}).get("max_files_per_scan", 10),
        context_window_size=config.get("llm", {}).get("context_window", 60000),
        auto_test=config.get("agent", {}).get("auto_test", True),
        debug_mode=config.get("general", {}).get("debug_mode", False)
    )
    state_manager = StateManager()
    workflow_manager = WorkflowManager()
    agent = AgentCoordinator(
        config=agent_config,
        state_manager=state_manager,
        workflow_manager=workflow_manager
    )
    return agent

@app.command()
def start(
    config: str = typer.Option(None, "--config", "-c", help="Path to configuration file"),
    interactive: bool = typer.Option(True, "--interactive", "-i", help="Start in interactive mode")
):
    """Start the agent system."""
    try:
        agent = setup_system(config)
        if interactive:
            cli = CLIInterface(agent)
            asyncio.run(cli.start())
        else:
            console.print("[green]Agent started in non-interactive mode[/green]")
            asyncio.run(agent.check_status())
    except Exception as e:
        console.print(f"[red]Error starting system: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def process(
    request: str = typer.Argument(..., help="Request to process"),
    config: str = typer.Option(None, "--config", "-c", help="Path to configuration file")
):
    """Process a single request."""
    try:
        agent = setup_system(config)
        result = asyncio.run(agent.process_request({
            "type": "process",
            "data": {"request": request}
        }))
        if result.get("success"):
            console.print("[green]Request processed successfully[/green]")
            console.print(result)
        else:
            console.print("[red]Error processing request[/red]")
            console.print(result)
    except Exception as e:
        console.print(f"[red]Error processing request: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def status(
    config: str = typer.Option(None, "--config", "-c", help="Path to configuration file")
):
    """Check agent status."""
    try:
        agent = setup_system(config)
        status = asyncio.run(agent.check_status())
        console.print("\n[bold]Agent Status[/bold]")
        console.print(f"State: {status['state']}")
        console.print(f"Active Workflow: {status['active_workflow']}")
        console.print("\n[bold]Metrics:[/bold]")
        for key, value in status["metrics"].items():
            console.print(f"{key}: {value}")
    except Exception as e:
        console.print(f"[red]Error checking status: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()

```

---

# ..\..\src\__init__.py
## File: ..\..\src\__init__.py

```py
# ..\..\src\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\src\config\prompts.py
## File: ..\..\src\config\prompts.py

```py
# ..\..\src\config\prompts.py
# src/config/prompts.py
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import yaml

@dataclass
class PromptTemplate:
    """Template for system prompts"""
    name: str
    content: str
    variables: List[str]
    description: str
    category: str
    version: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class PromptConfig:
    """Manages prompt templates and configurations"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        self.categories: Dict[str, List[str]] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load prompt configurations"""
        if not self.config_dir.exists():
            return

        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file) as f:
                    data = yaml.safe_load(f)
                    category = config_file.stem
                    
                    for name, template_data in data.items():
                        template = PromptTemplate(
                            name=name,
                            content=template_data["content"].strip(),
                            variables=template_data.get("variables", []),
                            description=template_data.get("description", ""),
                            category=template_data.get("category", category),
                            version=template_data.get("version", "1.0"),
                            metadata=template_data.get("metadata", {})
                        )
                        
                        self.templates[name] = template
                        
                        if template.category not in self.categories:
                            self.categories[template.category] = []
                        self.categories[template.category].append(name)
                        
            except Exception as e:
                print(f"Error loading prompt config {config_file}: {str(e)}")

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get prompt template by name"""
        return self.templates.get(name)

    def get_category_templates(self, category: str) -> List[PromptTemplate]:
        """Get all templates in category"""
        template_names = self.categories.get(category, [])
        return [self.templates[name] for name in template_names]

    def format_prompt(self, 
                     template_name: str,
                     variables: Dict[str, Any]) -> str:
        """Format prompt with variables"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")
            
        try:
            return template.content.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing required variable: {str(e)}")

    def add_template(self,
                    name: str,
                    content: str,
                    variables: List[str],
                    description: str = "",
                    category: str = "custom",
                    version: str = "1.0",
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add new prompt template"""
        if name in self.templates:
            raise ValueError(f"Template already exists: {name}")
            
        template = PromptTemplate(
            name=name,
            content=content.strip(),
            variables=variables,
            description=description,
            category=category,
            version=version,
            metadata=metadata or {}
        )
        
        self.templates[name] = template
        
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
        
        self._save_template(template)

    def update_template(self,
                       name: str,
                       content: Optional[str] = None,
                       variables: Optional[List[str]] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update existing template"""
        template = self.get_template(name)
        if not template:
            raise ValueError(f"Template not found: {name}")
            
        if content is not None:
            template.content = content.strip()
        if variables is not None:
            template.variables = variables
        if metadata is not None:
            template.metadata.update(metadata)
            
        template.updated_at = datetime.now()
        template.version = self._increment_version(template.version)
        
        self._save_template(template)

    def _increment_version(self, version: str) -> str:
        """Increment version number"""
        parts = version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return '.'.join(parts)

    def _save_template(self, template: PromptTemplate) -> None:
        """Save template to configuration file"""
        config_file = self.config_dir / f"{template.category}.yaml"
        
        # Load existing templates
        templates_data = {}
        if config_file.exists():
            with open(config_file) as f:
                templates_data = yaml.safe_load(f) or {}
                
        # Update template
        templates_data[template.name] = {
            "content": template.content,
            "variables": template.variables,
            "description": template.description,
            "category": template.category,
            "version": template.version,
            "metadata": template.metadata
        }
        
        # Save to file
        with open(config_file, 'w') as f:
            yaml.dump(templates_data, f, default_flow_style=False)


```

---

# ..\..\src\config\__init__.py
## File: ..\..\src\config\__init__.py

```py
# ..\..\src\config\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\src\core\agent_coordinator.py
## File: ..\..\src\core\agent_coordinator.py

```py
# ..\..\src\core\agent_coordinator.py
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
from core.state_manager import StateManager, AgentState
from core.workflow_manager import WorkflowManager
from core.prompt_manager import PromptManager
from core.memory_manager import MemoryManager
from core.event_bus import EventBus
from core.context_manager import ContextManager

# --------------------------------------------------
# Import LLM-related modules (assumed complete)
# --------------------------------------------------
from llm.llm_agent import llm_agent
from llm.llm_manager import llm_manager
from llm.conversation import conversation_manager

# --------------------------------------------------
# Import interface modules
# --------------------------------------------------
from interfaces.request_handler import RequestHandler
from interfaces.response_formatter import ResponseFormatter
from interfaces.terminal_manager import TerminalManager

# --------------------------------------------------
# Import storage modules
# --------------------------------------------------
from storage.cache_manager import CacheManager
from storage.persistence_manager import PersistenceManager

# --------------------------------------------------
# Import task management modules
# --------------------------------------------------
from task_management.checklist_manager import ChecklistManager
from task_management.process_manager import ProcessManager
from task_management.progress_tracker import ProgressTracker
from task_management.task_prioritizer import TaskPrioritizer

# --------------------------------------------------
# Import utility modules
# --------------------------------------------------
from utils.logger import get_logger
from utils.prompt_templates import PromptTemplateManager
from utils.system_metrics import MetricsCollector
from utils.token_counter import TokenCounter
from utils.log_analyzer import LogAnalyzer
from utils.error_handler import ErrorHandler, ErrorSeverity

# --------------------------------------------------
# Import validation modules
# --------------------------------------------------
from validation.backend_validator import BackendValidator
from validation.frontend_validator import FrontendValidator
from validation.implementation_validator import ImplementationValidator
from validation.test_manager import TestManager
from validation.validation_rules import ValidationRules


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

# ..\..\src\core\context_manager.py
## File: ..\..\src\core\context_manager.py

```py
# ..\..\src\core\context_manager.py
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

# ..\..\src\core\core-base.py
## File: ..\..\src\core\core-base.py

```py
# ..\..\src\core\core-base.py

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class AgentState(Enum):
    """Agent states"""
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    TESTING = "testing"
    ERROR = "error"
    WAITING_USER = "waiting_user"
    CONTEXT_SWITCHING = "context_switching"

@dataclass
class ContextWindow:
    """Manages context window content and tokens"""
    content: List[Dict[str, Any]] = field(default_factory=list)
    total_tokens: int = 0
    max_tokens: int = 60000

    def add_content(self, content: Dict[str, Any], token_count: int) -> bool:
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
        while self.content and self.total_tokens + needed_tokens > self.max_tokens:
            removed = self.content.pop(0)
            self.total_tokens -= removed["tokens"]

@dataclass
class StateMetadata:
    """Metadata for state tracking"""
    last_user_request: Optional[str] = None
    current_task: Optional[str] = None
    error_count: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

class StateManager:
    """Manages agent state and context"""
    
    def __init__(self):
        self.current_state: AgentState = AgentState.IDLE
        self.metadata: StateMetadata = StateMetadata()
        self.context_window: ContextWindow = ContextWindow()
        self.state_history: List[Dict[str, Any]] = []
        self.active_files: List[str] = []
        self.temporary_memory: Dict[str, Any] = {}
        
    def update_state(self, new_state: AgentState, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update agent state with new information"""
        self.current_state = new_state
        self.metadata.last_updated = datetime.now()
        
        if metadata:
            if "user_request" in metadata:
                self.metadata.last_user_request = metadata["user_request"]
            if "current_task" in metadata:
                self.metadata.current_task = metadata["current_task"]
        
        self._record_state_change(new_state, metadata)

    def add_to_context(self, content: Dict[str, Any], token_count: int) -> bool:
        """Add content to context window"""
        return self.context_window.add_content(content, token_count)

    def update_active_files(self, files: List[str]) -> None:
        """Update list of active files being processed"""
        self.active_files = files
        self._record_state_change(self.current_state, {"active_files": files})

    def record_error(self, error: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Record error information"""
        self.metadata.error_count += 1
        error_data = {
            "error": error,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "state": self.current_state.value
        }
        self._record_state_change(AgentState.ERROR, error_data)

    def get_current_context(self) -> List[Dict[str, Any]]:
        """Get current context window content"""
        return [item["data"] for item in self.context_window.content]

    def _record_state_change(self, state: AgentState, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record state change in history"""
        self.state_history.append({
            "state": state.value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "error_count": self.metadata.error_count
        })


from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
from uuid import UUID, uuid4

class WorkflowStepType(Enum):
    """Types of workflow steps"""
    FILE_ANALYSIS = "file_analysis"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    VALIDATION = "validation"
    USER_INTERACTION = "user_interaction"

@dataclass
class WorkflowStep:
    """Individual workflow step"""
    id: UUID
    type: WorkflowStepType
    action: Callable
    description: str
    required: bool = True
    dependencies: List[UUID] = field(default_factory=list)
    completed: bool = False
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3

@dataclass
class Workflow:
    """Complete workflow definition"""
    id: UUID
    name: str
    description: str
    steps: List[WorkflowStep]
    current_step: Optional[UUID] = None
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowManager:
    """Manages workflow creation and execution"""
    
    def __init__(self):
        self.workflows: Dict[UUID, Workflow] = {}
        self.active_workflow: Optional[UUID] = None
        self.step_handlers: Dict[WorkflowStepType, Callable] = {}
        self._initialize_handlers()
        
    def _initialize_handlers(self) -> None:
        """Initialize default step handlers"""
        self.step_handlers.update({
            WorkflowStepType.FILE_ANALYSIS: self._handle_file_analysis,
            WorkflowStepType.PLANNING: self._handle_planning,
            WorkflowStepType.IMPLEMENTATION: self._handle_implementation,
            WorkflowStepType.TESTING: self._handle_testing,
            WorkflowStepType.VALIDATION: self._handle_validation,
            WorkflowStepType.USER_INTERACTION: self._handle_user_interaction
        })

    async def create_workflow(self, request: Dict[str, Any]) -> Workflow:
        """Create new workflow from request"""
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
        return workflow

    async def execute_workflow(self, workflow_id: UUID) -> Dict[str, Any]:
        """Execute workflow steps"""
        workflow = self.workflows[workflow_id]
        self.active_workflow = workflow_id
        
        try:
            for step in workflow.steps:
                if step.dependencies:
                    await self._check_dependencies(step, workflow)
                
                workflow.current_step = step.id
                handler = self.step_handlers.get(step.type)
                if handler:
                    step.result = await handler(step, workflow)
                else:
                    step.result = await step.action()
                
                step.completed = True
                
            workflow.status = "completed"
            workflow.completed_at = datetime.now()
            return {"success": True, "workflow_id": workflow_id}
            
        except Exception as e:
            workflow.status = "error"
            return {"success": False, "error": str(e), "workflow_id": workflow_id}

    async def _check_dependencies(self, step: WorkflowStep, workflow: Workflow) -> None:
        """Check if step dependencies are met"""
        for dep_id in step.dependencies:
            dep_step = next((s for s in workflow.steps if s.id == dep_id), None)
            if not dep_step or not dep_step.completed:
                raise Exception(f"Dependency {dep_id} not met for step {step.id}")

    async def _handle_file_analysis(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle file analysis steps"""
        # Implementation specific to file analysis
        pass

    async def _handle_planning(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle planning steps"""
        # Implementation specific to planning
        pass

    async def _handle_implementation(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle implementation steps"""
        # Implementation specific to implementation
        pass

    async def _handle_testing(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle testing steps"""
        # Implementation specific to testing
        pass

    async def _handle_validation(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle validation steps"""
        # Implementation specific to validation
        pass

    async def _handle_user_interaction(self, step: WorkflowStep, workflow: Workflow) -> Dict[str, Any]:
        """Handle user interaction steps"""
        # Implementation specific to user interaction
        pass

    def _create_steps_from_request(self, request: Dict[str, Any]) -> List[WorkflowStep]:
        """Create workflow steps from request"""
        steps = []
        if "analyze_files" in request:
            steps.append(WorkflowStep(
                id=uuid4(),
                type=WorkflowStepType.FILE_ANALYSIS,
                action=self._handle_file_analysis,
                description="Analyze workspace files"
            ))
        # Add more step creation logic based on request
        return steps


```

---

# ..\..\src\core\event_bus.py
## File: ..\..\src\core\event_bus.py

```py
# ..\..\src\core\event_bus.py
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

# ..\..\src\core\memory_manager.py
## File: ..\..\src\core\memory_manager.py

```py
# ..\..\src\core\memory_manager.py
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

# ..\..\src\core\prompt_manager.py
## File: ..\..\src\core\prompt_manager.py

```py
# ..\..\src\core\prompt_manager.py
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

# ..\..\src\core\state_manager.py
## File: ..\..\src\core\state_manager.py

```py
# ..\..\src\core\state_manager.py
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

# ..\..\src\core\workflow_manager.py
## File: ..\..\src\core\workflow_manager.py

```py
# ..\..\src\core\workflow_manager.py
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

# ..\..\src\core\__init__.py
## File: ..\..\src\core\__init__.py

```py
# ..\..\src\core\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\src\file_services\file_analyzer.py
## File: ..\..\src\file_services\file_analyzer.py

```py
# ..\..\src\file_services\file_analyzer.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import ast
import re
import json
import yaml  # Ensure PyYAML is installed

@dataclass
class FileMetadata:
    """File metadata information"""
    path: Path
    size: int
    created: datetime
    modified: datetime
    type: str
    encoding: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CodeAnalysis:
    """Analysis of code structure"""
    imports: List[str]
    classes: List[str]
    functions: List[str]
    dependencies: List[str]
    complexity: int
    issues: List[str]
    metadata: Dict[str, Any]

@dataclass
class FileAnalysis:
    """Complete file analysis report"""
    path: Path
    size: int
    created: datetime
    modified: datetime
    file_type: str
    encoding: str
    line_count: int
    code_analysis: Optional[CodeAnalysis] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class FileAnalyzer:
    """
    Analyzes file content and structure.
    
    Supports multiple file types (Python, JavaScript, HTML, CSS, JSON, YAML).
    """
    
    def __init__(self):
        self.analyzers = {
            ".py": self._analyze_python,
            ".js": self._analyze_javascript,
            ".html": self._analyze_html,
            ".css": self._analyze_css,
            ".json": self._analyze_json,
            ".yaml": self._analyze_yaml,
            ".yml": self._analyze_yaml
        }
        self.encoding_detectors = ["utf-8", "latin-1", "cp1252"]

    async def analyze_file(self, file_path: Union[str, Path]) -> FileAnalysis:
        """Analyze a file's content and structure."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        stat = path.stat()
        file_type = path.suffix.lower()
        encoding = self._detect_encoding(path)
        try:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            line_count = len(content.splitlines())
            analyzer = self.analyzers.get(file_type)
            code_analysis = await analyzer(content) if analyzer else None
            return FileAnalysis(
                path=path,
                size=stat.st_size,
                created=datetime.fromtimestamp(stat.st_ctime),
                modified=datetime.fromtimestamp(stat.st_mtime),
                file_type=file_type,
                encoding=encoding,
                line_count=line_count,
                code_analysis=code_analysis,
                metadata={}
            )
        except Exception as e:
            raise RuntimeError(f"Analysis failed for {path}: {str(e)}")

    def _detect_encoding(self, path: Path) -> str:
        """Detect file encoding from a list of candidates."""
        for enc in self.encoding_detectors:
            try:
                with open(path, 'r', encoding=enc) as f:
                    f.read()
                return enc
            except UnicodeDecodeError:
                continue
        return "utf-8"  # Default encoding

    async def _analyze_python(self, content: str) -> CodeAnalysis:
        """Analyze Python code: imports, classes, functions, complexity, and issues."""
        imports = []
        classes = []
        functions = []
        dependencies = []
        issues = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(name.name for name in node.names)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.extend(f"{node.module}.{name.name}" for name in node.names)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            functions.append(f"{node.name}.{item.name}")
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
            complexity = self._calculate_complexity(tree)
            issues.extend(self._check_python_issues(tree))
        except SyntaxError as e:
            issues.append(f"Syntax error: {str(e)}")
        return CodeAnalysis(
            imports=list(set(imports)),
            classes=classes,
            functions=functions,
            dependencies=dependencies,
            complexity=complexity,
            issues=issues,
            metadata={}
        )

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate a simple complexity metric for Python code."""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.ExceptHandler)):
                complexity += 1
        return complexity

    def _check_python_issues(self, tree: ast.AST) -> List[str]:
        """Check for common Python code issues."""
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append("Bare except found; consider catching specific exceptions")
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        issues.append(f"Mutable default argument in function {node.name}")
        return issues

    async def _analyze_javascript(self, content: str) -> CodeAnalysis:
        """Analyze JavaScript code."""
        import_pattern = r'(?:import|require)\s*\(?[\'"](.*?)[\'"]'
        func_pattern = r'(?:function|const|let|var)\s+(\w+)\s*(?:=)?\s*(?:function)?\s*\('
        imports = re.findall(import_pattern, content)
        functions = re.findall(func_pattern, content)
        classes = re.findall(r'class\s+(\w+)', content)
        complexity = 1
        for pattern in [r'\bif\b', r'\bfor\b', r'\bwhile\b', r'\bswitch\b', r'\bcatch\b']:
            complexity += len(re.findall(pattern, content))
        issues = []
        if 'eval(' in content:
            issues.append("Use of eval() detected")
        return CodeAnalysis(
            imports=imports,
            classes=classes,
            functions=functions,
            dependencies=[],
            complexity=complexity,
            issues=issues,
            metadata={}
        )

    async def _analyze_html(self, content: str) -> CodeAnalysis:
        """Analyze HTML content by extracting dependencies."""
        script_pattern = r'<script[^>]*src=[\'"]([^\'"]+)[\'"]'
        style_pattern = r'<link[^>]*href=[\'"]([^\'"]+)[\'"]'
        dependencies = re.findall(script_pattern, content) + re.findall(style_pattern, content)
        issues = []
        if 'onclick=' in content:
            issues.append("Inline JavaScript events found")
        if 'style=' in content:
            issues.append("Inline styles found")
        return CodeAnalysis(
            imports=[],
            classes=[],
            functions=[],
            dependencies=list(set(dependencies)),
            complexity=0,
            issues=issues,
            metadata={}
        )

    async def _analyze_css(self, content: str) -> CodeAnalysis:
        """Analyze CSS content by extracting selectors and properties."""
        selectors = {}
        current_selector = None
        for line in content.splitlines():
            line = line.strip()
            if line.endswith('{'):
                current_selector = line[:-1].strip()
                selectors[current_selector] = []
            elif line.endswith('}'):
                current_selector = None
            elif current_selector and ':' in line:
                prop = line.split(':', 1)[0].strip()
                selectors[current_selector].append(prop)
        issues = []
        if '!important' in content:
            issues.append("Use of !important found")
        return CodeAnalysis(
            imports=[],
            classes=[],
            functions=[],
            dependencies=[],
            complexity=0,
            issues=issues,
            metadata={"selectors": selectors}
        )

    async def _analyze_json(self, content: str) -> CodeAnalysis:
        """Analyze JSON content."""
        issues = []
        try:
            data = json.loads(content)
            metadata = {"keys": list(data.keys()) if isinstance(data, dict) else None}
        except Exception as e:
            issues.append(f"JSON parse error: {str(e)}")
            metadata = {}
        return CodeAnalysis(
            imports=[],
            classes=[],
            functions=[],
            dependencies=[],
            complexity=0,
            issues=issues,
            metadata=metadata
        )

    async def _analyze_yaml(self, content: str) -> CodeAnalysis:
        """Analyze YAML content."""
        issues = []
        try:
            data = yaml.safe_load(content)
            metadata = {"keys": list(data.keys()) if isinstance(data, dict) else None}
        except Exception as e:
            issues.append(f"YAML parse error: {str(e)}")
            metadata = {}
        return CodeAnalysis(
            imports=[],
            classes=[],
            functions=[],
            dependencies=[],
            complexity=0,
            issues=issues,
            metadata=metadata
        )

```

---

# ..\..\src\file_services\file_watcher.py
## File: ..\..\src\file_services\file_watcher.py

```py
# ..\..\src\file_services\file_watcher.py
# src/file_services/file_watcher.py
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

@dataclass
class FileChange:
    """Record of file change"""
    path: Path
    event_type: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

class FileWatcher(FileSystemEventHandler):
    """Watches for file system changes"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        super().__init__()
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.observer = Observer()
        self.changes: List[FileChange] = []
        self.handlers: Dict[str, List[Callable]] = {
            "created": [],
            "modified": [],
            "deleted": [],
            "moved": []
        }
        self.watch_patterns: List[str] = []
        self.ignore_patterns: List[str] = [
            r'__pycache__',
            r'\.git',
            r'\.pytest_cache',
            r'*.pyc'
        ]
        self._is_running = False

    async def start_watching(self) -> None:
        """Start watching for changes"""
        if self._is_running:
            return
            
        self._is_running = True
        self.observer.schedule(self, str(self.workspace), recursive=True)
        self.observer.start()

    async def stop_watching(self) -> None:
        """Stop watching for changes"""
        if not self._is_running:
            return
            
        self._is_running = False
        self.observer.stop()
        self.observer.join()

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation event"""
        if not self._should_handle_event(event):
            return
            
        change = FileChange(
            path=Path(event.src_path).relative_to(self.workspace),
            event_type="created",
            timestamp=datetime.now()
        )
        self.changes.append(change)
        
        for handler in self.handlers["created"]:
            asyncio.create_task(handler(change))

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification event"""
        if not self._should_handle_event(event):
            return
            
        change = FileChange(
            path=Path(event.src_path).relative_to(self.workspace),
            event_type="modified",
            timestamp=datetime.now()
        )
        self.changes.append(change)
        
        for handler in self.handlers["modified"]:
            asyncio.create_task(handler(change))

    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file deletion event"""
        if not self._should_handle_event(event):
            return
            
        change = FileChange(
            path=Path(event.src_path).relative_to(self.workspace),
            event_type="deleted",
            timestamp=datetime.now()
        )
        self.changes.append(change)
        
        for handler in self.handlers["deleted"]:
            asyncio.create_task(handler(change))

    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move event"""
        if not self._should_handle_event(event):
            return
            
        change = FileChange(
            path=Path(event.dest_path).relative_to(self.workspace),
            event_type="moved",
            timestamp=datetime.now(),
            details={
                "source_path": str(Path(event.src_path).relative_to(self.workspace))
            }
        )
        self.changes.append(change)
        
        for handler in self.handlers["moved"]:
            asyncio.create_task(handler(change))

    def add_handler(self, event_type: str, handler: Callable) -> None:
        """Add event handler"""
        if event_type not in self.handlers:
            raise ValueError(f"Invalid event type: {event_type}")
        self.handlers[event_type].append(handler)

    def remove_handler(self, event_type: str, handler: Callable) -> None:
        """Remove event handler"""
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)

    def add_watch_pattern(self, pattern: str) -> None:
        """Add pattern to watch"""
        self.watch_patterns.append(pattern)

    def add_ignore_pattern(self, pattern: str) -> None:
        """Add pattern to ignore"""
        self.ignore_patterns.append(pattern)

    def get_changes(self, 
                   limit: Optional[int] = None,
                   event_type: Optional[str] = None) -> List[FileChange]:
        """Get recorded changes"""
        changes = self.changes
        if event_type:
            changes = [c for c in changes if c.event_type == event_type]
        if limit:
            changes = changes[-limit:]
        return changes

    def clear_changes(self) -> None:
        """Clear recorded changes"""
        self.changes.clear()

    def _should_handle_event(self, event: FileSystemEvent) -> bool:
        """Check if event should be handled"""
        path = Path(event.src_path)
        
        # Check ignore patterns
        if any(path.match(pattern) for pattern in self.ignore_patterns):
            return False
            
        # Check watch patterns
        if self.watch_patterns:
            return any(path.match(pattern) for pattern in self.watch_patterns)
            
        return True

    async def get_recent_changes(self, 
                               seconds: int = 60,
                               event_type: Optional[str] = None) -> List[FileChange]:
        """Get changes from last n seconds"""
        now = datetime.now()
        changes = [
            change for change in self.changes
            if (now - change.timestamp).total_seconds() <= seconds
            and (not event_type or change.event_type == event_type)
        ]
        return changes
```

---

# ..\..\src\file_services\workspace_scanner.py
## File: ..\..\src\file_services\workspace_scanner.py

```py
# ..\..\src\file_services\workspace_scanner.py
# src/file_services/workspace_scanner.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import re
import asyncio

@dataclass
class FileInfo:
    """Information about a file"""
    path: Path
    size: int
    created: datetime
    modified: datetime
    file_type: str
    content_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ScanResult:
    """Result of workspace scan"""
    timestamp: datetime
    files: List[FileInfo]
    total_size: int
    file_types: Dict[str, int]
    metadata: Dict[str, Any]

class WorkspaceScanner:
    """Scans workspace directory structure"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.ignored_patterns = [
            r'__pycache__',
            r'\.git',
            r'\.pytest_cache',
            r'\.venv',
            r'*.pyc',
            r'*.pyo'
        ]
        self.scan_history: List[ScanResult] = []

    async def scan_workspace(self, 
                           max_depth: Optional[int] = None,
                           file_types: Optional[List[str]] = None) -> ScanResult:
        """Scan workspace directory"""
        files = []
        total_size = 0
        file_types_count = {}
        
        try:
            for file_path in self._scan_files(max_depth, file_types):
                try:
                    stat = file_path.stat()
                    file_type = file_path.suffix.lower()[1:] if file_path.suffix else "unknown"
                    
                    # Update statistics
                    total_size += stat.st_size
                    file_types_count[file_type] = file_types_count.get(file_type, 0) + 1
                    
                    # Create file info
                    file_info = FileInfo(
                        path=file_path.relative_to(self.workspace),
                        size=stat.st_size,
                        created=datetime.fromtimestamp(stat.st_ctime),
                        modified=datetime.fromtimestamp(stat.st_mtime),
                        file_type=file_type,
                        content_type=self._get_content_type(file_path)
                    )
                    
                    files.append(file_info)
                    
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
                    
            result = ScanResult(
                timestamp=datetime.now(),
                files=files,
                total_size=total_size,
                file_types=file_types_count,
                metadata={
                    "workspace": str(self.workspace),
                    "max_depth": max_depth,
                    "file_types": file_types
                }
            )
            
            self.scan_history.append(result)
            return result
            
        except Exception as e:
            raise RuntimeError(f"Workspace scan failed: {str(e)}")

    def _scan_files(self, max_depth: Optional[int], file_types: Optional[List[str]]) -> List[Path]:
        """Generator for scanning files"""
        def should_ignore(path: Path) -> bool:
            return any(re.match(pattern, str(path)) for pattern in self.ignored_patterns)
            
        def scan_directory(path: Path, current_depth: int) -> List[Path]:
            if max_depth and current_depth > max_depth:
                return []
                
            files = []
            try:
                for item in path.iterdir():
                    if should_ignore(item):
                        continue
                        
                    if item.is_file():
                        if not file_types or (item.suffix and item.suffix[1:].lower() in file_types):
                            files.append(item)
                    elif item.is_dir():
                        files.extend(scan_directory(item, current_depth + 1))
            except Exception as e:
                print(f"Error scanning directory {path}: {str(e)}")
                
            return files
            
        return scan_directory(self.workspace, 0)

    def _get_content_type(self, file_path: Path) -> Optional[str]:
        """Determine content type of file"""
        content_types = {
            ".txt": "text/plain",
            ".py": "text/x-python",
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".xml": "application/xml",
            ".yaml": "application/x-yaml",
            ".yml": "application/x-yaml"
        }
        return content_types.get(file_path.suffix.lower())
```

---

# ..\..\src\file_services\__init__.py
## File: ..\..\src\file_services\__init__.py

```py
# ..\..\src\file_services\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\src\interfaces\cli_interface.py
## File: ..\..\src\interfaces\cli_interface.py

```py
# ..\..\src\interfaces\cli_interface.py
"""
src/interfaces/cli_interface.py

Command-Line Interface (CLI) for CodeMate – Din AI-drivna kodassistent

This module provides an interactive shell for the agent. In addition to basic commands
(like analyze, execute, status, config, history, clear, and exit), it includes extended
commands for:
  - Visualizing the active workflow.
  - Refreshing the LLM context.
  - Generating code from a prompt.
  - Simulating Git integration.
  - Running system diagnostics.
  - Dynamically updating configuration.
  - Reviewing audit logs and error history.
  - Debugging and reviewing internal state.

Each command is documented below.
"""

import asyncio
import cmd
import shlex
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Any, Union, Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from core.agent_coordinator import AgentCoordinator
from utils.logger import get_logger

@dataclass
class CommandContext:
    """Context for command execution."""
    command: str
    args: List[str]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class CLIInterface(cmd.Cmd):
    """
    Command-line interface for agent interaction.

    Available commands include:
      - analyze     : Analyze a file or directory.
      - execute     : Execute a workflow.
      - status      : Display current agent status.
      - config      : View current configuration.
      - update      : Update configuration dynamically.
      - visualize   : Visualize the active workflow.
      - refresh     : Refresh the LLM context.
      - generate    : Generate code from a given prompt.
      - git         : Simulate Git integration.
      - diagnostics : Run system diagnostics.
      - audit       : Show recent audit log entries.
      - error       : Show error history.
      - history     : Show CLI command history.
      - debug       : Display detailed system diagnostics and internal state.
      - clear       : Clear the screen.
      - exit        : Exit the CLI.
    """
    
    intro = "CodeMate – Din AI-drivna kodassistent CLI\nType 'help' for a list of available commands."
    prompt = "agent> "

    def __init__(self, agent: AgentCoordinator):
        super().__init__()
        self.agent = agent
        self.logger = get_logger(__name__)
        self.session = PromptSession()
        self.command_history: List[CommandContext] = []
        self._setup_completions()

    def _setup_completions(self) -> None:
        """Setup auto-completion with an extended list of commands."""
        self.completer = WordCompleter([
            'analyze', 'execute', 'status', 'config', 'update', 'visualize',
            'refresh', 'generate', 'git', 'diagnostics', 'audit', 'error',
            'history', 'debug', 'clear', 'exit', 'help'
        ])

    def _record_command(self, command: str, args: List[str]) -> None:
        """Record the executed command and its arguments."""
        self.command_history.append(CommandContext(
            command=command,
            args=args,
            timestamp=datetime.now()
        ))

    def do_analyze(self, arg: str) -> None:
        """Analyze workspace files or a specific file/directory.
        
        Usage: analyze <file_or_directory>
        """
        args = shlex.split(arg)
        self._record_command("analyze", args)
        if not args:
            print("Usage: analyze <file_or_directory>")
            return
        try:
            result = asyncio.run(
                self.agent.process_request({
                    "type": "analyze",
                    "data": {"path": args[0]}
                })
            )
            print("Analyze Request Result:")
            print(result)
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_execute(self, arg: str) -> None:
        """Execute a workflow.
        
        Usage: execute <workflow_id> [additional arguments...]
        """
        args = shlex.split(arg)
        self._record_command("execute", args)
        if not args:
            print("Usage: execute <workflow_id> [args...]")
            return
        try:
            result = asyncio.run(
                self.agent.process_request({
                    "type": "execute",
                    "data": {
                        "workflow": args[0],
                        "args": args[1:]
                    }
                })
            )
            print("Execute Request Result:")
            print(result)
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_status(self, arg: str) -> None:
        """Display the current agent status.
        
        Usage: status
        """
        self._record_command("status", [])
        try:
            status = asyncio.run(self.agent.check_status())
            print("\nAgent Status:")
            print(f"State: {status['state']}")
            print(f"Active Workflow: {status['active_workflow']}")
            print("\nMetrics:")
            for key, value in status['metrics'].items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_config(self, arg: str) -> None:
        """View the current configuration.
        
        Usage: config
        """
        self._record_command("config", [])
        try:
            print("\nCurrent Configuration:")
            config_dict = self.agent.config.__dict__
            for key, value in config_dict.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_update(self, arg: str) -> None:
        """Update the agent configuration dynamically.
        
        Usage: update <key> <value>
        Example: update debug_mode True
        """
        args = shlex.split(arg)
        self._record_command("update", args)
        if len(args) < 2:
            print("Usage: update <key> <value>")
            return
        key, value = args[0], args[1]
        try:
            if value.lower() in ["true", "false"]:
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)
            self.agent.update_configuration({key: value})
            print(f"Configuration updated: {key} set to {value}")
        except Exception as e:
            print(f"Error updating configuration: {str(e)}")

    def do_visualize(self, arg: str) -> None:
        """Visualize the current active workflow.
        
        Usage: visualize
        """
        self._record_command("visualize", [])
        try:
            visualization = self.agent.visualize_workflow()
            print("\nWorkflow Visualization:")
            print(visualization)
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_refresh(self, arg: str) -> None:
        """Refresh the LLM context from memory.
        
        Usage: refresh
        """
        self._record_command("refresh", [])
        try:
            asyncio.run(self.agent.refresh_llm_context())
            print("LLM context refreshed successfully.")
        except Exception as e:
            print(f"Error refreshing LLM context: {str(e)}")

    def do_generate(self, arg: str) -> None:
        """Generate code based on a prompt.
        
        Usage: generate <prompt>
        """
        args = shlex.split(arg)
        self._record_command("generate", args)
        if not args:
            print("Usage: generate <prompt>")
            return
        prompt_text = " ".join(args)
        try:
            generated_code = asyncio.run(self.agent.generate_code(prompt_text))
            print("\nGenerated Code:")
            print(generated_code)
        except Exception as e:
            print(f"Error generating code: {str(e)}")

    def do_git(self, arg: str) -> None:
        """Simulate Git integration: detect changes and commit them.
        
        Usage: git
        """
        self._record_command("git", [])
        try:
            result = asyncio.run(self.agent.integrate_with_git())
            print("\nGit Integration Result:")
            print(result)
        except Exception as e:
            print(f"Error during Git integration: {str(e)}")

    def do_diagnostics(self, arg: str) -> None:
        """Run system diagnostics and display results.
        
        Usage: diagnostics
        """
        self._record_command("diagnostics", [])
        try:
            diag = asyncio.run(self.agent.run_diagnostics())
            print("\nSystem Diagnostics:")
            for key, value in diag.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error running diagnostics: {str(e)}")

    def do_audit(self, arg: str) -> None:
        """Display the audit log (last 20 entries).
        
        Usage: audit
        """
        self._record_command("audit", [])
        try:
            print("\nAudit Log (most recent 20 entries):")
            for entry in self.agent.audit_log[-20:]:
                print(f"{entry.get('timestamp')} - Request ID: {entry.get('request_id')}, Data: {entry.get('request')}")
        except Exception as e:
            print(f"Error displaying audit log: {str(e)}")

    def do_error(self, arg: str) -> None:
        """Display error history from the error handler.
        
        Usage: error
        """
        self._record_command("error", [])
        try:
            history = self.agent.error_handler.get_error_history()
            print("\nError History (most recent 10 entries):")
            for report in history[-10:]:
                print(f"{report.context.timestamp.isoformat()} - {report.error_type}: {report.message}")
        except Exception as e:
            print(f"Error retrieving error history: {str(e)}")

    def do_history(self, arg: str) -> None:
        """Show command history.
        
        Usage: history
        """
        self._record_command("history", [])
        print("\nCommand History:")
        for ctx in self.command_history[-10:]:
            print(f"{ctx.timestamp.strftime('%H:%M:%S')} - {ctx.command} {' '.join(ctx.args)}")

    def do_debug(self, arg: str) -> None:
        """Display detailed system diagnostics and internal state.
        
        Usage: debug
        """
        self._record_command("debug", [])
        try:
            status = asyncio.run(self.agent.check_status())
            diag = asyncio.run(self.agent.run_diagnostics())
            print("\n[DEBUG] Agent Status:")
            print(f"State: {status['state']}")
            print(f"Active Workflow: {status['active_workflow']}")
            print("\n[DEBUG] Diagnostics:")
            for key, value in diag.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error running debug: {str(e)}")

    def do_clear(self, arg: str) -> None:
        """Clear the screen.
        
        Usage: clear
        """
        self._record_command("clear", [])
        print("\n" * 100)

    def do_exit(self, arg: str) -> bool:
        """Exit the CLI.
        
        Usage: exit
        """
        self._record_command("exit", [])
        print("\nExiting...")
        return True

    def do_help(self, arg: str) -> None:
        """Display help information for available commands."""
        cmds = [
            "analyze     : Analyze a file or directory",
            "execute     : Execute a workflow",
            "status      : Display agent status",
            "config      : View current configuration",
            "update      : Update configuration dynamically",
            "visualize   : Visualize the active workflow",
            "refresh     : Refresh LLM context",
            "generate    : Generate code from a prompt",
            "git         : Simulate Git integration",
            "diagnostics : Run system diagnostics",
            "audit       : Display audit log",
            "error       : Display error history",
            "history     : Show command history",
            "debug       : Display detailed diagnostics and internal state",
            "clear       : Clear the screen",
            "exit        : Exit the CLI"
        ]
        print("\nAvailable Commands:")
        for cmd_desc in cmds:
            print(cmd_desc)

```

---

# ..\..\src\interfaces\request_handler.py
## File: ..\..\src\interfaces\request_handler.py

```py
# ..\..\src\interfaces\request_handler.py
# src/interfaces/request_handler.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import json
from uuid import UUID, uuid4
from ..core.state_manager import StateManager
from ..core.workflow_manager import WorkflowManager
from ..utils.logger import get_logger

@dataclass
class RequestContext:
    """Context for request processing"""
    id: UUID
    request_type: str
    content: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0

@dataclass
class RequestResult:
    """Result of request processing"""
    success: bool
    data: Optional[Any]
    error: Optional[str]
    processing_time: float
    metadata: Dict[str, Any]

class RequestHandler:
    """Handles incoming requests and their processing"""
    
    def __init__(self, state_manager: StateManager, workflow_manager: WorkflowManager):
        self.state_manager = state_manager
        self.workflow_manager = workflow_manager
        self.logger = get_logger(__name__)
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.active_requests: Dict[UUID, RequestContext] = {}
        self._running = False

    async def start(self) -> None:
        """Start request processing"""
        self._running = True
        await self._process_queue()

    async def stop(self) -> None:
        """Stop request processing"""
        self._running = False

    async def handle_request(self, request_data: Dict[str, Any]) -> RequestResult:
        """Handle incoming request"""
        start_time = datetime.now()
        request_id = uuid4()
        
        try:
            # Validate request
            self._validate_request(request_data)
            
            # Create request context
            context = RequestContext(
                id=request_id,
                request_type=request_data.get("type", "unknown"),
                content=request_data,
                timestamp=datetime.now(),
                metadata=request_data.get("metadata", {}),
                priority=request_data.get("priority", 0)
            )
            
            # Add to active requests
            self.active_requests[request_id] = context
            
            # Process request
            result = await self._process_request(context)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return RequestResult(
                success=True,
                data=result,
                error=None,
                processing_time=processing_time,
                metadata={"request_id": str(request_id)}
            )
            
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return RequestResult(
                success=False,
                data=None,
                error=str(e),
                processing_time=processing_time,
                metadata={"request_id": str(request_id)}
            )
        finally:
            self.active_requests.pop(request_id, None)

    async def _process_queue(self) -> None:
        """Process requests from queue"""
        while self._running:
            try:
                request = await self.request_queue.get()
                await self.handle_request(request)
                self.request_queue.task_done()
            except Exception as e:
                self.logger.error(f"Error in queue processing: {str(e)}")
                await asyncio.sleep(1)

    async def _process_request(self, context: RequestContext) -> Any:
        """Process individual request"""
        # Update state
        self.state_manager.update_state("processing", {
            "request_id": str(context.id),
            "request_type": context.request_type
        })
        
        # Create workflow
        workflow = await self.workflow_manager.create_workflow({
            "type": context.request_type,
            "data": context.content,
            "metadata": context.metadata
        })
        
        # Execute workflow
        result = await self.workflow_manager.execute_workflow(workflow.id)
        
        # Update state
        self.state_manager.update_state("idle")
        
        return result

    def _validate_request(self, request_data: Dict[str, Any]) -> None:
        """Validate request data"""
        required_fields = ["type", "data"]
        for field in required_fields:
            if field not in request_data:
                raise ValueError(f"Missing required field: {field}")


```

---

# ..\..\src\interfaces\response_formatter.py
## File: ..\..\src\interfaces\response_formatter.py

```py
# ..\..\src\interfaces\response_formatter.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum
import re

class ResponseFormat(Enum):
    """Response format types"""
    TEXT = "text"
    JSON = "json"
    HTML = "html"
    MARKDOWN = "markdown"
    ERROR = "error"
    CONSOLE = "console"

@dataclass
class FormattingConfig:
    """Configuration for response formatting"""
    format_type: ResponseFormat
    indent_size: int = 2
    max_line_length: int = 80
    include_metadata: bool = True
    highlight_syntax: bool = True
    wrap_text: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

class ResponseFormatter:
    """Formats response content for output"""
    
    def __init__(self, config: Optional[FormattingConfig] = None):
        self.config = config or FormattingConfig(ResponseFormat.TEXT)
        self.formatters = {
            ResponseFormat.TEXT: self._format_text,
            ResponseFormat.JSON: self._format_json,
            ResponseFormat.HTML: self._format_html,
            ResponseFormat.MARKDOWN: self._format_markdown,
            ResponseFormat.ERROR: self._format_error,
            ResponseFormat.CONSOLE: self._format_console
        }
    
    def format_response(self, content: Any, format_type: Optional[ResponseFormat] = None) -> str:
        """Format response content"""
        format_type = format_type or self.config.format_type
        formatter = self.formatters.get(format_type)
        if not formatter:
            raise ValueError(f"Unsupported format type: {format_type}")
        try:
            formatted = formatter(content)
            if self.config.include_metadata:
                formatted = self._add_metadata(formatted, format_type)
            return formatted
        except Exception as e:
            return self._format_error(e)

    def _format_text(self, content: Any) -> str:
        """Format text content"""
        if not isinstance(content, str):
            content = str(content)
        if self.config.wrap_text and self.config.max_line_length > 0:
            lines = []
            for line in content.split('\n'):
                if len(line) > self.config.max_line_length:
                    words = line.split()
                    current_line = []
                    current_length = 0
                    for word in words:
                        word_length = len(word)
                        # Add a space only if there is already content in current_line.
                        additional = 1 if current_line else 0
                        if current_length + word_length + additional <= self.config.max_line_length:
                            current_line.append(word)
                            current_length += word_length + additional
                        else:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                            current_length = word_length
                    if current_line:
                        lines.append(' '.join(current_line))
                else:
                    lines.append(line)
            content = '\n'.join(lines)
        return content

    def _format_json(self, content: Any) -> str:
        """Format JSON content"""
        try:
            if isinstance(content, str):
                content = json.loads(content)
            return json.dumps(content, indent=self.config.indent_size, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Invalid JSON content: {str(e)}")

    def _format_html(self, content: Any) -> str:
        """Format HTML content"""
        if not isinstance(content, str):
            content = str(content)
        indent = 0
        lines = []
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('</'):
                indent = max(0, indent - 1)
            lines.append(' ' * (indent * self.config.indent_size) + stripped)
            if (stripped.endswith('>') and not stripped.startswith('</') and
                not stripped.endswith('/>') and not stripped.startswith('<!--')):
                indent += 1
        return '\n'.join(lines)

    def _format_markdown(self, content: Any) -> str:
        """Format Markdown content"""
        if not isinstance(content, str):
            content = str(content)
        # Format headers
        content = re.sub(r'^(#+)\s*', r'\1 ', content, flags=re.MULTILINE)
        # Format lists
        content = re.sub(r'^\s*[-*+]\s*', '- ', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*(\d+\.)\s*', r'\1 ', content, flags=re.MULTILINE)
        # Format code blocks
        content = re.sub(r'^```(\w*)\s*$', r'```\1', content, flags=re.MULTILINE)
        return content

    def _format_error(self, content: Any) -> str:
        """Format error content"""
        if isinstance(content, Exception):
            error_msg = f"Error: {str(content)}"
            if hasattr(content, '__traceback__'):
                error_msg += f"\nTraceback:\n{content.__traceback__}"
            return error_msg
        return f"Error: {str(content)}"

    def _format_console(self, content: Any) -> str:
        """Format console output"""
        if isinstance(content, (list, tuple)):
            return '\n'.join(str(item) for item in content)
        return str(content)

    def _add_metadata(self, content: str, format_type: ResponseFormat) -> str:
        """Add metadata to formatted content"""
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "format": format_type.value,
            **self.config.metadata
        }
        if format_type == ResponseFormat.JSON:
            return json.dumps({"content": content, "metadata": metadata}, indent=self.config.indent_size)
        elif format_type == ResponseFormat.MARKDOWN:
            meta_section = "---\n"
            for key, value in metadata.items():
                meta_section += f"{key}: {value}\n"
            meta_section += "---\n\n"
            return meta_section + content
        else:
            meta_section = "# Metadata\n"
            for key, value in metadata.items():
                meta_section += f"# {key}: {value}\n"
            return f"{meta_section}\n{content}"

```

---

# ..\..\src\interfaces\terminal_manager.py
## File: ..\..\src\interfaces\terminal_manager.py

```py
# ..\..\src\interfaces\terminal_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from pathlib import Path
import shlex
import os

@dataclass
class CommandResult:
    """Result of command execution"""
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration: float
    timestamp: datetime
    pid: Optional[int] = None

@dataclass
class TerminalSession:
    """Terminal session information"""
    id: str
    workspace: Path
    environment: Dict[str, str]
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_command: Optional[str] = None
    last_result: Optional[CommandResult] = None

class TerminalManager:
    """
    Manages terminal sessions and command execution.
    Supports both session-based commands and global commands.
    """
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        # Session-based management
        self.sessions: Dict[str, TerminalSession] = {}
        self.session_command_history: Dict[str, List[CommandResult]] = {}
        # Global command history and active processes
        self.global_command_history: List[CommandResult] = []
        self.max_history = 1000
        self.active_processes: Dict[str, asyncio.subprocess.Process] = {}
        self._setup_environment()

    def _setup_environment(self) -> None:
        """Setup default environment variables"""
        self.default_env = {
            "PYTHONPATH": str(self.workspace),
            "WORKSPACE": str(self.workspace),
            "TERM": "xterm-256color",
            **os.environ.copy()
        }

    # ----- Session management methods -----
    async def create_session(self, session_id: str, environment: Optional[Dict[str, str]] = None) -> TerminalSession:
        """Create a new terminal session"""
        if session_id in self.sessions:
            raise ValueError(f"Session already exists: {session_id}")
        session = TerminalSession(
            id=session_id,
            workspace=self.workspace,
            environment={**self.default_env, **(environment or {})}
        )
        self.sessions[session_id] = session
        self.session_command_history[session_id] = []
        return session

    def get_session(self, session_id: str) -> Optional[TerminalSession]:
        """Get session information"""
        return self.sessions.get(session_id)

    def get_active_sessions(self) -> List[TerminalSession]:
        """Get all active sessions"""
        return [s for s in self.sessions.values() if s.active]

    async def close_session(self, session_id: str) -> None:
        """Close a terminal session"""
        session = self.sessions.get(session_id)
        if session:
            session.active = False
            await self.terminate_command(session_id=session_id)
            self.sessions.pop(session_id)
            self.session_command_history.pop(session_id, None)
            self.active_processes.pop(session_id, None)

    def get_session_command_history(self, session_id: str, limit: Optional[int] = None) -> List[CommandResult]:
        """Get command history for a session"""
        history = self.session_command_history.get(session_id, [])
        return history[-limit:] if limit else history

    # ----- Global command execution methods -----
    async def execute_command(
        self,
        command: Union[str, List[str]],
        timeout: Optional[int] = None,
        capture_output: bool = True,
        session_id: Optional[str] = None
    ) -> CommandResult:
        """
        Execute a command.
        If session_id is provided, uses that session’s environment and records history there.
        Otherwise, uses the global workspace.
        """
        start_time = datetime.now()
        if isinstance(command, str):
            command_list = shlex.split(command)
        else:
            command_list = command

        # Determine environment and working directory based on session (if any)
        env = self.default_env.copy()
        cwd = str(self.workspace)
        if session_id:
            session = self.sessions.get(session_id)
            if not session:
                raise ValueError(f"Session not found: {session_id}")
            if not session.active:
                raise ValueError(f"Session is not active: {session_id}")
            env = session.environment
            cwd = str(session.workspace)
            proc_key = session_id  # One active command per session
        else:
            proc_key = f"{command_list[0]}_{start_time.timestamp()}"

        try:
            process = await asyncio.create_subprocess_exec(
                *command_list,
                stdout=asyncio.subprocess.PIPE if capture_output else None,
                stderr=asyncio.subprocess.PIPE if capture_output else None,
                env=env,
                cwd=cwd
            )
            self.active_processes[proc_key] = process
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                duration = (datetime.now() - start_time).total_seconds()
                result = CommandResult(
                    command=' '.join(command_list),
                    exit_code=process.returncode,
                    stdout=stdout.decode() if stdout else "",
                    stderr=stderr.decode() if stderr else "",
                    duration=duration,
                    timestamp=start_time,
                    pid=process.pid
                )
                if session_id:
                    session.last_command = ' '.join(command_list)
                    session.last_result = result
                    self.session_command_history[session_id].append(result)
                else:
                    self._add_to_global_history(result)
                return result
            except asyncio.TimeoutError:
                process.terminate()
                raise TimeoutError(f"Command timed out after {timeout} seconds")
            finally:
                self.active_processes.pop(proc_key, None)
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            result = CommandResult(
                command=' '.join(command_list),
                exit_code=-1,
                stdout="",
                stderr=str(e),
                duration=duration,
                timestamp=start_time
            )
            if session_id:
                session.last_command = ' '.join(command_list)
                session.last_result = result
                self.session_command_history[session_id].append(result)
            else:
                self._add_to_global_history(result)
            return result

    async def execute_python_script(
        self,
        script_path: Union[str, Path],
        args: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> CommandResult:
        """Execute a Python script"""
        script_path = Path(script_path)
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        command = ["python", str(script_path)]
        if args:
            command.extend(args)
        return await self.execute_command(command, timeout=timeout, session_id=session_id)

    def _add_to_global_history(self, result: CommandResult) -> None:
        """Add a command result to the global history and enforce max history size"""
        self.global_command_history.append(result)
        if len(self.global_command_history) > self.max_history:
            self.global_command_history.pop(0)

    def get_global_command_history(
        self, limit: Optional[int] = None, filter_success: Optional[bool] = None
    ) -> List[CommandResult]:
        """Get global command history, optionally filtering by success"""
        history = self.global_command_history
        if filter_success is not None:
            history = [cmd for cmd in history if (cmd.exit_code == 0) == filter_success]
        return history[-limit:] if limit else history

    def clear_global_history(self) -> None:
        """Clear the global command history"""
        self.global_command_history.clear()

    async def get_active_processes(self) -> Dict[str, Dict[str, Any]]:
        """Get information about currently running processes"""
        info = {}
        for key, process in self.active_processes.items():
            info[key] = {
                "command": key if "_" in key else f"session: {key}",
                "pid": process.pid if process.pid else None
                # Additional details (like start time) can be added if tracked.
            }
        return info

    async def terminate_command(self, command_key: Optional[str] = None, session_id: Optional[str] = None) -> bool:
        """
        Terminate a running command.
        If session_id is provided, that session’s running process is terminated.
        Otherwise, use command_key (as generated for global commands).
        """
        key = session_id if session_id else command_key
        process = self.active_processes.get(key)
        if process:
            process.terminate()
            self.active_processes.pop(key, None)
            return True
        return False

    def terminate_all(self) -> None:
        """Terminate all running commands"""
        for process in self.active_processes.values():
            process.terminate()
        self.active_processes.clear()

    def set_workspace(self, path: Union[str, Path]) -> None:
        """Set a new workspace path"""
        self.workspace = Path(path)
        if not self.workspace.exists():
            raise FileNotFoundError(f"Workspace path does not exist: {path}")
        self._setup_environment()

    async def check_command_exists(self, command: str) -> bool:
        """Check if a command exists in the system"""
        try:
            result = await self.execute_command(f"which {command}", capture_output=True)
            return result.exit_code == 0
        except Exception:
            return False

```

---

# ..\..\src\interfaces\__init__.py
## File: ..\..\src\interfaces\__init__.py

```py
# ..\..\src\interfaces\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\src\llm\conversation.py
## File: ..\..\src\llm\conversation.py

```py
# ..\..\src\llm\conversation.py
"""
conversation.py

Detta modul hanterar konversationer med agenten. Här lagras
historik och meddelanden skickas till LLM via llm_manager.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import asyncio
from uuid import uuid4

from .llm_manager import llm_manager, ModelResponse

class ConversationMessage:
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.id = str(uuid4())
        self.role = role  # ex. "user" eller "assistant"
        self.content = content
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

class ConversationManager:
    def __init__(self):
        self.history: List[ConversationMessage] = []
        self.max_history = 50  # max antal meddelanden att spara

    def add_message(self, role: str, content: str) -> None:
        message = ConversationMessage(role, content)
        self.history.append(message)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_history(self) -> List[Dict[str, Any]]:
        return [msg.to_dict() for msg in self.history]

    async def send_message(self, user_message: str, model_name: Optional[str] = None) -> ModelResponse:
        self.add_message("user", user_message)
        # Skicka med hela konversationshistoriken som kontext
        messages = [{"role": msg.role, "content": msg.content} for msg in self.history]
        response: ModelResponse = await llm_manager.generate_response(messages, model_name=model_name)
        self.add_message("assistant", response.content)
        return response

# Skapa en singleton-instans om så önskas
conversation_manager = ConversationManager()

```

---

# ..\..\src\llm\llm_agent.py
## File: ..\..\src\llm\llm_agent.py

```py
# ..\..\src\llm\llm_agent.py
"""
llm_agent.py

Detta är det centrala gränssnittet för LLM-integrationen. Här binder vi ihop:
- Konversation (med historik)
- Promptoptimering
- Modellval baserat på agentens state
- Svarsparsning

Genom metoden ask() kan du ange ett användarmeddelande samt (valfritt) ett agent_state.
Om inget state anges används default state (IDLE) och då väljer model_selector standardmodellen.
"""

from typing import Dict, Any, Optional
import asyncio

from core.state_manager import AgentState
from .conversation import conversation_manager
from .prompt_optimizer import prompt_optimizer
from .model_selector import model_selector
from .response_parser import response_parser
from .llm_manager import llm_manager

class LLMAgent:
    def __init__(self):
        self.conversation = conversation_manager
        self.optimizer = prompt_optimizer
        self.selector = model_selector
        self.parser = response_parser
        self.llm = llm_manager

    async def ask(self, user_input: str, agent_state: Optional[AgentState] = None) -> Dict[str, Any]:
        # Optimera prompten
        optimized_prompt = self.optimizer.optimize(user_input)
        # Om inget state specificeras, använd IDLE som default
        if agent_state is None:
            agent_state = AgentState.IDLE
        # Välj modell baserat på det angivna agent_state
        selected_model = self.selector.select_model(agent_state)
        # Skicka meddelande via konversationen – hela historiken skickas som kontext
        response = await self.conversation.send_message(optimized_prompt, model_name=selected_model)
        # Parsar svaret och returnerar det som en dictionary
        parsed_response = self.parser.parse(response)
        return parsed_response

    def get_conversation_history(self) -> Any:
        return self.conversation.get_history()

# Skapa en singleton-instans
llm_agent = LLMAgent()

```

---

# ..\..\src\llm\llm_manager.py
## File: ..\..\src\llm\llm_manager.py

```py
# ..\..\src\llm\llm_manager.py
"""
llm_manager.py

Detta modul hanterar integrationen med olika LLM‐providers.
Den definierar en ModelProvider‐enum, ModelConfig och ModelResponse,
samt en LLMManager-klass som initialiserar klienter baserat på miljövariabler.
"""

from typing import Optional, Dict, Any, Union
from enum import Enum
import os
from datetime import datetime
from dotenv import load_dotenv

from anthropic import Anthropic
from openai import OpenAI, AzureOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

# Ladda miljövariabler
load_dotenv()

class ModelProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    AZURE = "azure"
    GROQ = "groq"
    LM_STUDIO = "lm_studio"

class ModelConfig(BaseModel):
    provider: ModelProvider
    model_name: str
    temperature: float = Field(default=float(os.getenv("TEMPERATURE", "0.7")))
    max_tokens: int = Field(default=int(os.getenv("MAX_TOKENS", "60000")))
    top_p: float = Field(default=float(os.getenv("TOP_P", "0.9")))
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    additional_params: Dict[str, Any] = Field(default_factory=dict)

class ModelResponse(BaseModel):
    content: str
    model_name: str
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)

class LLMManager:
    def __init__(self):
        self.models = self._load_default_models()
        self.current_model = os.getenv("DEFAULT_MODEL", "claude-3-sonnet")
        self._load_api_keys()
        self._initialize_clients()

    def _load_default_models(self) -> Dict[str, ModelConfig]:
        return {
            "claude-3-haiku": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=os.getenv("CLAUDE_HAIKU_MODEL", "claude-3-haiku-20240307")
            ),
            "claude-3-sonnet": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=os.getenv("CLAUDE_SONNET_MODEL", "claude-3-sonnet-20240229")
            ),
            "claude-3-opus": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=os.getenv("CLAUDE_OPUS_MODEL", "claude-3-opus-20240229")
            ),
            "gpt-4": ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name=os.getenv("GPT4_MODEL", "gpt-4")
            ),
            "gpt-3.5-turbo": ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name=os.getenv("GPT35_MODEL", "gpt-3.5-turbo")
            ),
            "mixtral-8x7b": ModelConfig(
                provider=ModelProvider.GROQ,
                model_name=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
            ),
            "lm-studio-local": ModelConfig(
                provider=ModelProvider.LM_STUDIO,
                model_name=os.getenv("LM_STUDIO_MODEL", "model-identifier"),
                api_base=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
            )
        }

    def _load_api_keys(self):
        self.api_keys = {
            ModelProvider.ANTHROPIC: os.getenv("ANTHROPIC_API_KEY"),
            ModelProvider.OPENAI: os.getenv("OPENAI_API_KEY"),
            ModelProvider.GROQ: os.getenv("GROQ_API_KEY"),
            ModelProvider.AZURE: os.getenv("AZURE_OPENAI_API_KEY"),
            ModelProvider.LM_STUDIO: os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        }

    def _initialize_clients(self):
        self.clients = {}
        if self.api_keys.get(ModelProvider.ANTHROPIC):
            self.clients[ModelProvider.ANTHROPIC] = Anthropic(
                api_key=self.api_keys[ModelProvider.ANTHROPIC]
            )
        if self.api_keys.get(ModelProvider.OPENAI):
            self.clients[ModelProvider.OPENAI] = OpenAI(
                api_key=self.api_keys[ModelProvider.OPENAI]
            )
        if self.api_keys.get(ModelProvider.GROQ):
            self.clients[ModelProvider.GROQ] = ChatGroq(
                api_key=self.api_keys[ModelProvider.GROQ]
            )
        # För LM Studio antas klienten likna OpenAI-klienten
        self.clients[ModelProvider.LM_STUDIO] = OpenAI(
            base_url=self.models["lm-studio-local"].api_base,
            api_key=self.api_keys[ModelProvider.LM_STUDIO]
        )

    def add_model(self, name: str, config: ModelConfig):
        self.models[name] = config

    def set_current_model(self, model_name: str):
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found in available models")
        self.current_model = model_name

    def get_available_models(self) -> Dict[str, ModelConfig]:
        return self.models

    async def generate_response(
        self,
        messages: list,
        model_name: Optional[str] = None,
        **kwargs
    ) -> ModelResponse:
        start_time = datetime.now()
        model_name = model_name or self.current_model
        model_config = self.models[model_name]
        try:
            if model_config.provider == ModelProvider.ANTHROPIC:
                response = await self._generate_anthropic_response(messages, model_config, **kwargs)
            elif model_config.provider == ModelProvider.OPENAI:
                response = await self._generate_openai_response(messages, model_config, **kwargs)
            elif model_config.provider == ModelProvider.GROQ:
                response = await self._generate_groq_response(messages, model_config, **kwargs)
            elif model_config.provider == ModelProvider.LM_STUDIO:
                response = await self._generate_lm_studio_response(messages, model_config, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {model_config.provider}")

            processing_time = (datetime.now() - start_time).total_seconds()
            return ModelResponse(
                content=response.content,
                model_name=model_name,
                total_tokens=response.usage.total_tokens,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                processing_time=processing_time
            )
        except Exception as e:
            raise Exception(f"Error generating response with {model_name}: {str(e)}")

    async def _generate_anthropic_response(self, messages, model_config: ModelConfig, **kwargs):
        client = self.clients[ModelProvider.ANTHROPIC]
        return await client.messages.create(
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

    async def _generate_openai_response(self, messages, model_config: ModelConfig, **kwargs):
        client = self.clients[ModelProvider.OPENAI]
        return await client.chat.completions.create(
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

    async def _generate_groq_response(self, messages, model_config: ModelConfig, **kwargs):
        client = self.clients[ModelProvider.GROQ]
        return await client.create(
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

    async def _generate_lm_studio_response(self, messages, model_config: ModelConfig, **kwargs):
        client = self.clients[ModelProvider.LM_STUDIO]
        return await client.chat.completions.create(
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

# Skapa en singleton-instans för enkel åtkomst
llm_manager = LLMManager()

```

---

# ..\..\src\llm\model_selector.py
## File: ..\..\src\llm\model_selector.py

```py
# ..\..\src\llm\model_selector.py
"""
model_selector.py

Detta modul väljer rätt LM Studio-modell baserat på agentens state.
Alla modeller kommer från LM Studio.
"""

from typing import Optional, Dict, Any
from core.state_manager import AgentState

class ModelSelector:
    def __init__(self):
        # Mappning från specifika AgentState till modellnamn
        self.state_model_mapping = {
            AgentState.CODING: "rewnozom/nodex_l-8b/nodex_l-8b-q4_k_m.gguf",
            AgentState.WRITING_TESTS: "llama-3.2-3b-codereactor",
            AgentState.NAVIGATION: "nodex_l-8b@q8_0",
            AgentState.EMBEDDING: "text-embedding-nomic-embed-text-v1.5@q4_k_m"
        }
        # Om inget state matchar, använd denna standardmodell
        self.default_model = "lm-studio-local"

    def select_model(self, agent_state: AgentState) -> str:
        return self.state_model_mapping.get(agent_state, self.default_model)

# Skapa en singleton-instans
model_selector = ModelSelector()

```

---

# ..\..\src\llm\prompt_optimizer.py
## File: ..\..\src\llm\prompt_optimizer.py

```py
# ..\..\src\llm\prompt_optimizer.py
"""
prompt_optimizer.py

En enkel promptoptimizer som exempelvis kan trimma prompts om de blir för långa.
Här kan du lägga till mer avancerad logik vid behov.
"""

from typing import Dict, Any

class PromptOptimizer:
    def __init__(self, max_tokens: int = 60000):
        self.max_tokens = max_tokens

    def optimize(self, prompt: str) -> str:
        # Enkel uppskattning: 4 tecken per token
        token_estimate = len(prompt) // 4
        if token_estimate > self.max_tokens:
            # Trunkera prompten så att den ryms inom max_tokens
            prompt = prompt[: self.max_tokens * 4]
        return prompt

# Skapa en singleton-instans
prompt_optimizer = PromptOptimizer()

```

---

# ..\..\src\llm\response_parser.py
## File: ..\..\src\llm\response_parser.py

```py
# ..\..\src\llm\response_parser.py
"""
response_parser.py

Modul för att parsa och standardisera svar från LLM.
"""

from typing import Dict, Any
from .llm_manager import ModelResponse

class ResponseParser:
    def parse(self, response: ModelResponse) -> Dict[str, Any]:
        # Konvertera ModelResponse till en dictionary och försök
        # parsa innehållet (t.ex. om det är JSON)
        parsed = response.dict()
        content = parsed.get("content", "")
        try:
            import json
            parsed_json = json.loads(content)
            parsed["parsed_content"] = parsed_json
        except Exception:
            parsed["parsed_content"] = content
        return parsed

# Skapa en singleton-instans
response_parser = ResponseParser()

```

---

# ..\..\src\storage\cache_manager.py
## File: ..\..\src\storage\cache_manager.py

```py
# ..\..\src\storage\cache_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from pathlib import Path
import pickle

@dataclass
class CacheItem:
    """Individual cache item"""
    key: str
    data: Any
    created_at: datetime
    expires_at: Optional[datetime]
    metadata: Dict[str, Any] = field(default_factory=dict)
    access_count: int = 0

class CacheManager:
    """
    Manages temporary data caching.
    
    If a cache directory is provided, items are stored persistently using pickle.
    """
    
    def __init__(self, cache_dir: Optional[str] = None, max_size: int = 1000, default_ttl: Optional[int] = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path("temp/cache")
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheItem] = {}
        self.persistent: bool = cache_dir is not None
        self._initialize_cache()

    def _initialize_cache(self) -> None:
        """Initialize the cache system and load persistent items if needed"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if self.persistent:
            self._load_persistent_cache()

    def _load_persistent_cache(self) -> None:
        """Load persistent cache items from disk"""
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                with open(cache_file, 'rb') as f:
                    item = pickle.load(f)
                    if not self._is_expired(item):
                        self.cache[item.key] = item
            except Exception as e:
                print(f"Error loading cache item {cache_file}: {str(e)}")

    def _is_expired(self, item: CacheItem) -> bool:
        """Check if a cache item is expired"""
        return item.expires_at is not None and datetime.now() > item.expires_at

    def get(self, key: str, default: Any = None) -> Any:
        """Get an item from the cache"""
        item = self.cache.get(key)
        if not item:
            return default
        if self._is_expired(item):
            self.delete(key)
            return default
        item.access_count += 1
        if self.persistent:
            self._save_item(item)
        return item.data

    def set(self, key: str, data: Any, ttl: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Set a cache item"""
        if len(self.cache) >= self.max_size:
            self._cleanup()
        ttl_value = ttl if ttl is not None else self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl_value) if ttl_value else None
        item = CacheItem(
            key=key,
            data=data,
            created_at=datetime.now(),
            expires_at=expires_at,
            metadata=metadata or {}
        )
        self.cache[key] = item
        if self.persistent:
            self._save_item(item)

    def delete(self, key: str) -> bool:
        """Delete a cache item"""
        if key in self.cache:
            del self.cache[key]
            cache_file = self.cache_dir / f"{key}.cache"
            if cache_file.exists():
                cache_file.unlink()
            return True
        return False

    def clear(self) -> None:
        """Clear all cache items"""
        self.cache.clear()
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()

    def _cleanup(self) -> None:
        """Clean up expired and least-used items"""
        # Remove expired items first
        expired_keys = [key for key, item in self.cache.items() if self._is_expired(item)]
        for key in expired_keys:
            self.delete(key)
        # If still over limit, remove least-accessed items
        while len(self.cache) >= self.max_size:
            sorted_items = sorted(self.cache.items(), key=lambda x: (x[1].access_count, -x[1].created_at.timestamp()))
            if not sorted_items:
                break
            key_to_remove, _ = sorted_items[0]
            self.delete(key_to_remove)

    def _save_item(self, item: CacheItem) -> None:
        """Save a cache item to disk"""
        try:
            cache_file = self.cache_dir / f"{item.key}.cache"
            with open(cache_file, 'wb') as f:
                pickle.dump(item, f)
        except Exception as e:
            print(f"Error saving cache item {item.key}: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache"""
        total_items = len(self.cache)
        expired_items = len([item for item in self.cache.values() if self._is_expired(item)])
        total_access = sum(item.access_count for item in self.cache.values())
        average_access = total_access / total_items if total_items else 0
        memory_usage = sum(len(pickle.dumps(item)) for item in self.cache.values())
        hits_by_key = {key: item.access_count for key, item in self.cache.items()}
        return {
            "total_items": total_items,
            "expired_items": expired_items,
            "total_access_count": total_access,
            "average_access_count": average_access,
            "cached_keys": list(self.cache.keys()),
            "memory_usage": memory_usage,
            "hits_by_key": hits_by_key,
            "persistent": self.persistent,
            "cache_usage_percent": (total_items / self.max_size) * 100
        }

    def touch(self, key: str) -> bool:
        """Update the access time (via access count) for a cache item"""
        if key in self.cache:
            item = self.cache[key]
            item.access_count += 1
            if self.persistent:
                self._save_item(item)
            return True
        return False

    def get_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a cache item"""
        item = self.cache.get(key)
        return item.metadata if item else None

    def update_metadata(self, key: str, metadata: Dict[str, Any]) -> bool:
        """Update metadata for a cache item"""
        if key in self.cache:
            item = self.cache[key]
            item.metadata.update(metadata)
            if self.persistent:
                self._save_item(item)
            return True
        return False

    def get_expired_items(self) -> List[str]:
        """Get a list of keys that are expired"""
        return [key for key, item in self.cache.items() if self._is_expired(item)]

    def cleanup_expired(self) -> int:
        """Clean up expired items and return the count removed"""
        expired = self.get_expired_items()
        for key in expired:
            self.delete(key)
        return len(expired)

    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache"""
        return key in self.cache

    def set_many(self, items: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """Set multiple cache items at once"""
        for key, data in items.items():
            self.set(key, data, ttl)

    def get_many(self, keys: List[str], default: Any = None) -> Dict[str, Any]:
        """Get multiple cache items at once"""
        return {key: self.get(key, default) for key in keys}

```

---

# ..\..\src\storage\persistence_manager.py
## File: ..\..\src\storage\persistence_manager.py

```py
# ..\..\src\storage\persistence_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
import pickle
from pathlib import Path
import shutil
import zlib
from uuid import UUID, uuid4

@dataclass
class StorageConfig:
    """
    Configuration for persistent storage.
    For this merged version the default format is 'pickle'.
    """
    storage_path: Path
    format: str = "pickle"  # Currently only 'pickle' is supported.
    compression: bool = False
    backup_enabled: bool = True
    max_backups: int = 5

@dataclass
class StorageItem:
    """Individual storage item"""
    id: UUID
    key: str
    data: Any
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    compressed: bool = False

class PersistenceManager:
    """Manages persistent data storage with optional compression and backup"""
    
    def __init__(self, config: Optional[StorageConfig] = None, storage_path: Optional[str] = None, compression: bool = False):
        if config:
            self.config = config
        else:
            path = Path(storage_path) if storage_path else Path("storage")
            self.config = StorageConfig(storage_path=path, compression=compression)
        self.storage_path = self.config.storage_path
        self.compression = self.config.compression
        self.items: Dict[UUID, StorageItem] = {}
        self.indices: Dict[str, UUID] = {}
        self._initialize_storage()
        
    def _initialize_storage(self) -> None:
        """Initialize the storage system and load existing data"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._load_existing_data()
        
    def _load_existing_data(self) -> None:
        """Load existing data and indices from storage"""
        index_file = self.storage_path / "index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r') as f:
                    index_data = json.load(f)
                    self.indices = {k: UUID(v) for k, v in index_data.items()}
            except Exception as e:
                print(f"Error loading index file: {str(e)}")
        for item_file in self.storage_path.glob("item_*.dat"):
            try:
                with open(item_file, 'rb') as f:
                    item = pickle.load(f)
                    if isinstance(item, StorageItem):
                        self.items[item.id] = item
            except Exception as e:
                print(f"Error loading item {item_file}: {str(e)}")
                
    async def store(self, key: str, data: Any, metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """
        Store data persistently under the given key.
        If the key already exists, the data is updated.
        """
        if key in self.indices:
            return await self.update(key, data, metadata)
        item_id = uuid4()
        now = datetime.now()
        stored_data = self._compress_data(data) if self.compression else data
        item = StorageItem(
            id=item_id,
            key=key,
            data=stored_data,
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
            compressed=self.compression
        )
        self.items[item_id] = item
        self.indices[key] = item_id
        await self._save_item(item)
        await self._save_index()
        if self.config.backup_enabled:
            self.create_backup()
        return item_id

    async def retrieve(self, key: str) -> Any:
        """Retrieve stored data by key"""
        item_id = self.indices.get(key)
        if not item_id:
            raise KeyError(f"Key not found: {key}")
        item = self.items[item_id]
        return self._decompress_data(item.data) if item.compressed else item.data

    async def update(self, key: str, data: Any, metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Update stored data for the given key"""
        item_id = self.indices.get(key)
        if not item_id:
            raise KeyError(f"Key not found: {key}")
        item = self.items[item_id]
        item.data = self._compress_data(data) if self.compression else data
        item.updated_at = datetime.now()
        if metadata:
            item.metadata.update(metadata)
        await self._save_item(item)
        return item_id

    async def delete(self, key: str) -> None:
        """Delete stored data by key"""
        item_id = self.indices.pop(key, None)
        if item_id:
            self.items.pop(item_id, None)
            item_file = self.storage_path / f"item_{item_id}.dat"
            if item_file.exists():
                item_file.unlink()
            await self._save_index()

    def _compress_data(self, data: Any) -> bytes:
        """Compress data using pickle and zlib"""
        pickled = pickle.dumps(data)
        return zlib.compress(pickled)

    def _decompress_data(self, data: bytes) -> Any:
        """Decompress data"""
        try:
            decompressed = zlib.decompress(data)
            return pickle.loads(decompressed)
        except Exception as e:
            print(f"Decompression error: {str(e)}")
            return data

    async def _save_item(self, item: StorageItem) -> None:
        """Save a storage item to disk"""
        item_file = self.storage_path / f"item_{item.id}.dat"
        try:
            with open(item_file, 'wb') as f:
                pickle.dump(item, f)
        except Exception as e:
            print(f"Error saving item {item.id}: {str(e)}")

    async def _save_index(self) -> None:
        """Save the index mapping to disk"""
        index_file = self.storage_path / "index.json"
        try:
            with open(index_file, 'w') as f:
                json.dump({k: str(v) for k, v in self.indices.items()}, f)
        except Exception as e:
            print(f"Error saving index: {str(e)}")

    def create_backup(self) -> Path:
        """Create a backup of the storage directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.storage_path.parent / f"storage_backup_{timestamp}"
        try:
            shutil.copytree(self.storage_path, backup_path)
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
        # Remove old backups if necessary
        backups = sorted(self.storage_path.parent.glob("storage_backup_*"))
        while len(backups) > self.config.max_backups:
            old_backup = backups.pop(0)
            shutil.rmtree(old_backup)
        return backup_path

    def restore_backup(self, backup_path: Union[str, Path]) -> None:
        """Restore storage from a backup"""
        backup_path = Path(backup_path)
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")
        # Clear current storage and copy backup
        if self.storage_path.exists():
            shutil.rmtree(self.storage_path)
        shutil.copytree(backup_path, self.storage_path)
        # Reload data into memory
        self.items.clear()
        self.indices.clear()
        self._load_existing_data()

class StorageError(Exception):
    """Custom exception for storage-related errors"""
    pass

```

---

# ..\..\src\storage\__init__.py
## File: ..\..\src\storage\__init__.py

```py
# ..\..\src\storage\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\src\task_management\checklist_manager.py
## File: ..\..\src\task_management\checklist_manager.py

```py
# ..\..\src\task_management\checklist_manager.py
# src/task_management/checklist_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

class ChecklistItemStatus(Enum):
    """Status for checklist items"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    FAILED = "failed"

@dataclass
class ChecklistItem:
    """Individual checklist item"""
    id: UUID
    title: str
    description: str
    status: ChecklistItemStatus
    priority: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    dependencies: List[UUID] = field(default_factory=list)
    subtasks: List['ChecklistItem'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Checklist:
    """Complete checklist"""
    id: UUID
    name: str
    description: str
    items: List[ChecklistItem]
    created_at: datetime
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class ChecklistManager:
    """Manages task checklists"""
    
    def __init__(self):
        self.checklists: Dict[UUID, Checklist] = {}
        self.active_checklist: Optional[UUID] = None
        self.templates: Dict[str, Checklist] = {}

    def create_checklist(self,
                       name: str,
                       description: str,
                       items: Optional[List[Dict[str, Any]]] = None,
                       template: Optional[str] = None) -> UUID:
        """Create new checklist"""
        checklist_id = uuid4()
        
        if template and template in self.templates:
            # Clone template
            template_list = self.templates[template]
            checklist = Checklist(
                id=checklist_id,
                name=name,
                description=description,
                items=[self._clone_item(item) for item in template_list.items],
                created_at=datetime.now(),
                metadata={}
            )
        else:
            # Create new checklist
            checklist_items = []
            if items:
                for item in items:
                    item_id = uuid4()
                    checklist_items.append(ChecklistItem(
                        id=item_id,
                        title=item["title"],
                        description=item.get("description", ""),
                        status=ChecklistItemStatus.PENDING,
                        priority=item.get("priority", 0),
                        created_at=datetime.now(),
                        dependencies=[UUID(dep) for dep in item.get("dependencies", [])],
                        metadata=item.get("metadata", {})
                    ))
            
            checklist = Checklist(
                id=checklist_id,
                name=name,
                description=description,
                items=checklist_items,
                created_at=datetime.now(),
                metadata={}
            )
        
        self.checklists[checklist_id] = checklist
        return checklist_id

    def add_item(self,
                checklist_id: UUID,
                title: str,
                description: str = "",
                priority: int = 0,
                dependencies: Optional[List[UUID]] = None) -> UUID:
        """Add item to checklist"""
        if checklist_id not in self.checklists:
            raise ValueError(f"Checklist not found: {checklist_id}")
            
        item_id = uuid4()
        item = ChecklistItem(
            id=item_id,
            title=title,
            description=description,
            status=ChecklistItemStatus.PENDING,
            priority=priority,
            created_at=datetime.now(),
            dependencies=dependencies or []
        )
        
        self.checklists[checklist_id].items.append(item)
        return item_id

    def update_item_status(self,
                          checklist_id: UUID,
                          item_id: UUID,
                          status: ChecklistItemStatus) -> None:
        """Update item status"""
        checklist = self.checklists.get(checklist_id)
        if not checklist:
            raise ValueError(f"Checklist not found: {checklist_id}")
            
        item = self._find_item(checklist, item_id)
        if not item:
            raise ValueError(f"Item not found: {item_id}")
            
        # Check dependencies
        if status == ChecklistItemStatus.IN_PROGRESS:
            blocked = self._check_dependencies(checklist, item)
            if blocked:
                raise ValueError(f"Item blocked by dependencies: {blocked}")
            
        item.status = status

        
        if status in [ChecklistItemStatus.COMPLETED, ChecklistItemStatus.FAILED]:
            item.completed_at = datetime.now()
            
        # Check if checklist is complete
        if all(item.status in [ChecklistItemStatus.COMPLETED, ChecklistItemStatus.SKIPPED]
               for item in checklist.items):
            checklist.completed_at = datetime.now()

    def get_checklist(self, checklist_id: UUID) -> Checklist:
        """Get checklist by ID"""
        if checklist_id not in self.checklists:
            raise ValueError(f"Checklist not found: {checklist_id}")
        return self.checklists[checklist_id]

    def get_item(self, checklist_id: UUID, item_id: UUID) -> ChecklistItem:
        """Get checklist item by ID"""
        checklist = self.get_checklist(checklist_id)
        item = self._find_item(checklist, item_id)
        if not item:
            raise ValueError(f"Item not found: {item_id}")
        return item

    def delete_item(self, checklist_id: UUID, item_id: UUID) -> None:
        """Delete checklist item"""
        checklist = self.get_checklist(checklist_id)
        item = self._find_item(checklist, item_id)
        if not item:
            raise ValueError(f"Item not found: {item_id}")
            
        # Remove from main items list
        checklist.items = [i for i in checklist.items if i.id != item_id]
        
        # Remove from subtasks
        for i in checklist.items:
            i.subtasks = [st for st in i.subtasks if st.id != item_id]

    def add_subtask(self,
                   checklist_id: UUID,
                   parent_id: UUID,
                   title: str,
                   description: str = "",
                   priority: int = 0) -> UUID:
        """Add subtask to checklist item"""
        checklist = self.get_checklist(checklist_id)
        parent = self._find_item(checklist, parent_id)
        if not parent:
            raise ValueError(f"Parent item not found: {parent_id}")
            
        subtask_id = uuid4()
        subtask = ChecklistItem(
            id=subtask_id,
            title=title,
            description=description,
            status=ChecklistItemStatus.PENDING,
            priority=priority,
            created_at=datetime.now()
        )
        
        parent.subtasks.append(subtask)
        return subtask_id

    def save_template(self, name: str, checklist_id: UUID) -> None:
        """Save checklist as template"""
        if checklist_id not in self.checklists:
            raise ValueError(f"Checklist not found: {checklist_id}")
            
        self.templates[name] = self.checklists[checklist_id]

    def get_templates(self) -> Dict[str, Checklist]:
        """Get all templates"""
        return self.templates.copy()

    def _find_item(self, checklist: Checklist, item_id: UUID) -> Optional[ChecklistItem]:
        """Find item in checklist by ID"""
        for item in checklist.items:
            if item.id == item_id:
                return item
            for subtask in item.subtasks:
                if subtask.id == item_id:
                    return subtask
        return None

    def _check_dependencies(self, checklist: Checklist, item: ChecklistItem) -> List[UUID]:
        """Check if item dependencies are met"""
        blocked = []
        for dep_id in item.dependencies:
            dep_item = self._find_item(checklist, dep_id)
            if dep_item and dep_item.status != ChecklistItemStatus.COMPLETED:
                blocked.append(dep_id)
        return blocked

    def _clone_item(self, item: ChecklistItem) -> ChecklistItem:
        """Create copy of checklist item"""
        return ChecklistItem(
            id=uuid4(),
            title=item.title,
            description=item.description,
            status=ChecklistItemStatus.PENDING,
            priority=item.priority,
            created_at=datetime.now(),
            dependencies=[],
            subtasks=[self._clone_item(st) for st in item.subtasks],
            metadata=item.metadata.copy()
        )

    def get_progress(self, checklist_id: UUID) -> Dict[str, Any]:
        """Get checklist progress statistics"""
        checklist = self.get_checklist(checklist_id)
        total_items = len(checklist.items)
        completed_items = len([
            item for item in checklist.items
            if item.status == ChecklistItemStatus.COMPLETED
        ])
        
        return {
            "total_items": total_items,
            "completed_items": completed_items,
            "progress_percentage": (completed_items / total_items * 100) if total_items > 0 else 0,
            "status": {
                status.value: len([
                    item for item in checklist.items
                    if item.status == status
                ])
                for status in ChecklistItemStatus
            }
        }

```

---

# ..\..\src\task_management\process_manager.py
## File: ..\..\src\task_management\process_manager.py

```py
# ..\..\src\task_management\process_manager.py
# src/task_management/process_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import psutil
from pathlib import Path
from uuid import UUID, uuid4

@dataclass
class ProcessInfo:
    """Information about a running process"""
    id: UUID
    name: str
    command: str
    pid: int
    start_time: datetime
    status: str
    cpu_percent: float
    memory_percent: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class ProcessManager:
    """Manages external process execution and monitoring"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.active_processes: Dict[UUID, ProcessInfo] = {}
        self.completed_processes: Dict[UUID, ProcessInfo] = {}
        self._monitoring = False
        self._monitor_task: Optional[asyncio.Task] = None

    async def start_process(self,
                          name: str,
                          command: Union[str, List[str]],
                          metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Start new process"""
        if isinstance(command, str):
            command = command.split()
            
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.workspace)
        )
        
        process_id = uuid4()
        process_info = ProcessInfo(
            id=process_id,
            name=name,
            command=' '.join(command),
            pid=process.pid,
            start_time=datetime.now(),
            status="running",
            cpu_percent=0.0,
            memory_percent=0.0,
            metadata=metadata or {}
        )
        
        self.active_processes[process_id] = process_info
        
        # Start monitoring if not already running
        if not self._monitoring:
            await self.start_monitoring()
            
        return process_id

    async def stop_process(self, process_id: UUID) -> bool:
        """Stop running process"""
        if process_id not in self.active_processes:
            return False
            
        process_info = self.active_processes[process_id]
        try:
            process = psutil.Process(process_info.pid)
            process.terminate()
            
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()
                
            process_info.status = "terminated"
            self.completed_processes[process_id] = process_info
            del self.active_processes[process_id]
            return True
            
        except psutil.NoSuchProcess:
            return False


    async def start_monitoring(self) -> None:
        """Start process monitoring"""
        if self._monitoring:
            return
            
        self._monitoring = True
        self._monitor_task = asyncio.create_task(self._monitor_processes())

    async def stop_monitoring(self) -> None:
        """Stop process monitoring"""
        self._monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            self._monitor_task = None

    async def _monitor_processes(self) -> None:
        """Monitor active processes"""
        while self._monitoring:
            for process_id, info in list(self.active_processes.items()):
                try:
                    process = psutil.Process(info.pid)
                    info.cpu_percent = process.cpu_percent()
                    info.memory_percent = process.memory_percent()
                    
                    if not process.is_running():
                        info.status = "completed"
                        self.completed_processes[process_id] = info
                        del self.active_processes[process_id]
                        
                except psutil.NoSuchProcess:
                    info.status = "terminated"
                    self.completed_processes[process_id] = info
                    del self.active_processes[process_id]
                    
            await asyncio.sleep(1)

    async def get_process_output(self, process_id: UUID) -> Dict[str, str]:
        """Get process output streams"""
        if process_id not in self.active_processes:
            raise ValueError(f"Process not found: {process_id}")
            
        process = psutil.Process(self.active_processes[process_id].pid)
        try:
            stdout = []
            stderr = []
            
            # Read output
            for handler in process.open_files():
                if 'stdout' in handler.path:
                    with open(handler.path, 'r') as f:
                        stdout = f.readlines()
                elif 'stderr' in handler.path:
                    with open(handler.path, 'r') as f:
                        stderr = f.readlines()
                        
            return {
                "stdout": ''.join(stdout),
                "stderr": ''.join(stderr)
            }
            
        except (psutil.NoSuchProcess, FileNotFoundError):
            return {"stdout": "", "stderr": ""}

    def get_active_processes(self) -> List[ProcessInfo]:
        """Get list of active processes"""
        return list(self.active_processes.values())

    def get_completed_processes(self) -> List[ProcessInfo]:
        """Get list of completed processes"""
        return list(self.completed_processes.values())

    def get_process_info(self, process_id: UUID) -> Optional[ProcessInfo]:
        """Get information about specific process"""
        return self.active_processes.get(process_id) or self.completed_processes.get(process_id)
```

---

# ..\..\src\task_management\progress_tracker copy.py
## File: ..\..\src\task_management\progress_tracker copy.py

```py
# ..\..\src\task_management\progress_tracker copy.py
# src/task_management/progress_tracker.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum
from pathlib import Path

class TaskStatus(Enum):
    """Task status states"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"

@dataclass
class TaskProgress:
    """Task progress information"""
    task_id: str
    name: str
    status: TaskStatus
    progress: float  # 0-100
    start_time: datetime
    end_time: Optional[datetime] = None
    subtasks: List['TaskProgress'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class ProgressTracker:
    """Tracks progress of tasks and workflows"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else Path("temp/progress")
        self.tasks: Dict[str, TaskProgress] = {}
        self.active_task: Optional[str] = None
        
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self._load_progress()

    def start_task(self, 
                  task_id: str,
                  name: str,
                  metadata: Optional[Dict[str, Any]] = None) -> TaskProgress:
        """Start tracking a new task"""
        task = TaskProgress(
            task_id=task_id,
            name=name,
            status=TaskStatus.IN_PROGRESS,
            progress=0.0,
            start_time=datetime.now(),
            metadata=metadata or {}
        )
        
        self.tasks[task_id] = task
        self.active_task = task_id
        self._save_progress()
        
        return task

    def update_progress(self,
                       task_id: str,
                       progress: float,
                       status: Optional[TaskStatus] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update task progress"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        task = self.tasks[task_id]
        task.progress = min(100.0, max(0.0, progress))
        
        if status:
            task.status = status
            if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED]:
                task.end_time = datetime.now()
                
        if metadata:
            task.metadata.update(metadata)
            
        self._save_progress()

    def add_subtask(self,
                   parent_id: str,
                   subtask_id: str,
                   name: str,
                   metadata: Optional[Dict[str, Any]] = None) -> TaskProgress:
        """Add a subtask to a parent task"""
        if parent_id not in self.tasks:
            raise ValueError(f"Parent task {parent_id} not found")
            
        subtask = TaskProgress(
            task_id=subtask_id,
            name=name,
            status=TaskStatus.NOT_STARTED,
            progress=0.0,
            start_time=datetime.now(),
            metadata=metadata or {}
        )
        
        self.tasks[parent_id].subtasks.append(subtask)
        self.tasks[subtask_id] = subtask
        self._save_progress()
        
        return subtask

    def complete_task(self,
                     task_id: str,
                     status: TaskStatus = TaskStatus.COMPLETED,
                     metadata: Optional[Dict[str, Any]] = None) -> None:
        """Mark task as complete"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
            
        task = self.tasks[task_id]
        task.status = status
        task.progress = 100.0
        task.end_time = datetime.now()
        
        if metadata:
            task.metadata.update(metadata)
            
        if self.active_task == task_id:
            self.active_task = None
            
        self._save_progress()

    def get_task_progress(self, task_id: str) -> TaskProgress:
        """Get progress information for a task"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        return self.tasks[task_id]

    def get_all_tasks(self) -> List[TaskProgress]:
        """Get all tracked tasks"""
        return list(self.tasks.values())

    def get_active_tasks(self) -> List[TaskProgress]:
        """Get all currently active tasks"""
        return [
            task for task in self.tasks.values()
            if task.status == TaskStatus.IN_PROGRESS
        ]

    def calculate_overall_progress(self, task_id: str) -> float:
        """Calculate overall progress including subtasks"""
        task = self.tasks.get(task_id)
        if not task:
            return 0.0

        if not task.subtasks:
            return task.progress

        subtask_progress = sum(self.calculate_overall_progress(st.task_id) 
                             for st in task.subtasks)
        return (task.progress + subtask_progress) / (len(task.subtasks) + 1)

    def _save_progress(self) -> None:
        """Save progress to storage"""
        if not self.storage_path:
            return

        data = {
            task_id: {
                "name": task.name,
                "status": task.status.value,
                "progress": task.progress,
                "start_time": task.start_time.isoformat(),
                "end_time": task.end_time.isoformat() if task.end_time else None,
                "metadata": task.metadata,
                "subtasks": [
                    {
                        "task_id": st.task_id,
                        "name": st.name,
                        "status": st.status.value,
                        "progress": st.progress,
                        "start_time": st.start_time.isoformat(),
                        "end_time": st.end_time.isoformat() if st.end_time else None,
                        "metadata": st.metadata
                    }
                    for st in task.subtasks
                ]
            }
            for task_id, task in self.tasks.items()
        }

        with open(self.storage_path / "progress.json", 'w') as f:
            json.dump(data, f, indent=2)

    def _load_progress(self) -> None:
        """Load progress from storage"""
        progress_file = self.storage_path / "progress.json"
        if not progress_file.exists():
            return

        try:
            with open(progress_file) as f:
                data = json.load(f)

            for task_id, task_data in data.items():
                task = TaskProgress(
                    task_id=task_id,
                    name=task_data["name"],
                    status=TaskStatus(task_data["status"]),
                    progress=task_data["progress"],
                    start_time=datetime.fromisoformat(task_data["start_time"]),
                    end_time=datetime.fromisoformat(task_data["end_time"])
                    if task_data.get("end_time") else None,
                    metadata=task_data.get("metadata", {})
                )

                for st_data in task_data.get("subtasks", []):
                    subtask = TaskProgress(
                        task_id=st_data["task_id"],
                        name=st_data["name"],
                        status=TaskStatus(st_data["status"]),
                        progress=st_data["progress"],
                        start_time=datetime.fromisoformat(st_data["start_time"]),
                        end_time=datetime.fromisoformat(st_data["end_time"])
                        if st_data.get("end_time") else None,
                        metadata=st_data.get("metadata", {})
                    )
                    task.subtasks.append(subtask)
                    self.tasks[subtask.task_id] = subtask

                self.tasks[task_id] = task

        except Exception as e:
            print(f"Error loading progress data: {str(e)}")
```

---

# ..\..\src\task_management\progress_tracker.py
## File: ..\..\src\task_management\progress_tracker.py

```py
# ..\..\src\task_management\progress_tracker.py
# src/task_management/progress_tracker.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
import json
from pathlib import Path

# Import logger and configuration loader
from utils.logger import get_logger
from utils.config import load_config

# -------------------------------
# Define Task Status and Progress Data Structures
# -------------------------------

class TaskStatus(Enum):
    """Task status states"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"

@dataclass
class TaskProgress:
    """Task progress information"""
    task_id: UUID
    name: str
    description: str
    status: TaskStatus
    progress: float  # 0-100
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    dependencies: List[UUID] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProgressSnapshot:
    """Progress tracking snapshot"""
    timestamp: datetime
    completed_tasks: int
    total_tasks: int
    overall_progress: float
    status_counts: Dict[str, int]
    active_tasks: List[str]

# -------------------------------
# ProgressTracker Class Definition
# -------------------------------

class ProgressTracker:
    """Tracks task and workflow progress and records periodic snapshots."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.logger = get_logger(__name__)
        # Load configuration (if available) to set snapshot interval; default to 300 seconds (5 minutes)
        config = load_config()  # Assumes load_config returns a dict
        self.snapshot_interval: int = config.get("progress_tracker", {}).get("snapshot_interval", 300)
        
        # Set storage directory for progress data
        self.storage_path = Path(storage_path) if storage_path else Path("temp/progress_tracker")
        if not self.storage_path.exists():
            self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.tasks: Dict[UUID, TaskProgress] = {}
        self.snapshots: List[ProgressSnapshot] = []
        self.last_snapshot: Optional[datetime] = None
        
        # Attempt to load previously saved progress data
        self._load_progress()

    def record_snapshot(self) -> None:
        """Record a progress snapshot based on current task data."""
        now = datetime.now()
        total_tasks = len(self.tasks)
        completed_tasks = sum(
            1 for task in self.tasks.values()
            if task.status in [TaskStatus.COMPLETED, TaskStatus.SKIPPED, TaskStatus.FAILED]
        )
        overall_progress = (sum(task.progress for task in self.tasks.values()) / total_tasks) if total_tasks > 0 else 0.0
        
        # Count statuses
        status_counts: Dict[str, int] = {}
        for task in self.tasks.values():
            status_str = task.status.value
            status_counts[status_str] = status_counts.get(status_str, 0) + 1
        
        active_tasks = [str(task.task_id) for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS]
        
        snapshot = ProgressSnapshot(
            timestamp=now,
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            overall_progress=overall_progress,
            status_counts=status_counts,
            active_tasks=active_tasks
        )
        self.snapshots.append(snapshot)
        self.last_snapshot = now
        self.logger.info(f"Recorded progress snapshot at {now.isoformat()}")
        self._save_progress()

    def get_task_progress(self, task_id: Union[str, UUID]) -> Optional[TaskProgress]:
        """Get progress information for a specific task."""
        if isinstance(task_id, str):
            task_id = UUID(task_id)
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[TaskProgress]:
        """Return all tracked tasks."""
        return list(self.tasks.values())

    def get_active_tasks(self) -> List[TaskProgress]:
        """Return all currently active tasks."""
        return [task for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS]

    def calculate_overall_progress(self) -> float:
        """Calculate overall progress across all tasks."""
        if not self.tasks:
            return 0.0
        total_progress = sum(task.progress for task in self.tasks.values())
        return total_progress / len(self.tasks)

    # -------------------------------
    # Persistence Methods
    # -------------------------------

    def _save_progress(self) -> None:
        """Persist current tasks and snapshots to a JSON file."""
        try:
            data = {
                "tasks": {
                    str(task_id): {
                        "name": task.name,
                        "description": task.description,
                        "status": task.status.value,
                        "progress": task.progress,
                        "created_at": task.created_at.isoformat(),
                        "started_at": task.started_at.isoformat() if task.started_at else None,
                        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                        "dependencies": [str(dep) for dep in task.dependencies],
                        "metadata": task.metadata
                    } for task_id, task in self.tasks.items()
                },
                "snapshots": [
                    {
                        "timestamp": snap.timestamp.isoformat(),
                        "completed_tasks": snap.completed_tasks,
                        "total_tasks": snap.total_tasks,
                        "overall_progress": snap.overall_progress,
                        "status_counts": snap.status_counts,
                        "active_tasks": snap.active_tasks
                    } for snap in self.snapshots
                ]
            }
            progress_file = self.storage_path / "progress.json"
            with open(progress_file, "w") as f:
                json.dump(data, f, indent=2)
            self.logger.info("Progress data saved successfully.")
        except Exception as e:
            self.logger.error(f"Error saving progress data: {str(e)}")

    def _load_progress(self) -> None:
        """Load tasks and snapshots from persistent storage."""
        progress_file = self.storage_path / "progress.json"
        if not progress_file.exists():
            return
        try:
            with open(progress_file, "r") as f:
                data = json.load(f)
            tasks_data = data.get("tasks", {})
            for task_id_str, task_data in tasks_data.items():
                task = TaskProgress(
                    task_id=UUID(task_id_str),
                    name=task_data["name"],
                    description=task_data["description"],
                    status=TaskStatus(task_data["status"]),
                    progress=task_data["progress"],
                    created_at=datetime.fromisoformat(task_data["created_at"]),
                    started_at=datetime.fromisoformat(task_data["started_at"]) if task_data.get("started_at") else None,
                    completed_at=datetime.fromisoformat(task_data["completed_at"]) if task_data.get("completed_at") else None,
                    dependencies=[UUID(dep) for dep in task_data.get("dependencies", [])],
                    metadata=task_data.get("metadata", {})
                )
                self.tasks[task.task_id] = task
            snapshots_data = data.get("snapshots", [])
            for snap_data in snapshots_data:
                snap = ProgressSnapshot(
                    timestamp=datetime.fromisoformat(snap_data["timestamp"]),
                    completed_tasks=snap_data["completed_tasks"],
                    total_tasks=snap_data["total_tasks"],
                    overall_progress=snap_data["overall_progress"],
                    status_counts=snap_data["status_counts"],
                    active_tasks=snap_data["active_tasks"]
                )
                self.snapshots.append(snap)
            if self.snapshots:
                self.last_snapshot = self.snapshots[-1].timestamp
            self.logger.info("Progress data loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading progress data: {str(e)}")

```

---

# ..\..\src\task_management\task_prioritizer.py
## File: ..\..\src\task_management\task_prioritizer.py

```py
# ..\..\src\task_management\task_prioritizer.py
# src/task_management/task_prioritizer.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

class PriorityLevel(Enum):
    """Task priority levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    TRIVIAL = 1

@dataclass
class TaskPriority:
    """Task priority information"""
    task_id: UUID
    base_priority: PriorityLevel
    dynamic_priority: float
    last_updated: datetime
    factors: Dict[str, float]

class TaskPrioritizer:
    """Manages task prioritization"""
    
    def __init__(self):
        self.task_priorities: Dict[UUID, TaskPriority] = {}
        self.priority_factors = {
            "age": 0.1,           # Age of task
            "complexity": 0.2,    # Task complexity
            "dependencies": 0.3,  # Number of dependencies
            "urgency": 0.4       # Business urgency
        }

    def set_task_priority(self,
                         task_id: UUID,
                         priority: PriorityLevel,
                         factors: Optional[Dict[str, float]] = None) -> None:
        """Set task priority"""
        self.task_priorities[task_id] = TaskPriority(
            task_id=task_id,
            base_priority=priority,
            dynamic_priority=priority.value,
            last_updated=datetime.now(),
            factors=factors or {}
        )
        self._update_dynamic_priority(task_id)

    def update_factors(self, task_id: UUID, factors: Dict[str, float]) -> None:
        """Update task priority factors"""
        if task_id not in self.task_priorities:
            raise ValueError(f"Task not found: {task_id}")
            
        priority = self.task_priorities[task_id]
        priority.factors.update(factors)
        priority.last_updated = datetime.now()
        self._update_dynamic_priority(task_id)

    def get_priority(self, task_id: UUID) -> Optional[TaskPriority]:
        """Get task priority information"""
        return self.task_priorities.get(task_id)

    def get_prioritized_tasks(self) -> List[UUID]:
        """Get tasks sorted by priority"""
        return sorted(
            self.task_priorities.keys(),
            key=lambda x: self.task_priorities[x].dynamic_priority,
            reverse=True
        )

    def _update_dynamic_priority(self, task_id: UUID) -> None:
        """Update dynamic priority based on factors"""
        priority = self.task_priorities[task_id]
        base = priority.base_priority.value
        
        # Calculate factor adjustments
        factor_sum = 0
        for factor, weight in self.priority_factors.items():
            if factor in priority.factors:
                factor_sum += priority.factors[factor] * weight
                
        # Update dynamic priority
        priority.dynamic_priority = base * (1 + factor_sum)
```

---

# ..\..\src\task_management\__init__.py
## File: ..\..\src\task_management\__init__.py

```py
# ..\..\src\task_management\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\src\utils\config.py
## File: ..\..\src\utils\config.py

```py
# ..\..\src\utils\config.py
# src/utils/config.py
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path (Optional[str]): Path to the configuration file.
                                     Defaults to "config/default.yaml" if not provided.
    
    Returns:
        Dict[str, Any]: The configuration data as a dictionary.
    
    Raises:
        FileNotFoundError: If the configuration file is not found.
    """
    if config_path:
        path = Path(config_path)
    else:
        path = Path("config/default.yaml")
        
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
        
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config

```

---

# ..\..\src\utils\error_handler.py
## File: ..\..\src\utils\error_handler.py

```py
# ..\..\src\utils\error_handler.py
# src/utils/error_handler.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import traceback
import sys
import logging
from enum import Enum

class ErrorSeverity(Enum):
    """Error severity levels"""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ErrorContext:
    """Context information for error"""
    timestamp: datetime
    severity: ErrorSeverity
    location: str
    traceback: str
    metadata: Dict[str, Any]

@dataclass
class ErrorReport:
    """Detailed error report"""
    error_type: str
    message: str
    context: ErrorContext
    recovery_steps: List[str]
    recommendations: List[str]

class ErrorHandler:
    """Handles error tracking and recovery"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_history: List[ErrorReport] = []
        self.recovery_strategies: Dict[str, callable] = {}
        self._initialize_strategies()

    def _initialize_strategies(self) -> None:
        """Initialize error recovery strategies"""
        self.recovery_strategies.update({
            'FileNotFoundError': self._handle_missing_file,
            'PermissionError': self._handle_permission_error,
            'TimeoutError': self._handle_timeout,
            'ValueError': self._handle_value_error,
            'KeyError': self._handle_key_error
        })

    def handle_error(self,
                    error: Exception,
                    severity: ErrorSeverity,
                    metadata: Optional[Dict[str, Any]] = None) -> ErrorReport:
        """Handle and report error"""
        # Create error context
        context = ErrorContext(
            timestamp=datetime.now(),
            severity=severity,
            location=f"{error.__class__.__module__}.{error.__class__.__name__}",
            traceback=''.join(traceback.format_tb(error.__traceback__)),
            metadata=metadata or {}
        )
        
        # Create error report
        report = ErrorReport(
            error_type=error.__class__.__name__,
            message=str(error),
            context=context,
            recovery_steps=self._get_recovery_steps(error),
            recommendations=self._get_recommendations(error)
        )
        
        # Log error
        self._log_error(report)
        
        # Store in history
        self.error_history.append(report)
        
        # Attempt recovery
        self._attempt_recovery(error, context)
        
        return report

    def _log_error(self, report: ErrorReport) -> None:
        """Log error report"""
        self.logger.error(
            f"{report.error_type}: {report.message}\n"
            f"Location: {report.context.location}\n"
            f"Severity: {report.context.severity.value}\n"
            f"Traceback:\n{report.context.traceback}"
        )

    def _get_recovery_steps(self, error: Exception) -> List[str]:
        """Get recovery steps for error"""
        error_type = error.__class__.__name__
        
        if error_type in self.recovery_strategies:
            return self.recovery_strategies[error_type](error)
            
        return ["Document the error context",
                "Review recent changes",
                "Check system logs",
                "Contact support if persists"]

    def _get_recommendations(self, error: Exception) -> List[str]:
        """Get recommendations for preventing error"""
        recommendations = []
        
        if isinstance(error, FileNotFoundError):
            recommendations.extend([
                "Verify file paths before operations",
                "Implement file existence checks",
                "Add error handling for file operations"
            ])
        elif isinstance(error, PermissionError):
            recommendations.extend([
                "Check file/directory permissions",
                "Verify user access rights",
                "Implement proper permission handling"
            ])
        elif isinstance(error, TimeoutError):
            recommendations.extend([
                "Review timeout settings",
                "Implement retry mechanisms",
                "Add timeout handling"
            ])
            
        return recommendations

    def _attempt_recovery(self, error: Exception, context: ErrorContext) -> None:
        """Attempt to recover from error"""
        error_type = error.__class__.__name__
        
        if error_type in self.recovery_strategies:
            try:
                self.recovery_strategies[error_type](error)
            except Exception as e:
                self.logger.error(f"Recovery failed: {str(e)}")

    def _handle_missing_file(self, error: FileNotFoundError) -> List[str]:
        """Handle missing file error"""
        return [
            "Check if file exists at specified path",
            "Verify file name and extension",
            "Create file if missing and required",
            "Update file path if incorrect"
        ]

    def _handle_permission_error(self, error: PermissionError) -> List[str]:
        """Handle permission error"""
        return [
            "Check file/directory permissions",
            "Verify user access rights",
            "Request elevated permissions if needed",
            "Update file/directory ownership"
        ]

    def _handle_timeout(self, error: TimeoutError) -> List[str]:
        """Handle timeout error"""
        return [
            "Increase timeout duration",
            "Check system resources",
            "Implement retry mechanism",
            "Optimize operation if possible"
        ]

    def _handle_value_error(self, error: ValueError) -> List[str]:
        """Handle value error"""
        return [
            "Validate input values",
            "Check data types and formats",
            "Add input validation",
            "Provide valid value examples"
        ]

    def _handle_key_error(self, error: KeyError) -> List[str]:
        """Handle key error"""
        return [
            "Verify dictionary keys exist",
            "Check key case sensitivity",
            "Add key existence check",
            "Provide fallback values"
        ]

    def get_error_history(self, 
                         severity: Optional[ErrorSeverity] = None,
                         limit: Optional[int] = None) -> List[ErrorReport]:
        """Get error history"""
        history = self.error_history
        
        if severity:
            history = [
                report for report in history
                if report.context.severity == severity
            ]
            
        if limit:
            history = history[-limit:]
            
        return history

    def clear_history(self) -> None:
        """Clear error history"""
        self.error_history.clear()


```

---

# ..\..\src\utils\logger.py
## File: ..\..\src\utils\logger.py

```py
# ..\..\src\utils\logger.py
# src/utils/logger.py
import logging
import sys
from rich.logging import RichHandler

def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """
    Configure the root logger to use RichHandler and, optionally, a file handler.
    
    Args:
        log_level (str): The logging level (e.g., "DEBUG", "INFO").
        log_file (str, optional): Path to a file to also log messages.
    """
    # Configure RichHandler for pretty console output
    rich_handler = RichHandler(rich_tracebacks=True)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    
    handlers = [rich_handler, console_handler]
    
    # If a log_file is provided, add a FileHandler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers
    )

def get_logger(name: str) -> logging.Logger:
    """
    Return a logger with the specified name.
    
    Args:
        name (str): The name of the logger.
    
    Returns:
        logging.Logger: The configured logger.
    """
    return logging.getLogger(name)

```

---

# ..\..\src\utils\log_analyzer.py
## File: ..\..\src\utils\log_analyzer.py

```py
# ..\..\src\utils\log_analyzer.py
# src/utils/log_analyzer.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import re
from pathlib import Path
import json

@dataclass
class LogEntry:
    """Individual log entry"""
    timestamp: datetime
    level: str
    message: str
    source: str
    metadata: Dict[str, Any]

@dataclass
class LogAnalysis:
    """Analysis of log entries"""
    start_time: datetime
    end_time: datetime
    total_entries: int
    entries_by_level: Dict[str, int]
    error_patterns: Dict[str, int]
    warning_patterns: Dict[str, int]
    metadata: Dict[str, Any]

class LogAnalyzer:
    """Analyzes log files and patterns"""
    
    def __init__(self):
        self.log_entries: List[LogEntry] = []
        self.error_patterns = [
            r"error",
            r"exception",
            r"failed",
            r"failure",
            r"fatal"
        ]
        self.warning_patterns = [
            r"warning",
            r"warn",
            r"deprecated"
        ]
        self.datetime_patterns = [
            r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}",
            r"\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}"
        ]

    async def analyze_log(self, log_path: Union[str, Path]) -> LogAnalysis:
        """Analyze log file"""
        path = Path(log_path)
        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {path}")
            
        self.log_entries.clear()
        entries_by_level = {}
        error_counts = {}
        warning_counts = {}
        
        with open(path, 'r') as f:
            for line in f:
                entry = self._parse_log_entry(line)
                if entry:
                    self.log_entries.append(entry)
                    
                    # Count by level
                    entries_by_level[entry.level] = entries_by_level.get(entry.level, 0) + 1
                    
                    # Check for errors and warnings
                    message = entry.message.lower()
                    for pattern in self.error_patterns:
                        if re.search(pattern, message):
                            error_counts[pattern] = error_counts.get(pattern, 0) + 1
                            
                    for pattern in self.warning_patterns:
                        if re.search(pattern, message):
                            warning_counts[pattern] = warning_counts.get(pattern, 0) + 1
                            
        return LogAnalysis(
            start_time=self.log_entries[0].timestamp if self.log_entries else datetime.now(),
            end_time=self.log_entries[-1].timestamp if self.log_entries else datetime.now(),
            total_entries=len(self.log_entries),
            entries_by_level=entries_by_level,
            error_patterns=error_counts,
            warning_patterns=warning_counts,
            metadata={
                "file": str(path),
                "size": path.stat().st_size
            }
        )

    def _parse_log_entry(self, line: str) -> Optional[LogEntry]:
        """Parse single log entry"""
        try:
            # Extract timestamp
            timestamp = None
            for pattern in self.datetime_patterns:
                match = re.search(pattern, line)
                if match:
                    timestamp_str = match.group(0)
                    try:
                        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            timestamp = datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M:%S")
                        except ValueError:
                            continue
                    break
                    
            if not timestamp:
                return None
                
            # Extract level
            level_match = re.search(r'\[(DEBUG|INFO|WARNING|ERROR|CRITICAL)\]', line)
            level = level_match.group(1) if level_match else "UNKNOWN"
            
            # Extract message
            message = line
            if level_match:
                message = line[level_match.end():].strip()
                
            # Extract source
            source_match = re.search(r'\[([^\]]+)\]', line)
            source = source_match.group(1) if source_match else "unknown"
            
            return LogEntry(
                timestamp=timestamp,
                level=level,
                message=message,
                source=source,
                metadata={}
            )
            
        except Exception:
            return None

    def find_error_patterns(self) -> Dict[str, List[LogEntry]]:
        """Find common error patterns"""
        patterns = {}
        for entry in self.log_entries:
            if entry.level in ["ERROR", "CRITICAL"]:
                # Extract error pattern
                message = entry.message.lower()
                pattern = re.sub(r'\d+', 'N', message)
                pattern = re.sub(r'\'[^\']+\'', 'S', pattern)
                pattern = re.sub(r'"[^"]+"', 'S', pattern)
                
                if pattern not in patterns:
                    patterns[pattern] = []
                patterns[pattern].append(entry)
                
        return patterns

    def get_entries_by_timerange(self,
                               start_time: Optional[datetime] = None,
                               end_time: Optional[datetime] = None) -> List[LogEntry]:
        """Get log entries within timerange"""
        entries = self.log_entries
        
        if start_time:
            entries = [e for e in entries if e.timestamp >= start_time]
        if end_time:
            entries = [e for e in entries if e.timestamp <= end_time]
            
        return entries

    def export_analysis(self, analysis: LogAnalysis, output_path: Path) -> None:
        """Export analysis results"""
        data = {
            "start_time": analysis.start_time.isoformat(),
            "end_time": analysis.end_time.isoformat(),
            "total_entries": analysis.total_entries,
            "entries_by_level": analysis.entries_by_level,
            "error_patterns": analysis.error_patterns,
            "warning_patterns": analysis.warning_patterns,
            "metadata": analysis.metadata
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

```

---

# ..\..\src\utils\prompt_templates.py
## File: ..\..\src\utils\prompt_templates.py

```py
# ..\..\src\utils\prompt_templates.py
# src/utils/prompt_templates.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import yaml
from pathlib import Path
import re

@dataclass
class PromptTemplate:
    """Template for system prompts"""
    name: str
    content: str
    variables: List[str]
    description: str
    category: str
    version: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class PromptTemplateManager:
    """Manages system prompt templates"""
    
    def __init__(self, template_dir: Optional[str] = None):
        self.template_dir = Path(template_dir) if template_dir else Path("config/prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        self.categories: Dict[str, List[str]] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load templates from configuration files"""
        if not self.template_dir.exists():
            return

        for template_file in self.template_dir.glob("*.yaml"):
            try:
                with open(template_file) as f:
                    data = yaml.safe_load(f)
                    for name, template_data in data.items():
                        template = PromptTemplate(
                            name=name,
                            content=template_data["content"],
                            variables=template_data.get("variables", []),
                            description=template_data.get("description", ""),
                            category=template_data.get("category", "general"),
                            version=template_data.get("version", "1.0"),
                            metadata=template_data.get("metadata", {})
                        )
                        
                        self.templates[name] = template
                        
                        # Update categories
                        if template.category not in self.categories:
                            self.categories[template.category] = []
                        self.categories[template.category].append(name)
                        
            except Exception as e:
                print(f"Error loading template file {template_file}: {str(e)}")

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get template by name"""
        return self.templates.get(name)

    def get_templates_by_category(self, category: str) -> List[PromptTemplate]:
        """Get all templates in category"""
        template_names = self.categories.get(category, [])
        return [self.templates[name] for name in template_names]

    def format_prompt(self, 
                     template_name: str,
                     variables: Dict[str, Any]) -> str:
        """Format prompt with variables"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")
            
        # Validate variables
        missing_vars = set(template.variables) - set(variables.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")
            
        try:
            return template.content.format(**variables)
        except KeyError as e:
            raise ValueError(f"Invalid variable reference: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error formatting prompt: {str(e)}")

    def add_template(self,
                    name: str,
                    content: str,
                    variables: List[str],
                    description: str = "",
                    category: str = "custom",
                    version: str = "1.0",
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add new template"""
        if name in self.templates:
            raise ValueError(f"Template already exists: {name}")
            
        template = PromptTemplate(
            name=name,
            content=content,
            variables=variables,
            description=description,
            category=category,
            version=version,
            metadata=metadata or {}
        )
        
        self.templates[name] = template
        
        # Update categories
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
        
        # Save to file
        self._save_template(template)

    def update_template(self,
                       name: str,
                       content: Optional[str] = None,
                       variables: Optional[List[str]] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update existing template"""
        template = self.get_template(name)
        if not template:
            raise ValueError(f"Template not found: {name}")
            
        if content is not None:
            template.content = content
        if variables is not None:
            template.variables = variables
        if metadata is not None:
            template.metadata.update(metadata)
            
        # Update version
        version_parts = template.version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        template.version = '.'.join(version_parts)
        
        # Save changes
        self._save_template(template)

    def _save_template(self, template: PromptTemplate) -> None:
        """Save template to file"""
        if not self.template_dir.exists():
            self.template_dir.mkdir(parents=True)
            
        file_path = self.template_dir / f"{template.category}.yaml"
        
        # Load existing templates in category
        templates_data = {}
        if file_path.exists():
            with open(file_path) as f:
                templates_data = yaml.safe_load(f) or {}
                
        # Update template data
        templates_data[template.name] = {
            "content": template.content,
            "variables": template.variables,
            "description": template.description,
            "category": template.category,
            "version": template.version,
            "metadata": template.metadata
        }
        
        # Save to file
        with open(file_path, 'w') as f:
            yaml.dump(templates_data, f, sort_keys=False, indent=2)

    def extract_variables(self, content: str) -> List[str]:
        """Extract variable names from template content"""
        return [m.group(1) for m in re.finditer(r'\{(\w+)\}', content)]
```

---

# ..\..\src\utils\system_metrics.py
## File: ..\..\src\utils\system_metrics.py

```py
# ..\..\src\utils\system_metrics.py
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import psutil
import os
import logging
from pathlib import Path

@dataclass
class SystemMetrics:
    """System resource metrics. Combines fields from both implementations."""
    timestamp: datetime = field(default_factory=datetime.now)
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    disk_usage: float = 0.0
    process_memory: float = 0.0  # in MB
    network_io: Optional[Dict[str, int]] = None
    process_count: Optional[int] = None

@dataclass
class ProcessMetrics:
    """Process-specific metrics"""
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    threads: int
    status: str
    metadata: Dict[str, Any]

class MetricsCollector:
    """
    Collects and monitors system metrics.
    
    Provides asynchronous methods (for extended data such as network I/O and process count)
    as well as synchronous methods (including resource limit checks and detailed process info).
    """
    
    def __init__(self, log_dir: Optional[str] = None):
        self.log_dir: Path = Path(log_dir) if log_dir else Path("logs/metrics")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self.process = psutil.Process(os.getpid())
        # History for asynchronous metrics collection
        self.metrics_history: List[SystemMetrics] = []
        self.process_metrics: Dict[int, ProcessMetrics] = {}

    def _setup_logging(self) -> None:
        """Setup metrics logging"""
        handler = logging.FileHandler(self.log_dir / "system_metrics.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def async_collect_metrics(self) -> SystemMetrics:
        """
        Asynchronously collect extended system metrics.
        (Network I/O and process count are included in this version.)
        """
        try:
            metrics = SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=psutil.cpu_percent(),
                memory_percent=psutil.virtual_memory().percent,
                disk_usage=psutil.disk_usage('/').percent,
                network_io=dict(psutil.net_io_counters()._asdict()),
                process_count=len(psutil.pids()),
                process_memory=self.process.memory_info().rss / 1024 / 1024  # MB
            )
            self.metrics_history.append(metrics)
            self._log_metrics(metrics)
            return metrics
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {str(e)}")
            raise

    def collect_metrics(self) -> SystemMetrics:
        """
        Synchronously collect basic system metrics.
        (This version includes process memory but omits network I/O and process count.)
        """
        try:
            metrics = SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=psutil.cpu_percent(),
                memory_percent=psutil.virtual_memory().percent,
                disk_usage=psutil.disk_usage('/').percent,
                process_memory=self.process.memory_info().rss / 1024 / 1024  # MB
            )
            self._log_metrics(metrics)
            return metrics
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {str(e)}")
            return SystemMetrics()

    def _log_metrics(self, metrics: SystemMetrics) -> None:
        """Log collected metrics"""
        self.logger.info(
            f"CPU: {metrics.cpu_percent}%, Memory: {metrics.memory_percent}%, "
            f"Disk: {metrics.disk_usage}%, Process Memory: {metrics.process_memory:.2f}MB"
        )
        if metrics.network_io:
            self.logger.info(f"Network IO: {metrics.network_io}")
        if metrics.process_count is not None:
            self.logger.info(f"Process Count: {metrics.process_count}")

    def check_resource_limits(self, cpu_limit: float = 90.0, memory_limit: float = 90.0, disk_limit: float = 90.0) -> Dict[str, bool]:
        """Check if system resources are within specified limits (using synchronous metrics)."""
        metrics = self.collect_metrics()
        return {
            "cpu_ok": metrics.cpu_percent < cpu_limit,
            "memory_ok": metrics.memory_percent < memory_limit,
            "disk_ok": metrics.disk_usage < disk_limit
        }

    def get_process_info(self) -> Dict[str, Any]:
        """Get detailed process information for the current process."""
        try:
            return {
                "cpu_times": self.process.cpu_times()._asdict(),
                "memory_info": self.process.memory_info()._asdict(),
                "num_threads": self.process.num_threads(),
                "connections": len(self.process.connections()),
                "open_files": len(self.process.open_files())
            }
        except Exception as e:
            self.logger.error(f"Error getting process info: {str(e)}")
            return {}

    async def collect_process_metrics(self, pid: Optional[int] = None) -> Dict[int, ProcessMetrics]:
        """
        Asynchronously collect metrics for processes.
        If a PID is provided, only that process is measured; otherwise, all available processes are analyzed.
        """
        processes = {}
        try:
            if pid:
                proc = psutil.Process(pid)
                processes[pid] = self._get_process_metrics(proc)
            else:
                for proc in psutil.process_iter(['pid', 'name', 'status']):
                    try:
                        processes[proc.pid] = self._get_process_metrics(proc)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            self.process_metrics = processes
            return processes
        except Exception as e:
            self.logger.error(f"Error collecting process metrics: {str(e)}")
            raise

    def _get_process_metrics(self, process: psutil.Process) -> ProcessMetrics:
        """Get metrics for a specific process."""
        return ProcessMetrics(
            pid=process.pid,
            name=process.name(),
            cpu_percent=process.cpu_percent(),
            memory_percent=process.memory_percent(),
            threads=process.num_threads(),
            status=process.status(),
            metadata={
                "create_time": datetime.fromtimestamp(process.create_time()),
                "username": process.username()
            }
        )

    def get_metrics_history(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> List[SystemMetrics]:
        """Retrieve metrics history within a timeframe."""
        history = self.metrics_history
        if start_time:
            history = [m for m in history if m.timestamp >= start_time]
        if end_time:
            history = [m for m in history if m.timestamp <= end_time]
        return history

    def get_process_history(self, pid: int) -> List[ProcessMetrics]:
        """
        Retrieve process metrics history for a given PID.
        (In this implementation, only the current snapshot is available.)
        """
        return [self.process_metrics[pid]] if pid in self.process_metrics else []

    def clear_history(self) -> None:
        """Clear all collected metrics history."""
        self.metrics_history.clear()
        self.process_metrics.clear()

```

---

# ..\..\src\utils\token_counter.py
## File: ..\..\src\utils\token_counter.py

```py
# ..\..\src\utils\token_counter.py
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
import re
from transformers import AutoTokenizer

@dataclass
class TokenCount:
    """Token count information"""
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

class TokenCounter:
    """Counts tokens for different model types."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        self.tokenizer = None
        self._initialize_tokenizer()
        
    def _initialize_tokenizer(self) -> None:
        """Initialize appropriate tokenizer based on the model name."""
        try:
            if "gpt" in self.model_name.lower():
                self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            elif "claude" in self.model_name.lower():
                # Use GPT2 tokenizer as an approximation for Claude models
                self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            else:
                # Default to GPT2 tokenizer
                self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        except Exception as e:
            print(f"Error initializing tokenizer: {str(e)}")
            self.tokenizer = None

    def count_tokens(self, text: Union[str, Dict, List]) -> TokenCount:
        """
        Count tokens in the given text. If text is a dict or list, it is converted to a string.
        Returns a TokenCount dataclass instance.
        """
        if isinstance(text, (dict, list)):
            text = str(text)
        try:
            if self.tokenizer:
                tokens = self.tokenizer.encode(text)
                return TokenCount(
                    total_tokens=len(tokens),
                    prompt_tokens=len(tokens),
                    metadata={"tokenizer": self.tokenizer.__class__.__name__}
                )
            else:
                # Fallback approximation: word count plus punctuation count
                words = text.split()
                tokens_estimate = len(words) + len(re.findall(r'[.!?]', text))
                return TokenCount(
                    total_tokens=tokens_estimate,
                    prompt_tokens=tokens_estimate,
                    metadata={"method": "approximation"}
                )
        except Exception as e:
            print(f"Error counting tokens: {str(e)}")
            return TokenCount(total_tokens=0, prompt_tokens=0)

    def check_token_limit(self, text: Union[str, Dict, List], limit: int) -> bool:
        """Check if the token count for the text does not exceed the given limit."""
        count = self.count_tokens(text)
        return count.total_tokens <= limit

    def truncate_to_token_limit(self, text: str, limit: int) -> str:
        """Truncate the text so that its token count does not exceed the specified limit."""
        if not self.check_token_limit(text, limit):
            if self.tokenizer:
                tokens = self.tokenizer.encode(text)
                truncated_tokens = tokens[:limit]
                return self.tokenizer.decode(truncated_tokens)
            else:
                # Fallback approximation: reduce by estimated number of words
                words = text.split()
                estimated_limit = int(limit / 1.3)
                return ' '.join(words[:estimated_limit])
        return text

```

---

# ..\..\src\utils\__init__.py
## File: ..\..\src\utils\__init__.py

```py
# ..\..\src\utils\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\src\validation\backend_validator.py
## File: ..\..\src\validation\backend_validator.py

```py
# ..\..\src\validation\backend_validator.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import ast
import json
import re
from pathlib import Path

@dataclass
class ValidationIssue:
    """Details of a validation issue."""
    level: str  # e.g. "error", "warning", "info"
    message: str
    location: str
    suggestion: Optional[str] = None

@dataclass
class CodeFunction:
    """Information about a function in the code."""
    name: str
    args: List[str]
    returns: Optional[str]
    docstring: Optional[str]
    complexity: int
    source: str

@dataclass
class CodeClass:
    """Information about a class in the code."""
    name: str
    bases: List[str]
    methods: List[CodeFunction]
    docstring: Optional[str]
    properties: List[str]

@dataclass
class BackendValidationResult:
    """Result of backend validation."""
    valid: bool
    functions: List[CodeFunction] = field(default_factory=list)
    classes: List[CodeClass] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    issues: List[ValidationIssue] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class BackendValidator:
    """Validates backend implementation for various file types."""
    
    def __init__(self):
        self.max_complexity = 10
        self.required_docstrings = True
        self.check_type_hints = True
        self.validators = {
            ".py": self._validate_python,
            ".json": self._validate_json,
            ".yaml": self._validate_yaml,
            ".yml": self._validate_yaml,
            ".sql": self._validate_sql
        }

    async def validate_file(self, file_path: Union[str, Path]) -> BackendValidationResult:
        """Validate a backend file based on its extension."""
        path = Path(file_path)
        validator = self.validators.get(path.suffix.lower())
        if not validator:
            return BackendValidationResult(
                valid=False,
                errors=[f"Unsupported file type: {path.suffix}"],
                metadata={"file": str(path)}
            )
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return await validator(content, path)
        except Exception as e:
            return BackendValidationResult(
                valid=False,
                errors=[f"Validation error: {str(e)}"],
                metadata={"file": str(path)}
            )

    async def _validate_python(self, content: str, path: Path) -> BackendValidationResult:
        """Validate Python backend code with structural and style checks."""
        issues: List[ValidationIssue] = []
        functions: List[CodeFunction] = []
        classes: List[CodeClass] = []
        imports: List[str] = []
        metrics = {"loc": len(content.splitlines()), "comments": len(re.findall(r'#.*$', content, re.MULTILINE))}
        
        try:
            tree = ast.parse(content)
            
            # Analyze imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for name in node.names:
                        imports.append(f"{module}.{name.name}")
            # Check duplicate imports
            dupes = {x for x in imports if imports.count(x) > 1}
            if dupes:
                issues.append(ValidationIssue(
                    level="warning",
                    message=f"Duplicate imports found: {dupes}",
                    location="imports",
                    suggestion="Remove duplicate imports"
                ))
            
            # Analyze functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    returns = self._get_type_name(node.returns) if node.returns else None
                    docstring = ast.get_docstring(node)
                    complexity = self._calculate_complexity(node)
                    func = CodeFunction(
                        name=node.name,
                        args=args,
                        returns=returns,
                        docstring=docstring,
                        complexity=complexity,
                        source=ast.unparse(node) if hasattr(ast, "unparse") else ""
                    )
                    functions.append(func)
                    # Validate function details
                    if complexity > self.max_complexity:
                        issues.append(ValidationIssue(
                            level="warning",
                            message=f"Function {node.name} has high complexity ({complexity})",
                            location=f"function {node.name}",
                            suggestion="Consider refactoring into smaller functions"
                        ))
                    if self.required_docstrings and not docstring:
                        issues.append(ValidationIssue(
                            level="warning",
                            message=f"Missing docstring in function {node.name}",
                            location=f"function {node.name}",
                            suggestion="Add a docstring describing the function's purpose and parameters"
                        ))
                    if self.check_type_hints and not returns:
                        issues.append(ValidationIssue(
                            level="info",
                            message=f"Missing return type hint in function {node.name}",
                            location=f"function {node.name}",
                            suggestion="Add return type hint"
                        ))
            
            # Analyze classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    bases = [self._get_type_name(base) for base in node.bases]
                    methods = []
                    properties = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            args = [arg.arg for arg in item.args.args]
                            ret = self._get_type_name(item.returns) if item.returns else None
                            doc = ast.get_docstring(item)
                            comp = self._calculate_complexity(item)
                            methods.append(CodeFunction(
                                name=item.name,
                                args=args,
                                returns=ret,
                                docstring=doc,
                                complexity=comp,
                                source=ast.unparse(item) if hasattr(ast, "unparse") else ""
                            ))
                        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            properties.append(item.target.id)
                    cls = CodeClass(
                        name=node.name,
                        bases=bases,
                        methods=methods,
                        docstring=ast.get_docstring(node),
                        properties=properties
                    )
                    classes.append(cls)
                    if self.required_docstrings and not cls.docstring:
                        issues.append(ValidationIssue(
                            level="warning",
                            message=f"Missing docstring in class {node.name}",
                            location=f"class {node.name}",
                            suggestion="Add a docstring describing the class's purpose"
                        ))
                    if not bases:
                        issues.append(ValidationIssue(
                            level="info",
                            message=f"Class {node.name} has no base classes",
                            location=f"class {node.name}",
                            suggestion="Consider whether inheritance is applicable"
                        ))
                    for method in methods:
                        if method.complexity > self.max_complexity:
                            issues.append(ValidationIssue(
                                level="warning",
                                message=f"Method {method.name} in class {node.name} has high complexity ({method.complexity})",
                                location=f"class {node.name}",
                                suggestion="Refactor the method into simpler sub-methods"
                            ))
            
            overall_complexity = sum(func.complexity for func in functions) + sum(
                sum(m.complexity for m in cls.methods) for cls in classes
            )
            metrics["complexity"] = overall_complexity
            
        except SyntaxError as e:
            issues.append(ValidationIssue(
                level="error",
                message=f"Syntax error: {str(e)}",
                location=f"line {e.lineno}",
                suggestion="Fix syntax errors"
            ))
        except Exception as e:
            issues.append(ValidationIssue(
                level="error",
                message=f"Validation error: {str(e)}",
                location="file",
                suggestion="Check the file for issues"
            ))
            
        valid = not any(issue.level == "error" for issue in issues)
        return BackendValidationResult(
            valid=valid,
            functions=functions,
            classes=classes,
            imports=imports,
            issues=issues,
            metrics=metrics,
            metadata={"file": str(path)}
        )

    def _get_type_name(self, node: Optional[ast.AST]) -> str:
        """Get string representation of a type annotation node."""
        if node is None:
            return ""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_type_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_type_name(node.value)}[{self._get_type_name(node.slice)}]"
        else:
            return str(node)

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate a simple cyclomatic complexity metric for a node."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    async def _validate_json(self, content: str, path: Path) -> BackendValidationResult:
        """Validate a JSON configuration file."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                required_fields = {"version", "description"}
                missing = required_fields - set(data.keys())
                if missing:
                    warnings.append(f"Missing recommended fields: {missing}")
            metadata["structure"] = {"type": type(data).__name__, "keys": list(data.keys()) if isinstance(data, dict) else None}
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {str(e)}")
        valid = len(errors) == 0
        return BackendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    async def _validate_yaml(self, content: str, path: Path) -> BackendValidationResult:
        """Validate a YAML configuration file."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        try:
            import yaml
            data = yaml.safe_load(content)
            if isinstance(data, dict):
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    if line.strip() and line.startswith(' '):
                        indent = len(line) - len(line.lstrip())
                        if indent % 2 != 0:
                            warnings.append(f"Inconsistent indentation at line {i}")
                def check_empty(d, prefix=""):
                    for k, v in d.items():
                        if v is None:
                            warnings.append(f"Empty value for key: {prefix + str(k)}")
                        elif isinstance(v, dict):
                            check_empty(v, f"{prefix}{k}.")
                check_empty(data)
            metadata["structure"] = {"type": type(data).__name__, "keys": list(data.keys()) if isinstance(data, dict) else None}
        except Exception as e:
            errors.append(f"Invalid YAML: {str(e)}")
        valid = len(errors) == 0
        return BackendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    async def _validate_sql(self, content: str, path: Path) -> BackendValidationResult:
        """Validate an SQL file with basic syntax checks."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        statements = [stmt.strip() for stmt in content.split(';') if stmt.strip()]
        for i, stmt in enumerate(statements, 1):
            if not any(stmt.upper().startswith(keyword) for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']):
                warnings.append(f"Unknown SQL statement type at statement {i}")
            if 'SELECT *' in stmt.upper():
                warnings.append(f"Use of SELECT * found in statement {i}")
            if 'DROP TABLE' in stmt.upper() and 'IF EXISTS' not in stmt.upper():
                warnings.append(f"DROP TABLE without IF EXISTS in statement {i}")
            if 'CREATE TABLE' in stmt.upper() and 'IF NOT EXISTS' not in stmt.upper():
                warnings.append(f"CREATE TABLE without IF NOT EXISTS in statement {i}")
        metadata["statements_count"] = len(statements)
        valid = len(errors) == 0
        return BackendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

```

---

# ..\..\src\validation\frontend_validator.py
## File: ..\..\src\validation\frontend_validator.py

```py
# ..\..\src\validation\frontend_validator.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import re
import ast

@dataclass
class UIComponent:
    """UI component information"""
    name: str
    type: str
    properties: Dict[str, Any]
    children: List['UIComponent']
    events: List[str]
    metadata: Dict[str, Any]

@dataclass
class ValidationIssue:
    """Validation issue details"""
    level: str  # "error", "warning", or "info"
    message: str
    location: str
    suggestion: Optional[str] = None

@dataclass
class FrontendValidationResult:
    """Result of frontend validation"""
    valid: bool
    components: List[UIComponent] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class FrontendValidator:
    """Validates frontend implementation for various file types."""
    
    def __init__(self):
        self.validators = {
            ".py": self._validate_pyside6,
            ".ui": self._validate_ui_file,
            ".qss": self._validate_stylesheet,
            ".qrc": self._validate_resources
        }

    async def validate_file(self, file_path: Union[str, Path]) -> FrontendValidationResult:
        """Validate a frontend file based on its extension."""
        path = Path(file_path)
        validator = self.validators.get(path.suffix.lower())
        if not validator:
            return FrontendValidationResult(
                valid=False,
                errors=[f"Unsupported file type: {path.suffix}"],
                metadata={"file": str(path)}
            )
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return await validator(content, path)
        except Exception as e:
            return FrontendValidationResult(
                valid=False,
                errors=[f"Validation error: {str(e)}"],
                metadata={"file": str(path)}
            )

    async def _validate_pyside6(self, content: str, path: Path) -> FrontendValidationResult:
        """Validate PySide6 Python UI code."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        components: List[UIComponent] = []
        
        if not re.search(r'from\s+PySide6', content):
            errors.append("Missing PySide6 import")
        if not re.search(r'class\s+\w+\s*\(\s*(?:QMainWindow|QWidget|QDialog)\s*\)', content):
            warnings.append("No Qt window class found")
        if 'setupUi' not in content:
            warnings.append("No setupUi method found")
        if not re.search(r'\.connect\(', content):
            warnings.append("No signal connections found")
        
        # Extract components by parsing the code
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    comps = self._extract_components_from_class(node)
                    components.extend(comps)
        except Exception as e:
            errors.append(f"Error parsing UI code: {str(e)}")
        
        valid = len(errors) == 0
        return FrontendValidationResult(
            valid=valid,
            components=components,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    def _extract_components_from_class(self, node: ast.ClassDef) -> List[UIComponent]:
        """Extract UI components from a class definition."""
        components = []
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and isinstance(item.value, ast.Call):
                        if isinstance(item.value.func, ast.Name) and item.value.func.id.startswith('Q'):
                            comp = UIComponent(
                                name=target.id,
                                type=item.value.func.id,
                                properties=self._extract_properties(item.value),
                                children=[],
                                events=self._extract_events(target.id, node),
                                metadata={}
                            )
                            components.append(comp)
        return components

    def _extract_properties(self, node: ast.Call) -> Dict[str, Any]:
        """Extract properties from a widget initialization call."""
        properties = {}
        for keyword in node.keywords:
            try:
                # Use literal evaluation if possible
                properties[keyword.arg] = ast.literal_eval(keyword.value)
            except Exception:
                properties[keyword.arg] = None
        return properties

    def _extract_events(self, component_name: str, class_node: ast.ClassDef) -> List[str]:
        """Extract event names associated with a component."""
        events = []
        for node in ast.walk(class_node):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                # Look for patterns like object.clicked.connect(...)
                attr = node.func
                if hasattr(attr.value, 'id') and attr.value.id == component_name:
                    if attr.attr in ['clicked', 'triggered', 'valueChanged', 'textChanged']:
                        events.append(attr.attr)
        return events

    async def _validate_ui_file(self, content: str, path: Path) -> FrontendValidationResult:
        """Validate a Qt UI file (XML)."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        components: List[UIComponent] = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(content)
            main_widget = root.find('.//widget')
            if main_widget is None or main_widget.get('class') not in ['QMainWindow', 'QWidget', 'QDialog']:
                errors.append("Missing or invalid main widget")
            for widget in root.findall('.//widget'):
                widget_class = widget.get('class')
                widget_name = widget.get('name')
                if not widget_name:
                    warnings.append(f"Widget of type {widget_class} missing name")
                    continue
                comp = UIComponent(
                    name=widget_name,
                    type=widget_class,
                    properties=self._extract_ui_properties(widget),
                    children=self._extract_ui_children(widget),
                    events=[],  # UI files typically do not include event connections
                    metadata={}
                )
                components.append(comp)
            if not root.findall('.//layout'):
                warnings.append("No layouts found in UI file")
        except Exception as e:
            errors.append(f"Invalid UI file: {str(e)}")
        valid = len(errors) == 0
        return FrontendValidationResult(
            valid=valid,
            components=components,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    def _extract_ui_properties(self, widget: Any) -> Dict[str, Any]:
        """Extract properties from a UI widget XML element."""
        properties = {}
        for prop in widget.findall('./property'):
            prop_name = prop.get('name')
            if prop_name:
                value_elem = prop.find('./string')
                if value_elem is not None:
                    properties[prop_name] = value_elem.text
        return properties

    def _extract_ui_children(self, widget: Any) -> List[UIComponent]:
        """Extract child components from a UI widget XML element."""
        children = []
        for child in widget.findall('./widget'):
            widget_class = child.get('class')
            widget_name = child.get('name')
            if widget_name:
                child_comp = UIComponent(
                    name=widget_name,
                    type=widget_class,
                    properties=self._extract_ui_properties(child),
                    children=self._extract_ui_children(child),
                    events=[],
                    metadata={}
                )
                children.append(child_comp)
        return children

    async def _validate_stylesheet(self, content: str, path: Path) -> FrontendValidationResult:
        """Validate a Qt stylesheet (.qss)."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        for i, line in enumerate(content.splitlines(), 1):
            line = line.strip()
            if line and '{' in line and not line.endswith('{'):
                errors.append(f"Invalid selector syntax at line {i}: Selector should end with '{{'")
            if ':' in line and ';' not in line:
                errors.append(f"Missing semicolon after property at line {i}")
        if content.count('{') != content.count('}'):
            errors.append("Unmatched braces in stylesheet")
        if re.search(r'-webkit-|-moz-|-ms-|-o-', content):
            warnings.append("Vendor prefixes found; consider using standard properties")
        valid = len(errors) == 0
        return FrontendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    async def _validate_resources(self, content: str, path: Path) -> FrontendValidationResult:
        """Validate a Qt resource file (.qrc)."""
        errors = []
        warnings = []
        metadata = {"file": str(path)}
        if not content.strip().startswith('<!DOCTYPE RCC>'):
            errors.append("Invalid resource file format")
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(content)
            resource_paths = [file_elem.text for file_elem in root.findall('.//file') if file_elem.text]
            for res in resource_paths:
                res_file = path.parent / res
                if not res_file.exists():
                    errors.append(f"Resource file not found: {res}")
        except Exception as e:
            errors.append(f"Error parsing resource file: {str(e)}")
        valid = len(errors) == 0
        return FrontendValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

```

---

# ..\..\src\validation\implementation_validator.py
## File: ..\..\src\validation\implementation_validator.py

```py
# ..\..\src\validation\implementation_validator.py
# src/validation/implementation_validator.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import ast
import re

@dataclass
class ValidationResult:
    """Result of code validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    metadata: Dict[str, Any]

class ImplementationValidator:
    """Validates code implementation against requirements"""
    
    def __init__(self):
        self.requirements: Dict[str, Any] = {}
        self.validation_rules: Dict[str, callable] = {}
        self._initialize_validators()

    def _initialize_validators(self) -> None:
        """Initialize validation rules"""
        self.validation_rules.update({
            'python': self._validate_python_code,
            'javascript': self._validate_javascript_code,
            'html': self._validate_html_code,
            'css': self._validate_css_code
        })

    async def validate_implementation(self,
                                   code: str,
                                   language: str,
                                   requirements: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate code implementation"""
        if requirements:
            self.requirements.update(requirements)
            
        validator = self.validation_rules.get(language.lower())
        if not validator:
            return ValidationResult(
                valid=False,
                errors=[f"Unsupported language: {language}"],
                warnings=[],
                suggestions=[],
                metadata={}
            )
            
        return await validator(code)

    async def _validate_python_code(self, code: str) -> ValidationResult:
        """Validate Python code"""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Parse code
            tree = ast.parse(code)
            
            # Check syntax
            compile(code, '<string>', 'exec')
            
            # Analyze structure
            for node in ast.walk(tree):
                # Check function definitions
                if isinstance(node, ast.FunctionDef):
                    if not node.returns:
                        warnings.append(f"Missing return type hint in function {node.name}")
                    if not ast.get_docstring(node):
                        warnings.append(f"Missing docstring in function {node.name}")
                
                # Check class definitions
                elif isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        warnings.append(f"Missing docstring in class {node.name}")
                
                # Check error handling
                elif isinstance(node, ast.Try):
                    if not any(isinstance(handler.type, ast.Name) for handler in node.handlers):
                        warnings.append("Generic exception handler found")
                
                # Check variable names
                elif isinstance(node, ast.Name):
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.id):
                        warnings.append(f"Variable name {node.id} does not follow PEP 8")
            
            # Check requirements
            if 'required_functions' in self.requirements:
                found_functions = {n.name for n in ast.walk(tree) 
                                 if isinstance(n, ast.FunctionDef)}
                missing = set(self.requirements['required_functions']) - found_functions
                if missing:
                    errors.append(f"Missing required functions: {missing}")
            
        except SyntaxError as e:
            errors.append(f"Syntax error: {str(e)}")
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={
                "language": "python",
                "ast_nodes": len(list(ast.walk(tree))) if 'tree' in locals() else 0
            }
        )

    async def _validate_javascript_code(self, code: str) -> ValidationResult:
        """Validate JavaScript code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check basic syntax
        if code.count('{') != code.count('}'):
            errors.append("Mismatched curly braces")
            
        # Check for common issues
        if 'eval(' in code:
            warnings.append("Use of eval() detected")
        if 'with(' in code:
            warnings.append("Use of with statement detected")
            
        # Check semicolons
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.endswith('{') and not line.endswith('}') and \
               not line.endswith(';') and not line.startswith('//'):
                warnings.append(f"Missing semicolon on line {i}")
                
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "javascript"}
        )

    async def _validate_html_code(self, code: str) -> ValidationResult:
        """Validate HTML code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for unclosed tags
        tag_stack = []
        for match in re.finditer(r'</?(\w+)[^>]*>', code):
            tag = match.group(1)
            if match.group(0).startswith('</'):
                if not tag_stack or tag_stack[-1] != tag:
                    errors.append(f"Mismatched closing tag: {tag}")
                else:
                    tag_stack.pop()
            elif not match.group(0).endswith('/>'):
                tag_stack.append(tag)
                
        if tag_stack:
            errors.append(f"Unclosed tags: {', '.join(tag_stack)}")
            
        # Check for accessibility
        for match in re.finditer(r'<img[^>]*>', code):
            if 'alt=' not in match.group(0):
                warnings.append("Image missing alt attribute")
                
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "html"}
        )

    async def _validate_css_code(self, code: str) -> ValidationResult:
        """Validate CSS code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for unclosed blocks
        if code.count('{') != code.count('}'):
            errors.append("Mismatched curly braces")
            
        # Check for vendor prefixes
        vendor_prefixes = ['-webkit-', '-moz-', '-ms-', '-o-']
        for prefix in vendor_prefixes:
            if prefix in code:
                suggestions.append(f"Consider using autoprefixer for {prefix} properties")
                
        # Check for !important
        if '!important' in code:
            warnings.append("Use of !important found - consider refactoring")
            
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "css"}
        )

```

---

# ..\..\src\validation\test_manager.py
## File: ..\..\src\validation\test_manager.py

```py
# ..\..\src\validation\test_manager.py
# src/validation/test_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import subprocess
from pathlib import Path
import re
from uuid import UUID, uuid4

@dataclass
class TestCase:
    """Individual test case"""
    id: UUID
    name: str
    description: str
    test_file: Path
    test_type: str  # unit, integration, e2e
    dependencies: List[str]
    timeout: int = 30
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    last_result: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestResult:
    """Result of test execution"""
    test_id: UUID
    success: bool
    output: str
    error: Optional[str]
    duration: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class TestManager:
    """Manages test execution and results"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.test_cases: Dict[UUID, TestCase] = {}
        self.test_results: Dict[UUID, List[TestResult]] = {}
        self.active_tests: Dict[UUID, asyncio.Task] = {}
        
    async def add_test_case(self, 
                          name: str,
                          description: str,
                          test_file: Union[str, Path],
                          test_type: str,
                          dependencies: List[str] = None,
                          metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Add new test case"""
        test_id = uuid4()
        test_file = Path(test_file)
        
        if not test_file.exists():
            raise FileNotFoundError(f"Test file not found: {test_file}")
        
        self.test_cases[test_id] = TestCase(
            id=test_id,
            name=name,
            description=description,
            test_file=test_file,
            test_type=test_type,
            dependencies=dependencies or [],
            metadata=metadata or {}
        )
        
        return test_id

    async def run_test(self, test_id: UUID) -> TestResult:
        """Run specific test case"""
        if test_id not in self.test_cases:
            raise ValueError(f"Test case not found: {test_id}")
            
        test_case = self.test_cases[test_id]
        start_time = datetime.now()
        
        try:
            # Check dependencies
            for dep in test_case.dependencies:
                if not await self._check_dependency(dep):
                    raise RuntimeError(f"Dependency not met: {dep}")
            
            # Run test
            process = await asyncio.create_subprocess_exec(
                "python", "-m", "pytest", str(test_case.test_file),
                "-v", "--capture=sys",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace)
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=test_case.timeout
                )
                
                success = process.returncode == 0
                output = stdout.decode()
                error = stderr.decode() if stderr else None
                
            except asyncio.TimeoutError:
                success = False
                output = "Test timed out"
                error = f"Test exceeded timeout of {test_case.timeout} seconds"
                
            duration = (datetime.now() - start_time).total_seconds()
            
            # Create result
            result = TestResult(
                test_id=test_id,
                success=success,
                output=output,
                error=error,
                duration=duration,
                timestamp=datetime.now()
            )
            
            # Update test case
            test_case.last_run = datetime.now()
            test_case.last_result = success
            
            # Store result
            if test_id not in self.test_results:
                self.test_results[test_id] = []
            self.test_results[test_id].append(result)
            
            return result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            result = TestResult(
                test_id=test_id,
                success=False,
                output="",
                error=str(e),
                duration=duration,
                timestamp=datetime.now()
            )
            
            if test_id not in self.test_results:
                self.test_results[test_id] = []
            self.test_results[test_id].append(result)
            
            return result

    async def run_all_tests(self, test_type: Optional[str] = None) -> Dict[UUID, TestResult]:
        """Run all test cases of specified type"""
        results = {}
        test_cases = [
            tc for tc in self.test_cases.values()
            if not test_type or tc.test_type == test_type
        ]
        
        for test_case in test_cases:
            results[test_case.id] = await self.run_test(test_case.id)
            
        return results

    async def get_test_history(self, 
                            test_id: UUID,
                            limit: Optional[int] = None) -> List[TestResult]:
        """Get test execution history"""
        if test_id not in self.test_results:
            return []
            
        results = self.test_results[test_id]
        if limit:
            results = results[-limit:]
            
        return results

    async def analyze_results(self, results: Dict[UUID, TestResult]) -> Dict[str, Any]:
        """Analyze test results"""
        total_tests = len(results)
        passed_tests = len([r for r in results.values() if r.success])
        failed_tests = total_tests - passed_tests
        
        total_duration = sum(r.duration for r in results.values())
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_duration,
            "average_duration": avg_duration,
            "failed_test_ids": [
                test_id for test_id, result in results.items()
                if not result.success
            ]
        }

    async def _check_dependency(self, dependency: str) -> bool:
        """Check if dependency is satisfied"""
        if dependency.startswith("test:"):
            # Check test dependency
            test_name = dependency[5:]
            for test in self.test_cases.values():
                if test.name == test_name:
                    return test.last_result is True
        elif dependency.startswith("file:"):
            # Check file dependency
            file_path = self.workspace / dependency[5:]
            return file_path.exists()
        return False
```

---

# ..\..\src\validation\validation_rules.py
## File: ..\..\src\validation\validation_rules.py

```py
# ..\..\src\validation\validation_rules.py
# src/validation/validation_rules.py
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
import re
from enum import Enum

class ValidationLevel(Enum):
    """Validation severity levels"""
    STRICT = "strict"
    NORMAL = "normal"
    LENIENT = "lenient"

@dataclass
class ValidationRule:
    """Individual validation rule"""
    name: str
    description: str
    validator: Callable
    level: ValidationLevel
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """Result of validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]

class ValidationRules:
    """Manages and applies validation rules"""
    
    def __init__(self, level: ValidationLevel = ValidationLevel.NORMAL):
        self.level = level
        self.rules: Dict[str, ValidationRule] = {}
        self._initialize_rules()

    def _initialize_rules(self) -> None:
        """Initialize default validation rules"""
        # File path validation
        self.add_rule(
            "valid_path",
            "Validate file path format",
            self._validate_path,
            ValidationLevel.STRICT
        )
        
        # Code content validation
        self.add_rule(
            "code_syntax",
            "Validate Python code syntax",
            self._validate_code_syntax,
            ValidationLevel.STRICT
        )
        
        # Function name validation
        self.add_rule(
            "function_name",
            "Validate function naming convention",
            self._validate_function_name,
            ValidationLevel.NORMAL
        )
        
        # Variable name validation
        self.add_rule(
            "variable_name",
            "Validate variable naming convention",
            self._validate_variable_name,
            ValidationLevel.NORMAL
        )

    def add_rule(self,
                name: str,
                description: str,
                validator: Callable,
                level: ValidationLevel) -> None:
        """Add new validation rule"""
        self.rules[name] = ValidationRule(
            name=name,
            description=description,
            validator=validator,
            level=level
        )

    def validate(self, content: Any, rule_names: Optional[List[str]] = None) -> ValidationResult:
        """Validate content against rules"""
        errors = []
        warnings = []
        metadata = {}
        
        rules_to_apply = []
        if rule_names:
            rules_to_apply = [r for n, r in self.rules.items() if n in rule_names and r.enabled]
        else:
            rules_to_apply = [r for r in self.rules.values() if r.enabled]
        
        for rule in rules_to_apply:
            try:
                if rule.level.value <= self.level.value:
                    result = rule.validator(content)
                    if isinstance(result, dict):
                        if not result.get("valid", False):
                            if rule.level == ValidationLevel.STRICT:
                                errors.extend(result.get("errors", []))
                            else:
                                warnings.extend(result.get("errors", []))
                        metadata[rule.name] = result.get("metadata", {})
            except Exception as e:
                errors.append(f"Rule '{rule.name}' failed: {str(e)}")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    def _validate_path(self, path: str) -> Dict[str, Any]:
        """Validate file path"""
        if not isinstance(path, str):
            return {"valid": False, "errors": ["Path must be a string"]}
            
        if ".." in path:
            return {"valid": False, "errors": ["Path cannot contain parent directory references"]}
            
        if not path.startswith("./Workspace"):
            return {"valid": False, "errors": ["Path must be within Workspace directory"]}
            
        return {"valid": True, "metadata": {"path": path}}

    def _validate_code_syntax(self, code: str) -> Dict[str, Any]:
        """Validate Python code syntax"""
        try:
            compile(code, "<string>", "exec")
            return {"valid": True}
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [f"Syntax error: {str(e)}"],
                "metadata": {"line": e.lineno, "offset": e.offset}
            }

    def _validate_function_name(self, name: str) -> Dict[str, Any]:
        """Validate function naming convention"""
        if not re.match(r'^[a-z_][a-z0-9_]*$', name):
            return {
                "valid": False,
                "errors": ["Function name must be lowercase with underscores"]
            }
        return {"valid": True}

    def _validate_variable_name(self, name: str) -> Dict[str, Any]:
        """Validate variable naming convention"""
        if not re.match(r'^[a-z_][a-z0-9_]*$', name):
            return {
                "valid": False,
                "errors": ["Variable name must be lowercase with underscores"]
            }
        return {"valid": True}

```

---

# ..\..\src\validation\__init__.py
## File: ..\..\src\validation\__init__.py

```py
# ..\..\src\validation\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\.env.example
## File: ..\..\.env.example

```example
# ..\..\.env.example
# ==============================================
# LLM Configuration
# ==============================================
LLM_PROVIDER=lm_studio
CONTEXT_WINDOW=60000
TEMPERATURE=0.7
LM_STUDIO_BASE_URL=http://localhost:1234/v1
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# ==============================================
# Workspace & System Configuration
# ==============================================
WORKSPACE_PATH=./workspace
MAX_FILES_PER_SCAN=10

# ==============================================
# Development Settings
# ==============================================
DEBUG=false
LOG_LEVEL=INFO

# ==============================================
# Agent Settings
# ==============================================
AUTO_TEST=true

```

---

# ..\..\config\default.yaml
## File: ..\..\config\default.yaml

```yaml
# ..\..\config\default.yaml
# config/default.yaml
# Default configuration for semi-autonomous agent

general:
  workspace_path: "./Workspace"
  max_files_per_scan: 10
  debug_mode: false
  log_level: "INFO"

llm:
  default_provider: "lm_studio"
  # The following LLM variables will be loaded from .env (e.g., CONTEXT_WINDOW, TEMPERATURE)
  # context_window, temperature, and max_tokens are controlled via .env.
  providers:
    lm_studio:
      base_url: "http://localhost:1234/v1"
      timeout: 300
    anthropic:
      model: "claude-3-sonnet-20240229"
      timeout: 300
    openai:
      model: "gpt-4"
      timeout: 300

agent:
  auto_test: true
  max_retries: 3
  timeout: 300
  memory:
    short_term_limit: 100
    working_memory_limit: 50
    long_term_limit: 1000

storage:
  format: "json"
  compression: false
  backup_enabled: true
  max_backups: 5

validation:
  strict_mode: false
  auto_fix: true
  test_timeout: 30

monitoring:
  enabled: true
  metrics_interval: 60
  log_metrics: true

```

---

# ..\..\config\development.yaml
## File: ..\..\config\development.yaml

```yaml
# ..\..\config\development.yaml
# config/development.yaml
inherit: default.yaml

general:
  debug_mode: true
  log_level: "DEBUG"

llm:
  # Optionally override non-sensitive LLM settings here
  # Note: Temperature and similar variables are loaded from .env
  prompt_optimizer:
    optimization_factor: 0.9

validation:
  strict_mode: true
  auto_fix: false

```

---

# ..\..\config\gunicorn.py
## File: ..\..\config\gunicorn.py

```py
# ..\..\config\gunicorn.py
# config/gunicorn.py
import multiprocessing

# Gunicorn config
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 120
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 50
reload = False
accesslog = "-"
errorlog = "-"
loglevel = "info"

# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream agent_server {
        server agent:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://agent_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}

```

---

# ..\..\config\local.yaml
## File: ..\..\config\local.yaml

```yaml
# ..\..\config\local.yaml
# Local configuration
config/local.yaml
*.local.yaml

# Temporary files
*.log
*.tmp
*.temp

```

---

# ..\..\config\production.yaml
## File: ..\..\config\production.yaml

```yaml
# ..\..\config\production.yaml
# config/production.yaml
inherit: default.yaml

general:
  debug_mode: false
  log_level: "WARNING"

llm:
  # Temperature and similar sensitive variables remain under .env control.
  # Production-specific overrides can be added here if necessary.
  
validation:
  strict_mode: true
  auto_fix: false

storage:
  compression: true
  backup_enabled: true
  max_backups: 10

monitoring:
  metrics_interval: 30

```

---

# ..\..\config\prompts\base_prompts.yaml
## File: ..\..\config\prompts\base_prompts.yaml

```yaml
# ..\..\config\prompts\base_prompts.yaml
# config/prompts/base_prompts.yaml
# Base prompts for the system with comprehensive guidance

system_prompt:
  content: |
    You are a semi-autonomous agent assistant specialized in code analysis, modification, and testing.
    Your workspace is strictly limited to the "./Workspace" directory.
    Follow these principles meticulously:
      1. Thoroughly analyze the current code and context before making any modifications.
      2. Develop clear, step-by-step plans prior to implementation.
      3. Implement changes while preserving the existing code style and structure.
      4. Rigorously test all modifications using unit and integration tests.
      5. Document your decisions, changes, and underlying reasoning in detail.
      6. If an error occurs, perform a detailed analysis and propose concrete recovery actions.
    Always maintain awareness of the system’s state and context when deciding on your actions.
  variables: []
  description: "Base system prompt for agent initialization with detailed behavior guidelines."
  category: "system"
  version: "2.0"

analysis_prompt:
  content: |
    Analyze the following files thoroughly and provide a detailed report that includes:
      1. A high-level overview of the structure and architecture.
      2. Identification of key components and module dependencies.
      3. Potential issues, risks, or areas for improvement.
      4. Specific recommendations for immediate actions and long-term enhancements.
      5. Suggestions for further testing or analysis.
    Files to analyze: {files}
  variables: ["files"]
  description: "Detailed prompt for file analysis requiring a comprehensive report."
  category: "analysis"
  version: "2.0"

implementation_prompt:
  content: |
    Implement the requested changes by adhering to these guidelines:
      1. Analyze the existing codebase and preserve the current coding style.
      2. Add detailed documentation and inline comments to explain your changes.
      3. Develop comprehensive unit tests and, if necessary, integration tests to validate the modifications.
      4. Incorporate robust error handling to manage unexpected situations.
      5. Provide a detailed report outlining the changes, the rationale behind your decisions, and any assumptions made.
    Requested changes: {changes}
    Affected files: {files}
  variables: ["changes", "files"]
  description: "Prompt for implementation with detailed instructions and documentation requirements."
  category: "implementation"
  version: "2.0"

test_prompt:
  content: |
    Develop a comprehensive test suite to validate the implemented changes. Your test plan should include:
      1. Unit tests covering all new functionality and logical branches.
      2. Integration tests to ensure proper interaction between modules.
      3. Test cases for edge scenarios and error handling.
      4. A summary of test results and any observed anomalies.
    Implementation details: {implementation}
    Files to test: {files}
  variables: ["implementation", "files"]
  description: "Prompt for creating a full test suite with detailed validation criteria."
  category: "testing"
  version: "2.0"

```

---

# ..\..\config\prompts\error_prompts.yaml
## File: ..\..\config\prompts\error_prompts.yaml

```yaml
# ..\..\config\prompts\error_prompts.yaml
# config/prompts/error_prompts.yaml
# Error prompts for in-depth error analysis and recovery with detailed guidance

error_analysis:
  content: |
    Analyze the following error message and provide a comprehensive report that includes:
      1. A detailed root cause analysis identifying all relevant factors and contextual issues.
      2. Concrete recommendations for immediate corrective actions.
      3. Long-term prevention strategies to avoid similar errors in the future.
      4. Suggestions for additional tests or monitoring to ensure system stability.
    Error details: {error_message}
    Context: {context}
  variables: ["error_message", "context"]
  description: "Prompt for detailed error analysis, including both immediate fixes and long-term prevention."
  category: "error"
  version: "2.0"

error_recovery:
  content: |
    Propose a detailed recovery plan to restore the system to a functional state. Your plan should include:
      1. Immediate actions to stabilize the system.
      2. Steps to recover data or state if necessary.
      3. Validation measures to confirm the success of the recovery.
      4. Recommendations for follow-up tests and monitoring to prevent future issues.
    Error: {error}
    Current state: {state}
  variables: ["error", "state"]
  description: "Prompt for detailed error recovery steps, covering both immediate stabilization and long-term solutions."
  category: "error"
  version: "2.0"

```

---

# ..\..\config\prompts\workflow_prompts.yaml
## File: ..\..\config\prompts\workflow_prompts.yaml

```yaml
# ..\..\config\prompts\workflow_prompts.yaml
# config/prompts/workflow_prompts.yaml
# Workflow prompts providing step-by-step guidance for planning and validating workflows

workflow_planning:
  content: |
    Develop a comprehensive workflow plan that includes the following:
      1. A clear, step-by-step description of all actions to be taken.
      2. Identification of all dependencies between steps.
      3. Specific validation checkpoints to ensure each step is executed correctly.
      4. Clear objectives and measurable success criteria for the entire process.
      5. A detailed risk analysis along with recommended mitigation measures.
    Task description: {task}
    Context: {context}
  variables: ["task", "context"]
  description: "Prompt for creating a detailed workflow plan with clear steps, dependencies, and validation points."
  category: "workflow"
  version: "2.0"

workflow_validation:
  content: |
    Review the completed workflow and provide a detailed validation report that covers:
      1. Verification that all steps have been successfully completed.
      2. Confirmation that the results meet the specified requirements and objectives.
      3. Identification of any discrepancies or issues within the workflow.
      4. Recommendations for improvements and risk minimization.
      5. Suggestions for additional tests or inspections if needed.
    Workflow: {workflow}
    Results: {results}
  variables: ["workflow", "results"]
  description: "Prompt for validating a workflow with a focus on completeness, accuracy, and improvement recommendations."
  category: "workflow"
  version: "2.0"

```

---

# ..\..\.dockerignore
## File: ..\..\.dockerignore

```
# ..\..\.dockerignore
# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.venv
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.pytest_cache/
.mypy_cache/
.hypothesis/
.gitignore
.git/
docs/
tests/
*.md
Dockerfile
docker-compose.yml
```

---

# ..\..\.editorconfig
## File: ..\..\.editorconfig

```
# ..\..\.editorconfig
# .editorconfig
# EditorConfig is awesome: https://EditorConfig.org

# top-most EditorConfig file
root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true

[*.{py,ini,yaml,yml,json}]
indent_style = space
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab

```

---

# ..\..\.gitignore
## File: ..\..\.gitignore

```
# ..\..\.gitignore
# .gitignore

# ---------------------------
# 🐍 Python & Virtual Environments
# ---------------------------
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment (common names)
venv/
.venv/
env/
ENV/
.env

# ---------------------------
# 🛠 IDE / Editor Config Files
# ---------------------------
.idea/
.vscode/
*.swp
*.swo
*.swn
.DS_Store

# ---------------------------
# 🔧 Project-specific Files
# ---------------------------
logs/
logs/*.log  # Ignore all log files
temp/
output/     # Ignore all generated output files
workspace/*
!workspace/.gitkeep  # Keep workspace folder but ignore contents

# ---------------------------
# ✅ Testing & Coverage Reports
# ---------------------------
.coverage
coverage.xml
htmlcov/
.pytest_cache/
pytest_debug.log

# ---------------------------
# 🚀 Node.js / Frontend (if applicable)
# ---------------------------
node_modules/
package-lock.json
yarn.lock

# ---------------------------
# 🔍 Miscellaneous
# ---------------------------
*.bak  # Backup files
*.tmp  # Temporary files
*.swp  # Swap files from editors
*.log  # Any log files
*.out  # Output binary files

```

---

# ..\..\.gitlab-ci.yml
## File: ..\..\.gitlab-ci.yml

```yml
# ..\..\.gitlab-ci.yml
# .gitlab-ci.yml
image: python:3.10

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

cache:
  paths:
    - .pip-cache/
    - venv/

stages:
  - test
  - build
  - deploy

before_script:
  - python -V
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements/dev.txt

test:
  stage: test
  script:
    - flake8 src tests
    - black --check src tests
    - isort --check-only src tests
    - mypy src tests
    - pytest tests/ -v --cov=src --cov-report=term-missing
  coverage: '/TOTAL.+ ([0-9]{1,3}%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  script:
    - python -m build
  artifacts:
    paths:
      - dist/
  only:
    - main

deploy:
  stage: deploy
  script:
    - pip install twine
    - TWINE_USERNAME=${PYPI_USERNAME} TWINE_PASSWORD=${PYPI_PASSWORD} twine upload dist/*
  only:
    - main
  when: manual
```

---

# ..\..\.pre-commit-config.yaml
## File: ..\..\.pre-commit-config.yaml

```yaml
# ..\..\.pre-commit-config.yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
    -   id: debug-statements
    -   id: check-ast

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-all]

```

---

# ..\..\__init__.py
## File: ..\..\__init__.py

```py
# ..\..\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\cli_CodeMate.bat
## File: ..\..\cli_CodeMate.bat

```bat
# ..\..\cli_CodeMate.bat
@echo off
cd /d "C:\Users\Tobia\CodeMate"
"C:\Users\Tobia\AppData\Local\Programs\Python\Python310\python.exe" -m src.core.main
pause

```

---

# ..\..\deploy.sh
## File: ..\..\deploy.sh

```sh
# ..\..\deploy.sh
# scripts/deploy.sh
#!/bin/bash

# Deploy script
echo "Deploying agent system..."

# Create dist directory
mkdir -p dist

# Clean previous build
rm -rf dist/*

# Copy source files
cp -r src dist/
cp -r config dist/

# Copy requirements
cp requirements/prod.txt dist/requirements.txt

# Create necessary directories
mkdir -p dist/logs
mkdir -p dist/temp
mkdir -p dist/workspace

echo "Deployment completed"
```

---

# ..\..\docker-compose.dev.yml
## File: ..\..\docker-compose.dev.yml

```yml
# ..\..\docker-compose.dev.yml
# docker-compose.dev.yml
version: '3.8'

services:
  agent:
    build:
      context: .
      dockerfile: docker/Dockerfile.dev
    volumes:
      - .:/app
      - ./workspace:/app/workspace
    environment:
      - PYTHONPATH=/app
      - DEBUG=true
    ports:
      - "8000:8000"
    depends_on:
      - lm-studio
    networks:
      - agent_network

  lm-studio:
    image: lmstudio/lmstudio:latest
    ports:
      - "1234:1234"
    volumes:
      - ./models:/models
    environment:
      - MODEL_PATH=/models
    networks:
      - agent_network

networks:
  agent_network:
    driver: bridge

# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - agent
    networks:
      - agent_network

  agent:
    build:
      context: .
      dockerfile: docker/Dockerfile.prod
    expose:
      - "8000"
    environment:
      - PYTHONPATH=/app
    volumes:
      - workspace_data:/app/workspace
    depends_on:
      - lm-studio
    networks:
      - agent_network

  lm-studio:
    image: lmstudio/lmstudio:latest
    expose:
      - "1234"
    volumes:
      - model_data:/models
    environment:
      - MODEL_PATH=/models
    networks:
      - agent_network

volumes:
  workspace_data:
  model_data:

networks:
  agent_network:
    driver: bridge
```

---

# ..\..\docker-compose.yml
## File: ..\..\docker-compose.yml

```yml
# ..\..\docker-compose.yml
# docker-compose.yml
version: '3.8'

services:
  agent:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./workspace:/app/workspace
      - ./logs:/app/logs
      - ./config:/app/config
    environment:
      - PYTHONPATH=/app
      - WORKSPACE_PATH=/app/workspace
    ports:
      - "8000:8000"  # If needed for API
    networks:
      - agent_network

  lm-studio:  # Optional local LLM service
    image: lmstudio/lmstudio:latest
    ports:
      - "1234:1234"
    volumes:
      - ./models:/models
    environment:
      - MODEL_PATH=/models
    networks:
      - agent_network

networks:
  agent_network:
    driver: bridge



```

---

# ..\..\install_CodeMate.bat
## File: ..\..\install_CodeMate.bat

```bat
# ..\..\install_CodeMate.bat
@echo off
cd /d "C:\Users\Tobia\CodeMate"
"C:\Users\Tobia\AppData\Local\Programs\Python\Python310\python.exe" -m pip install -r requirements.txt
pause

```

---

# ..\..\Makefile
## File: ..\..\Makefile

```
# ..\..\Makefile
# Makefile
.PHONY: install test lint format clean docs

install:
	pip install -r requirements/dev.txt
	pre-commit install

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	flake8 src tests
	mypy src tests
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

docs:
	sphinx-build -b html docs/source docs/build/html

```

---

# ..\..\pyproject.toml
## File: ..\..\pyproject.toml

```toml
# ..\..\pyproject.toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "rewnozom-codemate"
version = "0.0.3"
description = "CodeMate – Din AI-drivna kodassistent"
requires-python = ">=3.10"

[tool.setuptools]
packages = ["find:"]
package-dir = {"" = "src"}

[tool.setuptools.package-data]
"*" = ["requirements/*.txt"]

[tool.setuptools.dynamic]
dependencies = {file = "requirements/base.txt"}
optional-dependencies = {
    dev = {file = "requirements/dev.txt"},
    prod = {file = "requirements/prod.txt"}
}

[project.scripts]
cmate = "cmate.main:app"
```

---

# ..\..\pytest.ini
## File: ..\..\pytest.ini

```ini
# ..\..\pytest.ini
# pytest.ini
[pytest]
minversion = 6.0
addopts = -ra -q --cov=src --cov-report=term-missing
testpaths =
    tests
python_files =
    test_*.py
    *_test.py
python_classes =
    Test
    *Tests
python_functions =
    test_*
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests

```

---

# ..\..\README.md
## File: ..\..\README.md

```md
# ..\..\README.md
# CodeMate Roadmap - Implementation Status

## Priority Levels:
- 🔴 High Priority: Critical features needed for core functionality
- 🟡 Medium Priority: Important features for enhanced operation
- 🔵 Low Priority: Nice-to-have features for future enhancement
## Core Components

### AgentCoordinator
✅ DONE:
- Full subsystem integration architecture
- Comprehensive error handling system
- Advanced event distribution system
- Audit logging and request tracking
- Dynamic configuration management
- System diagnostics infrastructure
- State-based model selection
- Multi-provider LLM integration

🔴 TODO (High Priority):
- Enhance recovery strategies with ML-based approaches
- Implement advanced workflow checkpointing
- Add dynamic resource management
- Implement auto-scaling capabilities

### WorkflowManager
✅ DONE:
- Async workflow execution engine
- Step-based workflow with dependencies
- Execution time tracking
- Persistent workflow state
- Basic error handling and recovery
- Basic workflow templates

🟡 TODO (Medium Priority):
- Advanced workflow templates
- Enhanced checkpoint/rollback system
- Multi-stage workflow validation
- Parallel workflow execution
- Workflow optimization algorithms

### StateManager
✅ DONE:
- State transitions with validation
- State persistence and history
- Observer pattern implementation
- Context window management
- Error tracking system
- State metadata handling

🟡 TODO (Medium Priority):
- Enhanced state prediction
- State optimization algorithms
- Advanced state recovery mechanisms
- Cross-state dependency tracking

### MemoryManager
✅ DONE:
- Multi-tier memory system
- Automatic cleanup
- Priority-based management
- Memory statistics
- Memory consolidation
- Token-based memory limits

🔵 TODO (Low Priority):
- Advanced memory indexing
- Memory optimization strategies
- Cross-reference memory items
- Enhanced memory persistence

## System Features

### Event System
✅ DONE:
- Event bus implementation
- Publisher/Subscriber pattern
- Event filtering
- Basic event persistence
- Event history tracking

🟡 TODO:
- Enhanced event routing
- Event prioritization
- Advanced event filtering
- Event analytics

### Request/Response Handling
✅ DONE:
- Request validation
- Response formatting
- Error handling
- Request queuing
- Basic rate limiting

🔴 TODO:
- Advanced rate limiting
- Request prioritization
- Response optimization
- Enhanced validation rules

### LLM Integration
✅ DONE:
- Multi-provider support
- State-based model selection
- Context management
- Response parsing
- Error handling

🟡 TODO:
- Enhanced prompt optimization
- Response caching
- Provider fallback system
- Context optimization

### File Services
✅ DONE:
- Basic file analysis
- Workspace scanning
- File change detection
- Basic dependency tracking

🟡 TODO:
- Enhanced dependency analysis
- Code structure visualization
- Advanced file categorization
- Pattern detection

### Validation System
✅ DONE:
- Basic validation strategies
- Frontend/Backend validation
- Implementation validation
- Test management

🔴 TODO:
- Dynamic rule generation
- Cross-file validation
- Enhanced test coverage
- Validation optimization

## Advanced Features

### Performance Optimization
✅ DONE:
- Basic metrics collection
- Resource monitoring
- Performance logging
- Basic caching

🔵 TODO:
- Advanced caching strategies
- Resource optimization
- Performance analytics
- Auto-scaling system

### Monitoring & Diagnostics
✅ DONE:
- Basic system metrics
- Error tracking
- Process monitoring
- Log analysis

🟡 TODO:
- Enhanced metrics collection
- Real-time monitoring
- Advanced diagnostics
- Performance predictions

### External Integration
✅ DONE:
- Basic Git integration
- Terminal management
- Process management

🔵 TODO:
- Enhanced Git integration
- CI/CD integration
- IDE integration
- External API integration

## Implementation Statistics:
- Core Components: ~75% Complete
- System Features: ~60% Complete
- Advanced Features: ~30% Complete
- Overall Project: ~60% Complete

## Next Steps:
1. Focus on high-priority error recovery enhancements
2. Implement advanced workflow templates
3. Enhance validation system with dynamic rules
4. Improve performance optimization
5. Develop advanced monitoring capabilities



---
---


# **CodeMate – Your AI-Powered Coding Assistant**

### 🤖 _Advanced AI Integration for Code Development, Analysis, and Testing_

**CodeMate** is a sophisticated **semi-autonomous coding assistant** that leverages multiple AI models to help you develop, analyze, and test code effectively. It uses state-based model selection to optimize AI responses for different tasks while ensuring all modifications are properly tested and integrated.

## 🔹 **Key Features**

### 1. **Advanced AI Integration**
- Multi-provider LLM support (Anthropic, OpenAI, Azure, Groq, LM Studio)
- State-based model selection for optimized responses
- Dynamic context management and token optimization
- Comprehensive error recovery and fallback systems

### 2. **Intelligent Codebase Analysis**
- Deep scanning of `./Workspace/` for project structure
- Automatic identification of frontend/backend components
- Dependency tracking and analysis
- File change monitoring and impact assessment

### 3. **Sophisticated Task Management**
- Automated task planning and workflow creation
- Interactive progress tracking with checklists
- Event-driven task orchestration
- Persistent state management with rollback capability

### 4. **Automated Code Operations**
- Context-aware code generation
- Intelligent code integration
- Style-preserving modifications
- Cross-component compatibility checks

### 5. **Comprehensive Testing**
- Automated test generation and execution
- Multi-level validation (frontend, backend, implementation)
- Test coverage analysis
- Failure recovery and code adjustment

### 6. **Advanced Monitoring**
- Detailed audit logging
- Performance metrics collection
- System diagnostics
- Error tracking and analysis

## 🔧 **System Requirements**

- Python 3.8+
- Storage: Minimum 1GB free space
- Memory: Minimum 4GB RAM recommended
- API Keys for desired LLM providers

## 📦 **Installation**

### 1. **Standard Installation**
```bash
# Navigate to project root
cd codemate

# Install package
pip install .
```

### 2. **Development Installation**
```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### 3. **Environment Setup**
```bash
# Set up development environment
python scripts/setup.py setupenv
```

This creates required directories (`logs/`, `temp/`, `workspace/`) and installs dependencies.

## ⚙️ **Configuration**

### 1. **Environment Variables**
Create a `.env` file with your configuration:
```env
# LLM Provider Settings
LLM_PROVIDER=lm_studio
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
AZURE_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# System Settings
CONTEXT_WINDOW=60000
TEMPERATURE=0.7
DEBUG=false
LOG_LEVEL=INFO
```

### 2. **Provider Selection**
CodeMate automatically selects the optimal model based on the current task:
- Code Generation: Uses specialized coding models
- Test Writing: Employs testing-focused models
- Analysis: Utilizes models optimized for comprehension

## 🖥️ **CLI Usage**

### Basic Commands
```bash
# Start interactive mode
cmate start

# Process a single request
cmate process "Analyze the project structure"

# Check system status
cmate status

# Display help
cmate --help
```

### Interactive CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Analyze code/directory | `analyze ./Workspace/` |
| `execute` | Run workflow | `execute build_pipeline` |
| `generate` | Generate code | `generate "Create login form"` |
| `visualize` | Show workflow | `visualize` |
| `config` | View/edit config | `config` |
| `diagnostics` | System diagnostics | `diagnostics` |
| `audit` | View audit logs | `audit` |

## 📊 **Advanced Usage Examples**

### 1. **Code Analysis**
```bash
agent> analyze ./Workspace/src
```
```output
Analysis Results:
- Project Structure
- Dependencies
- Code Metrics
- Potential Issues
```

### 2. **Code Generation**
```bash
agent> generate "Create a user authentication system"
```
```output
Generating:
6. User model
7. Authentication endpoints
8. Security middleware
9. Unit tests
```

### 3. **Configuration Updates**
```bash
agent> update debug_mode True
```
```output
Configuration updated:
- Debug mode enabled
- Enhanced logging activated
```

## 🔍 **Monitoring & Diagnostics**

### 1. **Audit Logs**
```bash
agent> audit
```
Shows recent operations, changes, and system events.

### 2. **Error Tracking**
```bash
agent> error
```
Displays error history with recovery attempts.

### 3. **System Diagnostics**
```bash
agent> diagnostics
```
Shows system health, resource usage, and performance metrics.

## 🛠️ **Error Handling**

CodeMate includes sophisticated error recovery:
10. Automatic error detection and classification
11. Recovery strategy selection
12. State preservation and rollback capability
13. Detailed error reporting and logging

## 📚 **Best Practices**

14. **Workspace Organization**
   - Keep workspace clean and organized
   - Use consistent file naming
   - Maintain clear directory structure

15. **Request Formulation**
   - Be specific in requests
   - Provide context when needed
   - Use proper command syntax

16. **Configuration Management**
   - Regularly update API keys
   - Monitor resource usage
   - Review audit logs

---

*CodeMate: Empowering Developers with AI-Driven Code Development*
```

---

# ..\..\run_tests.sh
## File: ..\..\run_tests.sh

```sh
# ..\..\run_tests.sh
# scripts/run_tests.sh
#!/bin/bash

# Run all tests
echo "Running tests..."
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

# ..\..\settings.toml
## File: ..\..\settings.toml

```toml
# ..\..\settings.toml
[paths]
base_dir = ""
output_dir = ""

[files]
ignored_extensions = [ ".exe", ".dll",]
ignored_files = [ "file_to_ignore.txt",]

[directories]
ignored_directories = [ "dir_to_ignore",]

[file_specific]
use_file_specific = false
specific_files = [ "",]

[output]
markdown_file_prefix = "Full_Project"
csv_file_prefix = "Detailed_Project"

[metrics]
size_unit = "KB"

[presets]
preset-1 = [ "",]

```

---

# ..\..\setup.cfg
## File: ..\..\setup.cfg

```cfg
# ..\..\setup.cfg
[metadata]
name = rewnozom-codemate
version = 0.0.03
author = Tobias Raanaes
author_email = contact@rewnozom.com  ; Use a generic email here if desired.
description = CodeMate – Your AI-driven code assistant for building, improving, and testing code.
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/rewnozom/CodeMate
project_urls =
    Bug Tracker = https://github.com/rewnozom/CodeMate/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.10
install_requires =
    pyside6>=6.0.0
    anthropic>=0.3.0
    openai>=1.0.0
    python-dotenv>=0.19.0
    rich>=10.0.0
    typer>=0.4.0
    pyyaml>=6.0.0

[options.packages.find]
where = src

[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,build,dist,*.egg

[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True

[coverage:run]
source = src
omit = tests/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    raise NotImplementedError
    if __name__ == '__main__':
    pass
    raise ImportError

```

---

# ..\..\setup.py
## File: ..\..\setup.py

```py
# ..\..\setup.py
#!/usr/bin/env python
"""
scripts/setup.py

This script serves two purposes:

1. Environment Setup Mode:
   --------------------------
   When executed with the command-line argument "setupenv", this script installs
   development dependencies (from requirements/dev.txt) and creates necessary directories
   (logs, temp, workspace, etc.). This helps set up your development environment.

   Example usage:
       python scripts/setup.py setupenv

2. Packaging Mode:
   ---------------
   When executed without the "setupenv" argument, this script calls setuptools.setup()
   with the packaging metadata so that your project (named "rewnozom-codemate") can be
   installed as a package and expose the CLI entry point "cmate". You can install the package
   using pip (e.g., pip install -e .).

   Packaging metadata includes:
       - name: "rewnozom-codemate"
       - version: "0.0.03"
       - description: A brief description of CodeMate
       - long_description: The contents of README.md (in Markdown)
       - author: "Tobias Raanaes"
       - url: "https://github.com/rewnozom/CodeMate"
       - python_requires: ">=3.10"

Usage:
  For environment setup:
      python scripts/setup.py setupenv

  For packaging (this is typically invoked via pip or build tools):
      python scripts/setup.py sdist bdist_wheel
"""

import subprocess
import sys
from pathlib import Path
import io
import os

# --------------------------------------------------
# Environment Setup Mode
# --------------------------------------------------
if len(sys.argv) > 1 and sys.argv[1] == "setupenv":
    def setup_environment():
        """Set up the development environment:
        
        - Install dependencies from requirements/dev.txt.
        - Create necessary directories (logs, temp, workspace, etc.).
        """
        try:
            print("Installing development dependencies from requirements/dev.txt ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements/dev.txt"])
            
            # List of directories to create
            directories = [
                "logs",
                "logs/metrics",
                "logs/errors",
                "temp",
                "temp/cache",
                "temp/workflow_states",
                "workspace"
            ]
            
            for directory in directories:
                Path(directory).mkdir(parents=True, exist_ok=True)
            
            print("Environment setup completed successfully.")
        except Exception as e:
            print(f"Error setting up environment: {str(e)}")
            sys.exit(1)
    
    setup_environment()
    sys.exit(0)

# --------------------------------------------------
# Packaging Mode: Call setuptools.setup()
# --------------------------------------------------
from setuptools import setup, find_packages

# Read the long description from README.md (assumes README.md is in the project root)
here = Path(__file__).parent.parent  # scripts folder's parent is the project root
readme_path = here / "README.md"
if readme_path.exists():
    with io.open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = ""

setup(
    name="rewnozom-codemate",
    version="0.0.03",
    description="CodeMate – Din AI-drivna kodassistent. Let AI build, improve, and test code for you.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tobias Raanaes",
    url="https://github.com/rewnozom/CodeMate",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "typer",
        "rich",
        "prompt_toolkit",
        "watchdog",
        "psutil",
        "python-dotenv",
        "transformers",
        # Add other dependencies as needed.
    ],
    entry_points={
        "console_scripts": [
            "cmate = cmate.main:app"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

```

---

# ..\..\tox.ini
## File: ..\..\tox.ini

```ini
# ..\..\tox.ini
# tox.ini
[tox]
envlist = py39, py310, lint
isolated_build = True

[testenv]
deps =
    -r{toxinidir}/requirements/dev.txt
commands =
    pytest tests/ -v --cov=src

[testenv:lint]
deps =
    flake8
    black
    isort
    mypy
commands =
    flake8 src tests
    black --check src tests
    isort --check-only src tests
    mypy src tests
```

---

