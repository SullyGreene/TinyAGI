import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from .commands import chat, generate, config, exit_cli

class CLI:
    """
    The main application class for the TinyAGI interactive CLI.
    """
    def __init__(self):
        self.console = Console()
        self.commands = {
            "chat": chat.run,
            "generate": generate.run,
            "config": config.run,
            "help": self.show_help,
            "exit": exit_cli.run,
        }

    def show_welcome_message(self):
        """Displays the welcome panel."""
        welcome_panel = Panel(
            Text(
                "Welcome to the TinyAGI Interactive CLI!\n"
                "Type 'help' to see a list of available commands.",
                justify="center"
            ),
            title="[bold blue]🧠 TinyAGI[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(welcome_panel)

    def show_help(self):
        """Displays the help table with all available commands."""
        table = Table(title="[bold]Available Commands[/bold]", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="dim", width=12)
        table.add_column("Description")

        table.add_row("chat", "Start an interactive chat session with an agent.")
        table.add_row("generate", "Generate text from a single prompt.")
        table.add_row("config", "Display the current agent configuration.")
        table.add_row("help", "Show this help message.")
        table.add_row("exit", "Exit the TinyAGI CLI.")

        self.console.print(table)

    def run(self):
        """
        The main loop for the CLI.
        """
        self.show_welcome_message()
        try:
            while True:
                command_input = Prompt.ask("[bold green]TinyAGI>[/bold green]").strip()
                if not command_input:
                    continue

                parts = command_input.split()
                command_name = parts[0].lower()
                args = parts[1:]

                command = self.commands.get(command_name)

                if command:
                    try:
                        # Pass console and args to the command runner
                        command(console=self.console, args=args)
                    except Exception as e:
                        self.console.print(f"[bold red]Error executing command '{command_name}':[/bold red] {e}")
                else:
                    self.console.print(f"[bold red]Unknown command:[/] '{command_name}'. Type 'help' for a list of commands.")

        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Exiting TinyAGI CLI. Goodbye![/bold yellow]")
            sys.exit(0)