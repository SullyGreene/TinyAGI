# gemini_interaction.py
import argparse
import os
import sys
import logging

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import TinyAGI as agi
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_gemini_config():
    """
    Creates a configuration for the Gemini agent.
    """
    if not os.getenv('GEMINI_API_KEY'):
        raise ValueError("GEMINI_API_KEY not set in environment for Gemini agent")
    return {
        "name": "gemini_agent",
        "module": "gemini_agent",
        "class": "GeminiAgent",
        "source": "local",
        "config": {
            "generation_model": "gemini-1.5-flash-latest",
            "embedding_model": "text-embedding-004",
            "parameters": {"temperature": 0.7, "max_output_tokens": 500}
        }
    }

def run_interaction(prompt, system_prompt=None, test_type="generate"):
    """
    Initializes the selected agent and runs a specific interaction test.
    """
    agent_name = "gemini"
    console = Console()
    console.print(Panel(f"🚀 Initializing [bold cyan]{agent_name}_agent[/bold cyan] for a '[bold]{test_type}[/bold]' interaction...",
                        title="[bold green]TinyAGI Agent Interaction[/bold green]", border_style="green"))

    try:
        # Use AgentSystem to load and manage the agent
        agent_config = get_gemini_config()
        agent_system = agi.AgentSystem(agent_configs=[agent_config])
        agent = agent_system.agent_manager.get_agent("gemini_agent")

        if not agent:
            console.print("[bold red]Error:[/bold red] Failed to initialize Gemini agent.")
            return

        console.print(f"✅ [bold green]Agent '{agent.name}' initialized successfully.[/bold green]")
        console.print(Panel(f"[italic]'{prompt}'[/italic]", title="[bold]Input Prompt[/bold]", border_style="blue"))

        if test_type == "generate":
            with console.status("[bold yellow]Generating response...", spinner="dots"):
                response = agent.generate_text(prompt, system_prompt=system_prompt)
            console.print(Panel(Markdown(response), title="[bold]Agent Response[/bold]", border_style="green"))

        elif test_type == "stream":
            console.print(Panel("", title="[bold]Streaming Agent Response[/bold]", border_style="green", expand=False))
            full_response = ""
            with Live(console=console, auto_refresh=False) as live:
                response_stream = agent.generate_text(prompt, system_prompt=system_prompt, stream=True)
                for chunk in response_stream:
                    full_response += chunk
                    live.update(Markdown(full_response), refresh=True)

        elif test_type == "embed":
            with console.status("[bold yellow]Generating embedding...", spinner="dots"):
                embedding = agent.embed(prompt)
            if isinstance(embedding, list) and len(embedding) > 0:
                console.print(Panel(f"Generated embedding with {len(embedding)} dimensions.\n"
                                    f"Example: {embedding[:5]}...",
                                    title="[bold]Embedding Result[/bold]", border_style="green"))
            else:
                console.print(Panel("[yellow]Agent does not support embedding or returned an empty result.[/yellow]",
                                    title="[bold]Embedding Result[/bold]", border_style="yellow"))

    except Exception as e:
        logger.error(f"An error occurred during agent interaction: {e}", exc_info=True)
        console.print(f"[bold red]Error:[/bold red] {e}")

def main():
    """Main function to parse arguments and run the agent interaction."""
    parser = argparse.ArgumentParser(
        description="A TinyAGI script to interact with the Gemini agent.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-p", "--prompt", type=str, required=True,
        help="The prompt to send to the agent."
    )
    parser.add_argument(
        "-t", "--test-type", type=str, default="generate", choices=["generate", "stream", "embed"],
        help="The type of interaction to perform."
    )
    parser.add_argument(
        "-s", "--system-prompt", type=str, default=None,
        help="An optional system prompt to guide the agent's behavior."
    )
    args = parser.parse_args()

    run_interaction(args.prompt, args.system_prompt, args.test_type)

if __name__ == "__main__":
    main()