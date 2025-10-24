# TinyAGI/cli/commands/generate.py

from rich.prompt import Prompt
from rich.console import Console
from TinyAGI.agent import AgentSystem
from .base_command import BaseCommand

console = Console()

class GenerateCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "generate"

    @property
    def description(self) -> str:
        return ":brain: Generate text from a prompt"

    def execute(self, agent_system: AgentSystem, args: list = None):
        """Handles the 'generate' command in the interactive CLI."""
        try:
            available_agents = list(agent_system.agent_manager.loaded_agents.keys())
            if not available_agents:
                console.print("[bold red]No agents available. Please check your configuration.[/bold red]")
                return

            agent_name = Prompt.ask("[bold yellow]Which agent to use?[/bold yellow]", choices=available_agents, default=available_agents[0])
            agent = agent_system.agent_manager.get_agent(agent_name)

            user_prompt = Prompt.ask("[bold yellow]Enter the prompt[/bold yellow]")
            stream_response = Prompt.ask("[bold yellow]Stream output? (yes/no)[/bold yellow]", choices=["yes", "no"], default="no")

            # Get system prompt from session_config if it exists
            system_prompt = getattr(agent_system, 'session_config', {}).get('system_prompt')
            if system_prompt:
                console.print(f"[dim]Using system prompt: '{system_prompt}'[/dim]")

            generation_kwargs = {'stream': stream_response.lower() == "yes"}
            if system_prompt:
                generation_kwargs['system_prompt'] = system_prompt

            if stream_response.lower() == "yes":
                with console.status("[bold green]Generating response...[/bold green]"):
                    for chunk in agent.generate_text(user_prompt, **generation_kwargs):
                        console.out(chunk, end="")
                console.print()  # for a newline
            else:
                with console.status("[bold green]Generating response...[/bold green]"):
                    response = agent.generate_text(user_prompt, **generation_kwargs)
                console.print(f"\n[bold cyan]Response:[/bold cyan]\n{response}")

        except Exception as e:
            console.print(f"[bold red]Error generating text: {e}[/bold red]")
