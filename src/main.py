# src/main.py

import sys
import os

# Hitta projektets root directory och lägg till det i sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))  # Platsen för main.py
project_root = os.path.abspath(os.path.join(current_dir, ".."))  # Gå en nivå upp till "src"

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
import typer
from rich.console import Console
from rich.logging import RichHandler

from core.agent_coordinator import AgentCoordinator, AgentConfig
from core.state_manager import StateManager
from core.workflow_manager import WorkflowManager
from utils.logger import setup_logging
from utils.config import load_config
from interfaces.cli_interface import CLIInterface

# Initialize Typer app
app = typer.Typer(help="Semi-Autonomous Agent Assistant")
console = Console()

def setup_system(config_path: Optional[str] = None) -> AgentCoordinator:
    """Setup and initialize system components"""
    # Load configuration
    config = load_config(config_path)
    
    # Setup logging
    setup_logging(
        log_level=config.get("general", {}).get("log_level", "INFO"),
        log_file=Path("logs/agent.log")
    )
    
    # Create agent configuration
    agent_config = AgentConfig(
        workspace_path=config.get("general", {}).get("workspace_path", "./Workspace"),
        max_files_per_scan=config.get("general", {}).get("max_files_per_scan", 10),
        context_window_size=config.get("llm", {}).get("context_window", 60000),
        auto_test=config.get("agent", {}).get("auto_test", True),
        debug_mode=config.get("general", {}).get("debug_mode", False)
    )
    
    # Initialize components
    state_manager = StateManager()
    workflow_manager = WorkflowManager()
    
    # Create agent coordinator
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
    """Start the agent system"""
    try:
        # Setup system
        agent = setup_system(config)
        
        if interactive:
            # Start CLI interface
            cli = CLIInterface(agent)
            asyncio.run(cli.start())
        else:
            # Wait for agent to be ready
            console.print("[green]Agent started in non-interactive mode[/green]")
            asyncio.run(agent_ready_check(agent))
            
    except Exception as e:
        console.print(f"[red]Error starting system: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def process(
    request: str = typer.Argument(..., help="Request to process"),
    config: str = typer.Option(None, "--config", "-c", help="Path to configuration file")
):
    """Process a single request"""
    try:
        # Setup system
        agent = setup_system(config)
        
        # Process request
        result = asyncio.run(agent.process_request({
            "type": "process",
            "request": request
        }))
        
        if result["success"]:
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
    """Check agent status"""
    try:
        # Setup system
        agent = setup_system(config)
        
        # Get status
        status = asyncio.run(agent.check_status())
        
        console.print("\n[bold]Agent Status[/bold]")
        console.print(f"State: {status['state']}")
        console.print(f"Active Workflow: {status['active_workflow']}")
        console.print("\n[bold]Metrics:[/bold]")
        for key, value in status['metrics'].items():
            console.print(f"{key}: {value}")
            
    except Exception as e:
        console.print(f"[red]Error checking status: {str(e)}[/red]")
        raise typer.Exit(1)

async def agent_ready_check(agent: AgentCoordinator) -> None:
    """Check if agent is ready"""
    try:
        status = await agent.check_status()
        if status["state"] == "idle":
            console.print("[green]Agent ready[/green]")
        else:
            console.print(f"[yellow]Agent in state: {status['state']}[/yellow]")
    except Exception as e:
        console.print(f"[red]Error checking agent status: {str(e)}[/red]")

if __name__ == "__main__":
    app()
