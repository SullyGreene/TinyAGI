# MIT License
# Copyright (c) 2025 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/config.py

from rich.table import Table
from rich.console import Console
from rich import box

console = Console()

def run(config: dict):
    table = Table(title="Current Configuration", box=box.ROUNDED)
    table.add_column("Key", style="bold cyan")
    table.add_column("Value", style="bold yellow")

    for key, value in config.items():
        table.add_row(str(key), str(value))

    console.print(table)
