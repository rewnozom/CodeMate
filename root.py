#!/usr/bin/env python3
import typer
from cmate.interfaces.cli_interface import CLI
from cmate.utils.logger import setup_logging

app = typer.Typer()
cli = CLI()

@app.command()
def start():
    """Start the CodeMate interactive session."""
    setup_logging()
    cli.start_interactive_session()

if __name__ == "__main__":
    app()