# ..\..\cmate\__main__.py
#!/usr/bin/env python
"""
Entry point for CodeMate – Your AI-Powered Code Assistant.

This module sets up the system and launches the interactive CLI via Typer.
It also integrates the HTML logging handler so that every run automatically
generates a visual HTML report summarizing all steps, prompts, responses, and errors.
"""

import sys
import os
import asyncio
import logging
from pathlib import Path
import yaml
import typer
from rich.console import Console
from rich.logging import RichHandler
from typing import Optional
from datetime import datetime
import atexit

# ----------------------------------------------------------
# Ensure the project root is in sys.path
# ----------------------------------------------------------
script_dir = Path(__file__).parent.resolve()    # This is the 'cmate' directory.
project_root = script_dir.parent                 # Parent of 'cmate' is the project root.
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
# Optionally, change the current working directory to project root:
# os.chdir(project_root)

# -------------------------------------------
# Now import your internal modules
# -------------------------------------------
from cmate.core.agent_coordinator import AgentCoordinator, AgentConfig
from cmate.core.state_manager import StateManager
from cmate.core.workflow_manager import WorkflowManager
from cmate.utils.logger import setup_logging
from cmate.utils.config import load_config
from cmate.interfaces.cli_interface import CLIInterface

# -------------------------------
# Import the new HTML logging handler
# -------------------------------
from cmate.utils.html_logger import HTMLLogHandler

# Load configuration and set up basic logging
config = load_config()
log_level = config.get("general", {}).get("log_level", "INFO")
setup_logging(log_level, log_file=str(Path("logs") / "agent.log"))

# Create and attach the HTML logging handler to the root logger
html_handler = HTMLLogHandler(log_dir="logs")
logging.getLogger().addHandler(html_handler)
atexit.register(html_handler.close)  # Ensure the HTML log is closed on exit

logger = logging.getLogger("run_main")
logger.info("Starting CodeMate...")
logger.success("CodeMate startup sequence initiated successfully.")

app = typer.Typer(help="CodeMate - Your AI-Powered Code Assistant")
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
    logger.success("System components initialized successfully.")
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
            # Start the interactive CLI loop using cmdloop()
            cli.cmdloop()
        else:
            console.print("[green]Agent started in non-interactive mode[/green]")
            asyncio.run(agent.check_status())
        logger.success("Agent system started successfully.")
    except Exception as e:
        console.print(f"[red]Error starting system: {str(e)}[/red]")
        logger.error("Error starting system: %s", str(e))
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
            logger.success("Request processed successfully: %s", result)
        else:
            console.print("[red]Error processing request[/red]")
            console.print(result)
            logger.error("Error processing request: %s", result)
    except Exception as e:
        console.print(f"[red]Error processing request: {str(e)}[/red]")
        logger.error("Error processing request: %s", str(e))
        raise typer.Exit(1)

@app.command()
def status(
    config: str = typer.Option(None, "--config", "-c", help="Path to configuration file")
):
    """Check agent status."""
    try:
        agent = setup_system(config)
        status = asyncio.run(agent.check_status())
        console.print("\nAgent Status:")
        console.print(f"State: {status['state']}")
        console.print(f"Active Workflow: {status['active_workflow']}")
        console.print("\nMetrics:")
        for key, value in status["metrics"].items():
            console.print(f"{key}: {value}")
        logger.success("Agent status checked successfully.")
    except Exception as e:
        console.print(f"[red]Error checking status: {str(e)}[/red]")
        logger.error("Error checking status: %s", str(e))
        raise typer.Exit(1)

def main():
    """
    Main entry point called by 'python -m cmate' or 'cmate' console script.
    """
    app()

if __name__ == "__main__":
    main()
