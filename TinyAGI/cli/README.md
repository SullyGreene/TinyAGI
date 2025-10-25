# TinyAGI CLI

## Overview

The TinyAGI framework includes a powerful and user-friendly Command-Line Interface (CLI) for interacting with the system. Built with `rich` and `argparse`, the CLI supports both an interactive shell and direct command execution.

## How to Run

### Interactive Mode

To start the interactive CLI, run the following command from the root of the project:

```bash
poetry run cli
```

This will launch the interactive shell, displaying a welcome message and a table of available commands.

## Available Commands

The interactive CLI supports the following commands:

| Command    | Description                        | 
|------------|------------------------------------|
| `run`      | Execute the task pipeline from config. |
| `chat`     | Start an interactive chat session. |
| `generate` | Generate text from a prompt.       |
| `config`   | Display the agent configuration.   |
| `agents`   | List all available AI agents.      |
| `plugins`  | List all available plugins.        |
| `tools`    | List all available tools.          |
| `help`     | Show the command help table again. |
| `clear`    | Clear the console screen.          |
| `exit`     | Exit the CLI.                      |

## Structure

The CLI is modular, with each command implemented in its own file within the `TinyAGI/cli/commands/` directory. The main user interface logic is handled by `TinyAGI/cli/ui.py`, which is responsible for the command prompt and displaying the rich output.