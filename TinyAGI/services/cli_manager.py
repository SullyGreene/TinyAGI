# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/services/cli_manager.py

import argparse
import sys
import logging
from ..agent import AgentSystem
from ..utils import setup_logging
from ..cli.ui import run_cli_ui

logger = logging.getLogger(__name__)

def handle_direct_command(args):
    """Handles direct command execution from the command line."""
    setup_logging()
    config_file = args.config if args.config else 'config/agent_config.json'
    
    try:
        agent_system = AgentSystem(config_files=config_file)
    except ValueError as e:
        logger.error(f"Failed to initialize AgentSystem: {e}")
        sys.exit(1)

    if args.command == 'generate':
        try:
            # Use the default agent for direct generation
            agent = agent_system.agent_manager.get_agent(args.agent)
            if not agent:
                logger.error(f"Agent '{args.agent}' not found.")
                sys.exit(1)
            
            response = agent.generate_text(args.prompt, stream=args.stream)
            if args.stream:
                for chunk in response:
                    print(chunk, end='', flush=True)
                print()
            else:
                print(response)
        except Exception as e:
            logger.error(f"Error during generation: {e}")
            sys.exit(1)
    elif args.command == 'run':
        try:
            agent_system.run()
        except Exception as e:
            logger.error(f"Error during task execution: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='TinyAGI CLI. Runs in interactive mode if no command is provided.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate command
    parser_generate = subparsers.add_parser('generate', help='Generate text from a prompt.')
    parser_generate.add_argument('prompt', help='The prompt to generate text from.')
    parser_generate.add_argument('--agent', '-a', default='ollama_agent', help='The agent to use for generation.')
    parser_generate.add_argument('--config', '-c', help='Path to a custom config file.')
    parser_generate.add_argument('--stream', '-s', action='store_true', help='Stream the output.')

    # Run command
    parser_run = subparsers.add_parser('run', help='Run tasks defined in the config file.')
    parser_run.add_argument('--config', '-c', help='Path to a custom config file.')

    # Parse arguments. If no command is given, sys.argv will be short.
    if len(sys.argv) == 1:
        # No command provided, start interactive UI
        run_cli_ui()
    else:
        # Command provided, parse args and handle it
        args = parser.parse_args()
        handle_direct_command(args)

def run_cli():
    """
    Run the CLI manager.
    """
    main()


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
