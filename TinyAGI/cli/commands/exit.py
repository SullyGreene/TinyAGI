# MIT License
# Copyright (c) 2025 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/exit.py

import sys
from rich.console import Console

console = Console()

def run():
    console.print("[bold green]Thank you for using TinyAGI CLI![/bold green]")
    sys.exit(0)
