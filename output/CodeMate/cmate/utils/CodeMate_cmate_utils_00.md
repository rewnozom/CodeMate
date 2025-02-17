# Project Details

# Table of Contents
- [..\CodeMate\cmate\utils\__init__.py](#-CodeMate-cmate-utils-__init__py)
- [..\CodeMate\cmate\utils\config.py](#-CodeMate-cmate-utils-configpy)
- [..\CodeMate\cmate\utils\error_handler.py](#-CodeMate-cmate-utils-error_handlerpy)
- [..\CodeMate\cmate\utils\html_logger.py](#-CodeMate-cmate-utils-html_loggerpy)
- [..\CodeMate\cmate\utils\log_analyzer.py](#-CodeMate-cmate-utils-log_analyzerpy)
- [..\CodeMate\cmate\utils\logger.py](#-CodeMate-cmate-utils-loggerpy)
- [..\CodeMate\cmate\utils\prompt_templates.py](#-CodeMate-cmate-utils-prompt_templatespy)
- [..\CodeMate\cmate\utils\system_metrics.py](#-CodeMate-cmate-utils-system_metricspy)
- [..\CodeMate\cmate\utils\token_counter.py](#-CodeMate-cmate-utils-token_counterpy)


# ..\..\CodeMate\cmate\utils\__init__.py
## File: ..\..\CodeMate\cmate\utils\__init__.py

```py
# ..\..\CodeMate\cmate\utils\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\cmate\utils\config.py
## File: ..\..\CodeMate\cmate\utils\config.py

```py
# ..\..\CodeMate\cmate\utils\config.py
#!/usr/bin/env python
# cmate/utils/config.py

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def load_yaml_config(file_path: Path) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Determine the base configuration path by going three levels up from this file.
BASE_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "default.yaml"
default_config = load_yaml_config(BASE_CONFIG_PATH) if BASE_CONFIG_PATH.exists() else {}

# Merge environment-specific overrides (e.g. development.yaml or production.yaml)
ENV = os.getenv("ENVIRONMENT", "development")
override_path = Path(__file__).parent.parent.parent / "config" / f"{ENV}.yaml"
if override_path.exists():
    override_config = load_yaml_config(override_path)
    default_config.update(override_config)

# Load additional LLM settings from .env if necessary
default_config.setdefault("llm", {})
default_config["llm"]["temperature"] = float(os.getenv("TEMPERATURE", default_config["llm"].get("temperature", 0.7)))
default_config["llm"]["context_window"] = int(os.getenv("CONTEXT_WINDOW", default_config["llm"].get("context_window", 60000)))
default_config["llm"]["default_provider"] = os.getenv("LLM_PROVIDER", default_config["llm"].get("default_provider", "lm_studio"))

# Add conversation and prompt_optimizer settings if not present
default_config["llm"].setdefault("conversation", {"history_limit": 50})
default_config["llm"].setdefault("prompt_optimizer", {"enabled": True, "optimization_factor": 1.0})

# Expose the final configuration as a global variable
config = default_config

def load_config(config_path: str = None) -> dict:
    """
    Load configuration from a YAML file if provided;
    otherwise, return the default configuration.
    """
    if config_path:
        path = Path(config_path)
        if path.exists():
            return load_yaml_config(path)
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
    return config

```

---

# ..\..\CodeMate\cmate\utils\error_handler.py
## File: ..\..\CodeMate\cmate\utils\error_handler.py

```py
# ..\..\CodeMate\cmate\utils\error_handler.py
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

# ..\..\CodeMate\cmate\utils\html_logger.py
## File: ..\..\CodeMate\cmate\utils\html_logger.py

```py
# ..\..\CodeMate\cmate\utils\html_logger.py
# ..\..\cmate\utils\html_logger.py
# cmate/utils/html_logger.py
"""
HTMLLogHandler: A logging handler that collects log records during a run and writes an HTML report.

This handler gathers all log records and, upon closure, writes an HTML file that features:
- A dark-themed design with dark-gray background and orange accents.
- A header with a search box, level filter buttons (with count badges), and "Collapse All"/"Expand All" buttons.
- A table listing each log record with timestamp, level, logger name, and message.
- Each log message is contained in a collapsible area with an individual "Toggle" button and a "Copy" button.
- A status bar that displays the number of visible logs versus total logs and version information.
  
Place this file in cmate/utils/ and integrate it into your __main__.py and run_tests.py.
"""

import logging
import datetime
from pathlib import Path

class HTMLLogHandler(logging.Handler):
    def __init__(self, log_dir: str = "logs", filename_prefix: str = "run_log"):
        """
        Initialize the HTMLLogHandler.
        
        Args:
            log_dir (str): Directory where the HTML log file will be saved.
            filename_prefix (str): Prefix for the generated HTML file name.
        """
        super().__init__()
        self.records = []
        self.log_dir = Path(log_dir)
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = self.log_dir / f"{filename_prefix}_{timestamp}.html"

    def formatTime(self, record, datefmt=None):
        """Custom implementation to format the record timestamp."""
        ct = datetime.datetime.fromtimestamp(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y-%m-%d %H:%M:%S")
        return s

    def emit(self, record: logging.LogRecord):
        """
        Emit a log record.
        
        The record is formatted and stored as an HTML table row.
        Each row includes:
          - A "Toggle" button to collapse/expand the log message.
          - A "Copy" button to copy the message text.
        """
        try:
            msg = self.format(record)
            timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
            # Create a unique row id for JavaScript toggling.
            row_id = f"log_row_{len(self.records)}"
            # Build the row with an individual Copy button.
            row = (
                f"<tr id='{row_id}'>"
                f"<td class='timestamp'>{timestamp}</td>"
                f"<td class='level-{record.levelname.lower()}'>{record.levelname}</td>"
                f"<td class='logger-name'>{record.name}</td>"
                f"<td>"
                f"<button class='toggle-button' onclick='toggleMessage(this)'>Collapse</button>"
                f"<button class='copy-button' onclick='copyToClipboard(this)'>Copy</button>"
                f"<div class='collapsible-content'>{msg}</div>"
                f"</td>"
                f"</tr>\n"
            )
            self.records.append(row)
        except Exception:
            self.handleError(record)

    def close(self):
        """
        Write out the complete HTML log report and then close the handler.
        
        The HTML report includes:
          - A sticky header with search/filter controls.
          - A table with all log records.
          - A status bar showing visible logs / total logs and version info.
        """
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n<html>\n<head>\n")
                f.write("<meta charset='utf-8'>\n")
                f.write("<title>CodeMate Log Report</title>\n")
                # Dark theme CSS styles with orange accents and professional enhancements
                f.write("<style>\n")
                f.write("body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; min-height: 100vh; "
                        "background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); color: #e0e0e0; }\n")
                f.write(".container { max-width: 1400px; margin: 0 auto; padding: 2rem; }\n")
                f.write("header { margin-bottom: 2rem; padding: 1rem 0; border-bottom: 2px solid #3d3d3d; "
                        "display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }\n")
                f.write(".header-title { flex: 1; }\n")
                f.write(".header-controls { display: flex; gap: 0.5rem; flex-wrap: wrap; }\n")
                f.write("header h1 { font-size: 1.8rem; font-weight: 500; color: #fff; margin: 0; }\n")
                f.write(".filter-bar { background: #383838; padding: 1rem; border-radius: 6px; margin-bottom: 1rem; "
                        "display: flex; gap: 1rem; flex-wrap: wrap; }\n")
                f.write(".search-box { background: #2d2d2d; border: 1px solid #4d4d4d; padding: 0.5rem 1rem; "
                        "color: #fff; border-radius: 4px; flex: 1; min-width: 200px; }\n")
                f.write("button { padding: 8px 16px; cursor: pointer; background-color: #e67e00; border: none; "
                        "border-radius: 4px; color: #fff; font-weight: 500; transition: all 0.2s ease; display: flex; "
                        "align-items: center; gap: 0.5rem; }\n")
                f.write("button:hover { background-color: #ff9008; transform: translateY(-1px); }\n")
                f.write("button.level-filter { background-color: #2d2d2d; }\n")
                f.write("button.level-filter.active { background-color: #e67e00; }\n")
                f.write(".table-container { background: #2d2d2d; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; }\n")
                f.write("table { width: 100%; border-collapse: collapse; }\n")
                f.write("th, td { padding: 12px 16px; text-align: left; vertical-align: top; }\n")
                f.write("th { background-color: #383838; font-weight: 500; color: #fff; font-size: 0.95rem; "
                        "text-transform: uppercase; letter-spacing: 0.5px; position: sticky; top: 0; z-index: 1; }\n")
                f.write("tr:nth-child(even) { background-color: #333333; }\n")
                f.write("tr:hover { background-color: #3a3a3a; }\n")
                f.write(".collapsible-content { display: block; margin-top: 8px; line-height: 1.5; font-family: 'Consolas', monospace; white-space: pre-wrap; }\n")
                f.write(".level-error { color: #ff6b6b; font-weight: 500; }\n")
                f.write(".level-warning { color: #ffd93d; font-weight: 500; }\n")
                f.write(".level-info { color: #4dacff; font-weight: 500; }\n")
                f.write(".level-debug { color: #6ce5bb; font-weight: 500; }\n")
                f.write(".level-success { color: #28a745; font-weight: 500; }\n")
                f.write(".timestamp { color: #888; font-family: 'Consolas', monospace; font-size: 0.9rem; white-space: nowrap; }\n")
                f.write(".logger-name { font-family: 'Consolas', monospace; font-size: 0.9rem; color: #b8b8b8; }\n")
                f.write(".error-trace { background: #3d2c2c; padding: 8px 12px; border-radius: 4px; margin-top: 8px; font-family: 'Consolas', monospace; font-size: 0.9rem; border-left: 3px solid #ff6b6b; }\n")
                f.write(".copy-button { background: #2d2d2d; color: #888; padding: 2px 8px; font-size: 0.8rem; margin-left: 0.5rem; }\n")
                f.write(".copy-button:hover { background: #383838; color: #fff; }\n")
                f.write(".badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; margin-left: 0.5rem; }\n")
                f.write(".badge-error { background: #ff6b6b33; color: #ff6b6b; }\n")
                f.write(".badge-warning { background: #ffd93d33; color: #ffd93d; }\n")
                f.write(".badge-info { background: #4dacff33; color: #4dacff; }\n")
                f.write(".badge-debug { background: #6ce5bb33; color: #6ce5bb; }\n")
                f.write(".badge-success { background: #28a74533; color: #28a745; }\n")
                f.write(".status-bar { margin-top: 1rem; padding: 0.5rem; background: #383838; border-radius: 4px; display: flex; justify-content: space-between; font-size: 0.9rem; color: #888; }\n")
                f.write("</style>\n")
                # JavaScript for interactivity: toggling messages, filtering, copying, and updating the status bar.
                f.write("<script>\n")
                f.write("function toggleMessage(btn) {\n")
                f.write("  var contentDiv = btn.nextElementSibling;\n")
                f.write("  if (contentDiv.style.display === 'none') {\n")
                f.write("    contentDiv.style.display = 'block';\n")
                f.write("    btn.textContent = 'Collapse';\n")
                f.write("  } else {\n")
                f.write("    contentDiv.style.display = 'none';\n")
                f.write("    btn.textContent = 'Expand';\n")
                f.write("  }\n")
                f.write("}\n")
                f.write("function collapseAll() {\n")
                f.write("  var buttons = document.getElementsByClassName('toggle-button');\n")
                f.write("  for (var i = 0; i < buttons.length; i++) {\n")
                f.write("    var btn = buttons[i];\n")
                f.write("    var contentDiv = btn.nextElementSibling;\n")
                f.write("    contentDiv.style.display = 'none';\n")
                f.write("    btn.textContent = 'Expand';\n")
                f.write("  }\n")
                f.write("  filterLogs();\n")
                f.write("}\n")
                f.write("function expandAll() {\n")
                f.write("  var buttons = document.getElementsByClassName('toggle-button');\n")
                f.write("  for (var i = 0; i < buttons.length; i++) {\n")
                f.write("    var btn = buttons[i];\n")
                f.write("    var contentDiv = btn.nextElementSibling;\n")
                f.write("    contentDiv.style.display = 'block';\n")
                f.write("    btn.textContent = 'Collapse';\n")
                f.write("  }\n")
                f.write("  filterLogs();\n")
                f.write("}\n")
                f.write("function filterLogs() {\n")
                f.write("  const searchText = document.getElementById('searchBox').value.toLowerCase();\n")
                f.write("  const rows = document.querySelectorAll('tbody tr');\n")
                f.write("  let visible = 0;\n")
                f.write("  rows.forEach(row => {\n")
                f.write("    const text = row.textContent.toLowerCase();\n")
                f.write("    const display = text.includes(searchText);\n")
                f.write("    row.style.display = display ? '' : 'none';\n")
                f.write("    if (display) visible++;\n")
                f.write("  });\n")
                f.write("  updateStatusBar(visible);\n")
                f.write("}\n")
                f.write("function toggleLevelFilter(level) {\n")
                f.write("  const btn = document.querySelector(`button[data-level='${level}']`);\n")
                f.write("  btn.classList.toggle('active');\n")
                f.write("  filterByLevels();\n")
                f.write("}\n")
                f.write("function filterByLevels() {\n")
                f.write("  const activeFilters = Array.from(document.querySelectorAll('button.level-filter.active'))\n")
                f.write("      .map(btn => btn.dataset.level);\n")
                f.write("  const rows = document.querySelectorAll('tbody tr');\n")
                f.write("  let visible = 0;\n")
                f.write("  rows.forEach(row => {\n")
                f.write("    const level = row.querySelector('td:nth-child(2)').textContent;\n")
                f.write("    const display = (activeFilters.length === 0 || activeFilters.includes(level)) &&\n")
                f.write("                    row.style.display !== 'none';\n")
                f.write("    row.style.display = display ? '' : 'none';\n")
                f.write("    if (display) visible++;\n")
                f.write("  });\n")
                f.write("  updateStatusBar(visible);\n")
                f.write("}\n")
                f.write("function updateStatusBar(visibleCount) {\n")
                f.write("  const total = document.querySelectorAll('tbody tr').length;\n")
                f.write("  document.getElementById('logCount').textContent = `Showing ${visibleCount} of ${total} logs`;\n")
                f.write("}\n")
                f.write("function copyToClipboard(btn) {\n")
                f.write("  const content = btn.parentElement.querySelector('.collapsible-content').textContent;\n")
                f.write("  navigator.clipboard.writeText(content);\n")
                f.write("  const originalText = btn.textContent;\n")
                f.write("  btn.textContent = 'Copied!';\n")
                f.write("  setTimeout(() => btn.textContent = originalText, 1000);\n")
                f.write("}\n")
                f.write("document.addEventListener('DOMContentLoaded', () => {\n")
                f.write("  const total = document.querySelectorAll('tbody tr').length;\n")
                f.write("  updateStatusBar(total);\n")
                f.write("});\n")
                f.write("</script>\n")
                f.write("</head>\n<body>\n")
                f.write("<div class='container'>\n")
                f.write("  <header>\n")
                f.write("    <div class='header-title'>\n")
                f.write(f"      <h1>CodeMate Log Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>\n")
                f.write("    </div>\n")
                f.write("    <div class='header-controls'>\n")
                f.write("      <button onclick='collapseAll()'>Collapse All</button>\n")
                f.write("      <button onclick='expandAll()'>Expand All</button>\n")
                f.write("    </div>\n")
                f.write("  </header>\n")
                f.write("  <div class='filter-bar'>\n")
                f.write("    <input type='text' id='searchBox' class='search-box' placeholder='Search logs...' oninput='filterLogs()'>\n")
                f.write("    <button class='level-filter' data-level='ERROR' onclick='toggleLevelFilter(\"ERROR\")'>\n")
                f.write("      ERROR <span class='badge badge-error'>0</span>\n")
                f.write("    </button>\n")
                f.write("    <button class='level-filter' data-level='WARNING' onclick='toggleLevelFilter(\"WARNING\")'>\n")
                f.write("      WARNING <span class='badge badge-warning'>0</span>\n")
                f.write("    </button>\n")
                f.write("    <button class='level-filter' data-level='INFO' onclick='toggleLevelFilter(\"INFO\")'>\n")
                f.write("      INFO <span class='badge badge-info'>0</span>\n")
                f.write("    </button>\n")
                f.write("    <button class='level-filter' data-level='DEBUG' onclick='toggleLevelFilter(\"DEBUG\")'>\n")
                f.write("      DEBUG <span class='badge badge-debug'>0</span>\n")
                f.write("    </button>\n")
                f.write("    <button class='level-filter' data-level='SUCCESS' onclick='toggleLevelFilter(\"SUCCESS\")'>\n")
                f.write("      SUCCESS <span class='badge badge-success'>0</span>\n")
                f.write("    </button>\n")
                f.write("  </div>\n")
                f.write("  <div class='table-container'>\n")
                f.write("    <table>\n")
                f.write("      <thead>\n")
                f.write("        <tr>\n")
                f.write("          <th>Timestamp</th>\n")
                f.write("          <th>Level</th>\n")
                f.write("          <th>Logger</th>\n")
                f.write("          <th>Message</th>\n")
                f.write("        </tr>\n")
                f.write("      </thead>\n")
                f.write("      <tbody>\n")
                for row in self.records:
                    f.write(row)
                f.write("      </tbody>\n")
                f.write("    </table>\n")
                f.write("  </div>\n")
                f.write("  <div class='status-bar'>\n")
                f.write("    <span id='logCount'>Showing 0 logs</span>\n")
                f.write("    <span>CodeMate Logger v1.0.0</span>\n")
                f.write("  </div>\n")
                f.write("</div>\n")
                f.write("</body>\n</html>\n")
        except Exception as e:
            print(f"Error writing HTML log file: {str(e)}")
        finally:
            super().close()

```

---

# ..\..\CodeMate\cmate\utils\log_analyzer.py
## File: ..\..\CodeMate\cmate\utils\log_analyzer.py

```py
# ..\..\CodeMate\cmate\utils\log_analyzer.py
# ..\..\cmate\utils\log_analyzer.py
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
                
            # Extract level (now including SUCCESS)
            level_match = re.search(r'\[(DEBUG|INFO|WARNING|ERROR|CRITICAL|SUCCESS)\]', line)
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

# ..\..\CodeMate\cmate\utils\logger.py
## File: ..\..\CodeMate\cmate\utils\logger.py

```py
# ..\..\CodeMate\cmate\utils\logger.py
# ..\..\cmate\utils\logger.py
# src/utils/logger.py
import logging
import sys
from rich.logging import RichHandler

# --- Define a custom SUCCESS log level ---
SUCCESS_LEVEL = 25  # Place this between INFO (20) and WARNING (30)
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)

# Add the success method to the Logger class
logging.Logger.success = success

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

# ..\..\CodeMate\cmate\utils\prompt_templates.py
## File: ..\..\CodeMate\cmate\utils\prompt_templates.py

```py
# ..\..\CodeMate\cmate\utils\prompt_templates.py
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

# ..\..\CodeMate\cmate\utils\system_metrics.py
## File: ..\..\CodeMate\cmate\utils\system_metrics.py

```py
# ..\..\CodeMate\cmate\utils\system_metrics.py
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

# ..\..\CodeMate\cmate\utils\token_counter.py
## File: ..\..\CodeMate\cmate\utils\token_counter.py

```py
# ..\..\CodeMate\cmate\utils\token_counter.py
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

