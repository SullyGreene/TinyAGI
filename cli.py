#!/usr/bin/env python
# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# cli.py

import json
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from TinyAGI.services.cli_manager import run_cli
from TinyAGI.utils import setup_logging

console = Console()

def load_server_config(path='server_config.json'):
    """
    Load server configuration file to get parameters like agent config.
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error loading server configuration: {e}[/bold red]")
        return {}

def display_welcome():
    """
    Display a welcome message and show the available options to the user.
    """
    console.clear()
    console.print("[bold green]Welcome to the TinyAGI Interactive CLI![/bold green]")
    console.print("Use the commands below to interact with TinyAGI:")
    console.print("[bold yellow]generate[/bold yellow]: Generate text from a prompt")
    console.print("[bold yellow]config[/bold yellow]: Display current configuration")
    console.print("[bold yellow]exit[/bold yellow]: Exit the CLI")

def display_config(config):
    """
    Display the current configuration in a nice table format.
    """
    table = Table(title="Current Configuration", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    
    for key, value in config.items():
        table.add_row(str(key), str(value))
    
    console.print(table)

def run_cli_ui():
    """
    Start the interactive CLI UI for TinyAGI using rich for a styled terminal interface.
    """
    # Load the server config
    config = load_server_config()

    # Display the welcome message and options
    display_welcome()

    # Main CLI loop
    while True:
        # Interactive prompt for command selection
        user_command = Prompt.ask("Enter a command [bold green](generate, config, exit)[/bold green]", choices=["generate", "config", "exit"], default="generate")

        if user_command == "exit":
            console.print("[bold red]Exiting the TinyAGI CLI UI...[/bold red]")
            sys.exit(0)

        elif user_command == "generate":
            # For the generate command, ask for the prompt and stream flag
            user_prompt = Prompt.ask("[bold yellow]Enter the prompt text:[/bold yellow]")
            stream_flag = Prompt.ask("[bold yellow]Do you want to stream the output? (yes/no):[/bold yellow]").lower()
            stream_flag = stream_flag == 'yes'
            
            # Execute the generate command through the CLI manager
            try:
                # Pass arguments to the existing CLI manager
                args = {
                    'command': 'generate',
                    'prompt': user_prompt,
                    'config': config.get('agent_config_file', 'config/agent_config.json'),
                    'stream': stream_flag
                }
                run_cli(args, config.get('agent_config_file', 'config/agent_config.json'))
                
            except Exception as e:
                console.print(f"[bold red]Error during generation: {e}[/bold red]")

        elif user_command == "config":
            # Display current config settings
            display_config(config)

        else:
            console.print(f"[bold red]Unknown command: {user_command}[/bold red]")
            continue

if __name__ == '__main__':
    run_cli_ui()
