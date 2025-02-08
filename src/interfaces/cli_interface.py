# src/interfaces/cli_interface.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import cmd
import shlex
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from src.core.agent_coordinator import AgentCoordinator
from src.utils.logger import get_logger

@dataclass
class CommandContext:
    """Context for command execution"""
    command: str
    args: List[str]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class CLIInterface(cmd.Cmd):
    """Command-line interface for agent interaction"""
    
    intro = "Semi-Autonomous Agent Assistant CLI\nType 'help' for command list."
    prompt = "agent> "

    def __init__(self, agent: AgentCoordinator):
        super().__init__()
        self.agent = agent
        self.logger = get_logger(__name__)
        self.session = PromptSession()
        self.command_history: List[CommandContext] = []
        self._setup_completions()

    def _setup_completions(self) -> None:
        """Setup command auto-completion"""
        self.completer = WordCompleter([
            'analyze', 'execute', 'status', 'config',
            'help', 'exit', 'history', 'clear'
        ])

    def do_analyze(self, arg: str) -> None:
        """Analyze workspace files or specific file"""
        args = shlex.split(arg)
        self._record_command("analyze", args)
        
        try:
            if not args:
                print("Please specify a file or directory to analyze")
                return
                
            asyncio.get_event_loop().run_until_complete(
                self.agent.process_request({
                    "type": "analyze",
                    "data": {
                        "path": args[0]
                    }
                })
            )
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_execute(self, arg: str) -> None:
        """Execute a workflow"""
        args = shlex.split(arg)
        self._record_command("execute", args)
        
        try:
            if not args:
                print("Please specify a workflow to execute")
                return
                
            asyncio.get_event_loop().run_until_complete(
                self.agent.process_request({
                    "type": "execute",
                    "data": {
                        "workflow": args[0],
                        "args": args[1:]
                    }
                })
            )
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_status(self, arg: str) -> None:
        """Get agent status"""
        self._record_command("status", [])
        
        try:
            status = asyncio.get_event_loop().run_until_complete(
                self.agent.check_status()
            )
            print("\nAgent Status:")
            print(f"State: {status['state']}")
            print(f"Active Workflow: {status['active_workflow']}")
            print("\nMetrics:")
            for key, value in status['metrics'].items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_config(self, arg: str) -> None:
        """View or modify configuration"""
        args = shlex.split(arg)
        self._record_command("config", args)
        
        if not args:
            print("\nCurrent Configuration:")
            for key, value in self.agent.config.as_dict.items():
                print(f"{key}: {value}")
            return
            
        if len(args) < 2:
            print("Usage: config <key> <value>")
            return
            
        key, value = args[0], args[1]
        try:
            # Update configuration
            print(f"Setting {key} to {value}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_history(self, arg: str) -> None:
        """Show command history"""
        self._record_command("history", [])
        
        print("\nCommand History:")
        for ctx in self.command_history[-10:]:
            print(f"{ctx.timestamp.strftime('%H:%M:%S')} - {ctx.command} {' '.join(ctx.args)}")

    def do_clear(self, arg: str) -> None:
        """Clear the screen"""
        self._record_command("clear", [])
        print("\n" * 100)

    def do_exit(self, arg: str) -> bool:
        """Exit the CLI"""
        self._record_command("exit", [])
        print("\nExiting...")
        return True

    def _record_command(self, command: str, args: List[str]) -> None:
        """Record command execution"""
        self.command_history.append(CommandContext(
            command=command,
            args=args,
            timestamp=datetime.now()
        ))
