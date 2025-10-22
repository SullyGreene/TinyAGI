# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/run.py

from rich.console import Console
from TinyAGI.agent import AgentSystem

console = Console()

def run(agent_system: AgentSystem):
    """Handles the 'run' command in the interactive CLI, executing all configured tasks."""
    console.print("[bold green]Executing task pipeline from configuration...[/bold green]")
    try:
        agent_system.run()
        console.print("\n[bold green]✅ Task pipeline execution finished.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error during task execution: {e}[/bold red]")