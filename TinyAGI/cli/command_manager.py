# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/command_manager.py

import os
import importlib
import inspect
from rich.console import Console
from .commands.base_command import BaseCommand

console = Console()

class CommandManager:
    """Dynamically loads and manages CLI commands."""

    def __init__(self, commands_dir="TinyAGI/cli/commands"):
        self._commands = {}
        self._load_commands(commands_dir)

    def _load_commands(self, commands_dir):
        """Scans the commands directory and loads all command classes."""
        for filename in os.listdir(commands_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module_path = f"{commands_dir.replace('/', '.')}.{module_name}"
                try:
                    module = importlib.import_module(module_path)
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj is not BaseCommand:
                            command_instance = obj()
                            self._commands[command_instance.name] = command_instance
                except Exception as e:
                    console.print(f"[bold red]Failed to load command from {filename}: {e}[/bold red]")

    def get_command(self, name):
        """Retrieves a command by its name."""
        return self._commands.get(name)

    def get_commands(self):
        """Returns a dictionary of all loaded commands."""
        return self._commands