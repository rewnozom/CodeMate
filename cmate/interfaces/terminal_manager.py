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
