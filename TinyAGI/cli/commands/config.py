# TinyAGI/cli/commands/config.py

import json
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

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

def create_section_table(title: str, items: list) -> Table:
    """Creates a rich Table for a section of the config."""
    table = Table(title=title, show_header=True, header_style="bold blue", expand=True)
    if not items:
        return table

    # Dynamically create columns based on keys of the first item
    headers = items[0].keys()
    for header in headers:
        table.add_column(header.capitalize(), style="cyan" if header != "name" else "bold cyan")

    for item in items:
        row = []
        for header in headers:
            value = item.get(header)
            if isinstance(value, dict):
                # Pretty print dicts
                row.append(json.dumps(value, indent=2))
            else:
                row.append(str(value))
        table.add_row(*row)
    
    return table

def run(config: dict):
    """Displays the agent configuration in a structured format."""
    agent_config = load_agent_config()
    if not agent_config:
        return

    console.print(Panel(Text("Agent Configuration", justify="center", style="bold green")))

    # Create tables for each main section
    agents_table = create_section_table("🤖 Agents", agent_config.get('agents', []))
    plugins_table = create_section_table("🔌 Plugins", agent_config.get('plugins', []))
    tools_table = create_section_table("🛠️ Tools", agent_config.get('tools', []))
    
    console.print(agents_table)
    console.print(plugins_table)
    console.print(tools_table)