# MIT License
# Copyright (c) 2025 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/generate.py

from rich.prompt import Prompt
from rich.console import Console
from TinyAGI.services.cli_manager import run_cli

console = Console()

def run(config):
    user_prompt = Prompt.ask("[bold yellow]Enter the prompt:[/bold yellow]")
    stream = Prompt.ask("[bold yellow]Stream output? (yes/no):[/bold yellow]", choices=["yes", "no"], default="no")
    stream = stream.lower() == "yes"

    try:
        args = {
            'command': 'generate',
            'prompt': user_prompt,
            'config': config.get('agent_config_file', 'config/agent_config.json'),
            'stream': stream
        }
        run_cli(args, args['config'])
    except Exception as e:
        console.print(f"[bold red]Error generating text: {e}[/bold red]")
