# TinyAGI/cli/commands/tools.py

import json
from rich.console import Console
from rich.table import Table

console = Console()

def load_agent_config(path='config/agent_config.json'):
    """Loads the agent configuration file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"[bold red]Error: Agent configuration file not found at '{path}'[/bold red]")
        return None
    except json.JSONDecodeError:
        console.print(f"[bold red]Error: Could not decode JSON from '{path}'[/bold red]")
        return None

def run():
    """Displays a table of available tools."""
    agent_config = load_agent_config()
    if not agent_config or 'tools' not in agent_config:
        console.print("[yellow]No tools found in configuration.[/yellow]")
        return

    table = Table(title="🛠️ Available Tools", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="bold cyan")
    table.add_column("Module", style="green")
    table.add_column("Class", style="green")
    table.add_column("Config", style="yellow")

    for tool in agent_config['tools']:
        config_str = json.dumps(tool.get('config', {}), indent=2)
        table.add_row(
            tool.get('name'),
            tool.get('module'),
            tool.get('class'),
            config_str
        )

    console.print(table)
