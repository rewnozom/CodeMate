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
