# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/ui.py

import sys
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from TinyAGI.agent import AgentSystem
from .command_manager import CommandManager

console = Console()

class CLI:
    def __init__(self):
        """Initializes the CLI, loading commands and the agent system."""
        self.command_manager = CommandManager()
        self.agent_system = self._initialize_agent_system()

    def _initialize_agent_system(self):
        """Initializes the AgentSystem and handles potential errors."""
        try:
            console.print("[dim]Initializing AgentSystem...[/dim]")
            agent_system = AgentSystem(config_files='config/agent_config.json')
            console.print("[bold green]AgentSystem initialized successfully.[/bold green]")
            return agent_system
        except Exception as e:
            console.print(f"[bold red]Fatal Error: Could not initialize AgentSystem: {e}[/bold red]")
            console.print("[bold yellow]Please ensure 'config/agent_config.json' is correctly configured.[/bold yellow]")
            sys.exit(1)

    def display_welcome(self):
        """Displays a rich, styled welcome message and command table."""
        console.clear()

        title = Text("Welcome to the TinyAGI Interactive CLI!", justify="center", style="bold green")
        subtitle = Text("Your AI-powered command-line assistant.", justify="center", style="italic cyan")

        command_table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
        command_table.add_column("Command", style="dim", width=12)
        command_table.add_column("Description", style="cyan")

        # Dynamically build the help table from loaded commands
        for name, cmd in sorted(self.command_manager.get_commands().items()):
            command_table.add_row(name, cmd.description)

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

    def run_loop(self):
        """The main interactive loop for the CLI."""
        if not self.agent_system:
            return # Do not start the loop if AgentSystem failed to initialize

        self.display_welcome()
        command_names = sorted(self.command_manager.get_commands().keys())

        while True:
            try:
                user_input = Prompt.ask(
                    Text.from_markup("[bold green] :comet: Enter a command or chat[/bold green]")
                )

                if not user_input:
                    continue

                command_name, *args = user_input.split()

                if command_name in self.command_manager.get_commands():
                    if command_name == "help":
                        self.display_welcome()
                        continue
                    if command_name == "clear":
                        console.clear()
                        continue
                    if command_name == "exit":
                        console.print("[bold yellow]Exiting... Goodbye![/bold yellow]")
                        break
                    
                    command = self.command_manager.get_command(command_name)
                    if command:
                        command.execute(self.agent_system, args)
                else:
                    # If not a command, treat it as a chat prompt
                    response = self.agent_system.chat(user_input)
                    console.print(Markdown(response))


            except KeyboardInterrupt:
                console.print("\n[bold red]Interrupted by user. Exiting...[/bold red]")
                break
            except Exception as e:
                console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

def run_cli_ui():
    """Entry point to run the CLI UI."""
    cli_app = CLI()
    cli_app.run_loop()
