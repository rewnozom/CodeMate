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
