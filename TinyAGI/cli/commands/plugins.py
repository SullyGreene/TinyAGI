# TinyAGI/cli/commands/plugins.py

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
    """Displays a table of available plugins."""
    agent_config = load_agent_config()
    if not agent_config or 'plugins' not in agent_config:
        console.print("[yellow]No plugins found in configuration.[/yellow]")
        return

    table = Table(title="🔌 Available Plugins", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="bold cyan")
    table.add_column("Module", style="green")
    table.add_column("Source", style="green")
    table.add_column("Config", style="yellow")

    for plugin in agent_config['plugins']:
        config_str = json.dumps(plugin.get('config', {}), indent=2)
        table.add_row(
            plugin.get('name'),
            plugin.get('module'),
            plugin.get('source'),
            config_str
        )

    console.print(table)
