# Project Details

# Table of Contents
- [..\CodeMate\cmate\interfaces\__init__.py](#-CodeMate-cmate-interfaces-__init__py)
- [..\CodeMate\cmate\interfaces\cli_interface.py](#-CodeMate-cmate-interfaces-cli_interfacepy)
- [..\CodeMate\cmate\interfaces\request_handler.py](#-CodeMate-cmate-interfaces-request_handlerpy)
- [..\CodeMate\cmate\interfaces\response_formatter.py](#-CodeMate-cmate-interfaces-response_formatterpy)
- [..\CodeMate\cmate\interfaces\terminal_manager.py](#-CodeMate-cmate-interfaces-terminal_managerpy)


# ..\..\CodeMate\cmate\interfaces\__init__.py
## File: ..\..\CodeMate\cmate\interfaces\__init__.py

```py
# ..\..\CodeMate\cmate\interfaces\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\cmate\interfaces\cli_interface.py
## File: ..\..\CodeMate\cmate\interfaces\cli_interface.py

```py
# ..\..\CodeMate\cmate\interfaces\cli_interface.py
#!/usr/bin/env python
# cmate/interfaces/cli_interface.py

"""
Command-Line Interface (CLI) for CodeMate – Your AI-Powered Coding Assistant

This module provides an interactive shell for the agent. Available commands include:
  - analyze     : Analyze a file or directory.
  - execute     : Execute a workflow.
  - status      : Display current agent status.
  - config      : View current configuration.
  - update      : Update configuration dynamically.
  - visualize   : Visualize the active workflow.
  - refresh     : Refresh the LLM context.
  - generate    : Generate code from a prompt.
  - git         : Simulate Git integration.
  - diagnostics : Run system diagnostics.
  - audit       : Show recent audit log entries.
  - error       : Show error history.
  - history     : Show CLI command history.
  - debug       : Display detailed system diagnostics and internal state.
  - clear       : Clear the screen.
  - exit        : Exit the CLI.
  - help        : Display help information.
"""

import asyncio
import cmd
import shlex
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Any, Union, Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from ..core.agent_coordinator import AgentCoordinator
from ..utils.logger import get_logger

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
    """
    intro = "CodeMate – Your AI-Powered Coding Assistant CLI\nType 'help' for a list of available commands."
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

# ..\..\CodeMate\cmate\interfaces\request_handler.py
## File: ..\..\CodeMate\cmate\interfaces\request_handler.py

```py
# ..\..\CodeMate\cmate\interfaces\request_handler.py
# cmate/interfaces/request_handler.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from uuid import UUID, uuid4
from cmate.core.state_manager import StateManager, AgentState
from cmate.core.workflow_manager import WorkflowManager, WorkflowType
from cmate.utils.logger import get_logger

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
        # Update state to processing (using AgentState.ANALYZING)
        self.state_manager.update_state(AgentState.ANALYZING, {
            "request_id": str(context.id),
            "request_type": context.request_type
        })
        
        # Create workflow for the request.
        # Map the request type to a workflow type (for example, "analyze" maps to NAVIGATION).
        workflow_type = self._map_request_to_workflow_type(context.request_type)
        workflow = await self.workflow_manager.create_workflow(
            workflow_type=workflow_type,
            name=f"Workflow for {context.request_type}",
            description=f"Processing request: {context.request_type}",
            context=context.content
        )
        
        # Execute workflow
        result = await self.workflow_manager.execute_workflow(workflow.id)
        
        # Update state to idle
        self.state_manager.update_state(AgentState.IDLE)
        
        return result

    def _validate_request(self, request_data: Dict[str, Any]) -> None:
        """Validate request data"""
        required_fields = ["type", "data"]
        for field in required_fields:
            if field not in request_data:
                raise ValueError(f"Missing required field: {field}")

    def _map_request_to_workflow_type(self, request_type: str):
        """Map a request type to a workflow type"""
        # For this example, we assume that an "analyze" request uses the NAVIGATION workflow.
        if request_type.lower() == "analyze":
            from cmate.core.workflow_manager import WorkflowType
            return WorkflowType.NAVIGATION
        # Default to IMPLEMENTATION for other types.
        from cmate.core.workflow_manager import WorkflowType
        return WorkflowType.IMPLEMENTATION

```

---

# ..\..\CodeMate\cmate\interfaces\response_formatter.py
## File: ..\..\CodeMate\cmate\interfaces\response_formatter.py

```py
# ..\..\CodeMate\cmate\interfaces\response_formatter.py
# cmate/interfaces/response_formatter.py
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

# ..\..\CodeMate\cmate\interfaces\terminal_manager.py
## File: ..\..\CodeMate\cmate\interfaces\terminal_manager.py

```py
# ..\..\CodeMate\cmate\interfaces\terminal_manager.py
# cmate/interfaces/terminal_manager.py
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
        # If command is a string, use it directly
        if isinstance(command, str):
            cmd_to_run = command
        else:
            cmd_to_run = ' '.join(command)

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
            proc_key = f"{cmd_to_run}_{start_time.timestamp()}"

        try:
            # Use shell execution if command is a string to support built-in commands on Windows
            if isinstance(command, str):
                process = await asyncio.create_subprocess_shell(
                    cmd_to_run,
                    stdout=asyncio.subprocess.PIPE if capture_output else None,
                    stderr=asyncio.subprocess.PIPE if capture_output else None,
                    env=env,
                    cwd=cwd
                )
            else:
                process = await asyncio.create_subprocess_exec(
                    *command,
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
                    command=cmd_to_run,
                    exit_code=process.returncode,
                    stdout=stdout.decode() if stdout else "",
                    stderr=stderr.decode() if stderr else "",
                    duration=duration,
                    timestamp=start_time,
                    pid=process.pid
                )
                if session_id:
                    session.last_command = cmd_to_run
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
                command=cmd_to_run,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                duration=duration,
                timestamp=start_time
            )
            if session_id:
                session.last_command = cmd_to_run
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

