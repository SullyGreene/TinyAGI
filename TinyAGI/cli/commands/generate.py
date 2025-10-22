# MIT License
# Copyright (c) 2025 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/generate.py

from rich.prompt import Prompt
from rich.console import Console
from TinyAGI.agent import AgentSystem
import sys

console = Console()

def run(agent_system: AgentSystem):
    """Handles the 'generate' command in the interactive CLI."""
    try:
        # Let user choose an agent
        available_agents = list(agent_system.agent_manager.loaded_agents.keys())
        agent_name = Prompt.ask("[bold yellow]Which agent to use?[/bold yellow]", choices=available_agents, default=available_agents[0] if available_agents else None)
        
        agent = agent_system.agent_manager.get_agent(agent_name)
        if not agent:
            console.print(f"[bold red]Agent '{agent_name}' not found.[/bold red]")
            return

        user_prompt = Prompt.ask("[bold yellow]Enter the prompt[/bold yellow]")
        stream_response = Prompt.ask("[bold yellow]Stream output? (yes/no)[/bold yellow]", choices=["yes", "no"], default="no")
        
        if stream_response.lower() == "yes":
            with console.status("[bold green]Generating response...[/bold green]"):
                for chunk in agent.generate_text(user_prompt, stream=True):
                    console.out(chunk, end="")
            console.print() # for a newline
        else:
            with console.status("[bold green]Generating response...[/bold green]"):
                response = agent.generate_text(user_prompt, stream=False)
            console.print(f"\n[bold cyan]Response:[/bold cyan]\n{response}")

    except Exception as e:
        console.print(f"[bold red]Error generating text: {e}[/bold red]")
