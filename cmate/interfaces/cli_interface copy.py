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
