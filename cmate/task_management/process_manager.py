# cmate/task_management/process_manager.py
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
            # Use shell to support built-in commands on Windows
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace)
            )
        else:
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
            command=command if isinstance(command, str) else ' '.join(command),
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
            
        # In practice, you would track the output from the asyncio subprocess.
        return {
            "stdout": "",
            "stderr": ""
        }

    def get_active_processes(self) -> List[ProcessInfo]:
        """Get list of active processes"""
        return list(self.active_processes.values())

    def get_completed_processes(self) -> List[ProcessInfo]:
        """Get list of completed processes"""
        return list(self.completed_processes.values())

    def get_process_info(self, process_id: UUID) -> Optional[ProcessInfo]:
        """Get information about specific process"""
        return self.active_processes.get(process_id) or self.completed_processes.get(process_id)
