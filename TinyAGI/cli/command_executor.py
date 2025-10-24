# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/command_executor.py

from .command_manager import CommandManager

class CommandExecutor:
    def __init__(self, command_manager: CommandManager, agent_system):
        self.command_manager = command_manager
        self.agent_system = agent_system

    def execute_command(self, command_name: str, args: list = None):
        """Executes a CLI command."""
        command = self.command_manager.get_command(command_name)
        if command:
            return command.execute(self.agent_system, args)
        else:
            return f"Command '{command_name}' not found."
