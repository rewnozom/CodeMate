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
