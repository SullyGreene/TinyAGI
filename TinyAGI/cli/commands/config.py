# TinyAGI/cli/commands/config.py

from rich.console import Console
from rich.prompt import Prompt
from TinyAGI.agent import AgentSystem
from .base_command import BaseCommand

console = Console()

class ConfigCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "config"

    @property
    def description(self) -> str:
        return "⚙️  Configure session settings (e.g., system prompt)"

    def execute(self, agent_system: AgentSystem, args: list = None):
        """Handles the 'config' command to set session-wide settings."""
        if not hasattr(agent_system, 'session_config'):
            agent_system.session_config = {}

        new_system_prompt = Prompt.ask("[bold yellow]Enter new system prompt (leave blank to clear)[/bold yellow]", default=agent_system.session_config.get('system_prompt', ''))
        agent_system.session_config['system_prompt'] = new_system_prompt

        if new_system_prompt:
            console.print(f"[bold green]System prompt set to:[/bold green] '{new_system_prompt}'")
        else:
            console.print("[bold yellow]System prompt cleared.[/bold yellow]")