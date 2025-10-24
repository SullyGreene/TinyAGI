# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/base_command.py

from abc import ABC, abstractmethod
from TinyAGI.agent import AgentSystem

class BaseCommand(ABC):
    """Abstract base class for all CLI commands."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def execute(self, agent_system: AgentSystem, args: list = None): ...