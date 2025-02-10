# src/cmate/main.py
import sys
import os
import asyncio
import logging
from pathlib import Path
import yaml
import typer
from rich.console import Console
from rich.logging import RichHandler
from typing import Optional, Dict, Any

from cmate.core.agent_coordinator import AgentCoordinator, AgentConfig
from cmate.core.state_manager import StateManager
from cmate.core.workflow_manager import WorkflowManager
from cmate.utils.logger import setup_logging
from cmate.utils.config import load_config
from cmate.interfaces.cli_interface import CLIInterface

app = typer.Typer(help="Semi-Autonomous Agent Assistant (CodeMate)")
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
            asyncio.run(cli.start())
        else:
            console.print("[green]Agent started in non-interactive mode[/green]")
            asyncio.run(agent.check_status())
    except Exception as e:
        console.print(f"[red]Error starting system: {str(e)}[/red]")
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
        else:
            console.print("[red]Error processing request[/red]")
            console.print(result)
    except Exception as e:
        console.print(f"[red]Error processing request: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def status(
    config: str = typer.Option(None, "--config", "-c", help="Path to configuration file")
):
    """Check agent status."""
    try:
        agent = setup_system(config)
        status = asyncio.run(agent.check_status())
        console.print("\n[bold]Agent Status[/bold]")
        console.print(f"State: {status['state']}")
        console.print(f"Active Workflow: {status['active_workflow']}")
        console.print("\n[bold]Metrics:[/bold]")
        for key, value in status["metrics"].items():
            console.print(f"{key}: {value}")
    except Exception as e:
        console.print(f"[red]Error checking status: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
