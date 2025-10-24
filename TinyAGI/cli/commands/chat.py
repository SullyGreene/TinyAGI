# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/chat.py

from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from TinyAGI.agent import AgentSystem
from .base_command import BaseCommand

console = Console()

class ChatCommand(BaseCommand):
    """Command to interact with the agent in a chat-like manner."""

    @property
    def name(self) -> str:
        return "chat"

    @property
    def description(self) -> str:
        return "Chat with the agent."

    def execute(self, agent_system: AgentSystem, args: list = None):
        """The main chat loop."""
        if not args:
            console.print("[bold green]Starting chat session. Type 'exit' to end.[/bold green]")
            while True:
                try:
                    prompt = Prompt.ask("[bold cyan]You[/bold cyan]")
                    if prompt.lower() == "exit":
                        break
                    
                    response = agent_system.chat(prompt)
                    console.print(Markdown(response))

                except KeyboardInterrupt:
                    console.print("\n[bold red]Exiting chat session.[/bold red]")
                    break
        else:
            prompt = " ".join(args)
            response = agent_system.chat(prompt)
            console.print(Markdown(response))
