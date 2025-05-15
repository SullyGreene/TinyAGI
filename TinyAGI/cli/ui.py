# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/ui.py

from rich.console import Console
from rich.prompt import Prompt
from TinyAGI.cli.commands import config as config_cmd
from TinyAGI.cli.commands import generate as generate_cmd
from TinyAGI.cli.commands import exit as exit_cmd
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
    console.clear()
    console.print("[bold green]Welcome to the TinyAGI Interactive CLI![/bold green]")
    console.print("Use the commands below to interact with TinyAGI:")
    console.print("[bold yellow]generate[/bold yellow]: Generate text from a prompt")
    console.print("[bold yellow]config[/bold yellow]: Display current configuration")
    console.print("[bold yellow]exit[/bold yellow]: Exit the CLI\n")

def run_cli_ui():
    config = load_server_config()
    display_welcome()

    while True:
        try:
            command = Prompt.ask(
                "[bold green]Enter a command[/bold green]",
                choices=["generate", "config", "exit"],
                default="generate"
            )

            if command == "config":
                config_cmd.run(config)
            elif command == "generate":
                generate_cmd.run(config)
            elif command == "exit":
                exit_cmd.run()
        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted by user. Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")
