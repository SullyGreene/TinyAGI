# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/cli/commands/chat.py

from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from TinyAGI.agent import AgentSystem

console = Console()

def run(agent_system: AgentSystem):
    """Handles the 'chat' command in the interactive CLI for a continuous conversation."""
    try:
        available_agents = list(agent_system.agent_manager.loaded_agents.keys())
        if not available_agents:
            console.print("[bold red]No agents available to chat with.[/bold red]")
            return

        agent_name = Prompt.ask(
            "[bold yellow]Which agent to chat with?[/bold yellow]",
            choices=available_agents,
            default=available_agents[0]
        )

        agent = agent_system.agent_manager.get_agent(agent_name)
        if not agent:
            console.print(f"[bold red]Agent '{agent_name}' not found.[/bold red]")
            return

        console.print(f"\n[bold green]Starting chat with {agent_name}. Type 'exit' or 'quit' to end the session.[/bold green]\n")
        messages = []

        while True:
            user_input = Prompt.ask(Text.from_markup("[bold cyan]You[/bold cyan]"))

            if user_input.lower() in ['exit', 'quit']:
                console.print("[bold yellow]Ending chat session.[/bold yellow]")
                break

            messages.append({"role": "user", "content": user_input})
            prompt = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages]) + "\nAssistant:"

            console.out(Text.from_markup(f"[bold magenta]Assistant[/bold magenta]: "), end="")
            
            response_stream = agent.generate_text(prompt, stream=True)
            if response_stream:
                full_response = ""
                for chunk in response_stream:
                    console.out(chunk, end="")
                    full_response += chunk
                console.print()  # for a newline
                messages.append({"role": "assistant", "content": full_response})
            else:
                console.print("[bold red]Agent failed to generate a response.[/bold red]")

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Ending chat session.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]An error occurred during chat: {e}[/bold red]")