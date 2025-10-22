# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/ui.py

from rich.console import Console, Group
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from TinyAGI.cli.commands import config as config_cmd
from TinyAGI.cli.commands import generate as generate_cmd
from TinyAGI.cli.commands import exit as exit_cmd
from TinyAGI.cli.commands import chat as chat_cmd
from TinyAGI.cli.commands import agents as agents_cmd
from TinyAGI.cli.commands import run as run_cmd
from TinyAGI.cli.commands import plugins as plugins_cmd
from TinyAGI.cli.commands import tools as tools_cmd
from TinyAGI.agent import AgentSystem
import json

console = Console()

def load_server_config(path='server_config.json'):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error loading config: {e}[/bold red]")
        return {}

def display_welcome():
    """Displays a rich, styled welcome message and command table."""
    console.clear()

    title = Text("Welcome to the TinyAGI Interactive CLI!", justify="center", style="bold green")
    subtitle = Text("Your AI-powered command-line assistant.", justify="center", style="italic cyan")

    command_table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
    command_table.add_column("Command", style="dim", width=12)
    command_table.add_column("Description", style="cyan")

    command_table.add_row("run", ":rocket: Execute the task pipeline from config")
    command_table.add_row("chat", ":speech_balloon: Start an interactive chat session")
    command_table.add_row("generate", ":brain: Generate text from a prompt")
    command_table.add_row("config", ":gear: Display current configuration")
    command_table.add_row("agents", ":robot: List available AI agents")
    command_table.add_row("plugins", ":electric_plug: List available plugins")
    command_table.add_row("tools", ":hammer_and_wrench: List available tools")
    command_table.add_row("help", ":question: Show this help message again")
    command_table.add_row("clear", ":broom: Clear the console screen")
    command_table.add_row("exit", ":door: Exit the CLI")

    welcome_group = Group(
        Text.assemble(title, "\n", subtitle),
        "\n",
        command_table
    )

    welcome_panel = Panel(
        welcome_group,
        border_style="green",
        padding=(1, 2)
    )
    console.print(welcome_panel)

def run_cli_ui():
    try:
        # Initialize AgentSystem once
        agent_system = AgentSystem(config_files='config/agent_config.json')
        console.print("[bold green]AgentSystem initialized successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Fatal Error: Could not initialize AgentSystem: {e}[/bold red]")
        return
    display_welcome()

    while True:
        try:
            command = Prompt.ask(
                Text.from_markup("[bold green] :comet: Enter a command[/bold green]"),
                choices=["run", "chat", "generate", "config", "agents", "plugins", "tools", "help", "clear", "exit"],
                default="generate"
            )

            if command == "run":
                run_cmd.run(agent_system)
            elif command == "chat":
                chat_cmd.run(agent_system)
            elif command == "config":
                config_cmd.run(agent_system.config)
            elif command == "generate":
                generate_cmd.run(agent_system)
            elif command == "agents":
                agents_cmd.run(agent_system)
            elif command == "plugins":
                plugins_cmd.run(agent_system)
            elif command == "tools":
                tools_cmd.run(agent_system)
            elif command == "help":
                display_welcome()
            elif command == "clear":
                console.clear()
            elif command == "exit":
                exit_cmd.run()
        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted by user. Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")
