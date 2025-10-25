# TinyAGI Agents

## Overview

The `agents` directory contains the core logic for different AI agents that can be used within the TinyAGI framework. Each agent is a self-contained module responsible for interacting with a specific AI model or service, such as OpenAI, Ollama, or Gemini.

## Agent Manager

The `agent_manager.py` is responsible for discovering, loading, and managing all available agents. It reads the agent configurations from the main `config.json` and can dynamically load agents from:
- **Local:** Agents defined as Python modules within this directory.
- **GitHub:** Agents from remote Git repositories, which are cloned on the fly.

## Creating a New Agent

To add a new agent, you need to:
1.  Create a new Python file in this directory (e.g., `my_agent.py`).
2.  Inside the file, define a class that inherits from a base agent class (if one exists) or implements the required methods (e.g., `generate`, `chat`).
3.  The agent's `__init__` method should accept `config` and `module_manager` arguments.
4.  Add a new entry to the `agents` list in your `config.json` file, specifying the `name`, `module`, `class`, and any `config` required for your new agent.

This modular approach allows for easy extension of TinyAGI's capabilities with new and custom AI models.

## Programmatic Usage

While agents are typically used within tasks, you can also interact with them directly through the `AgentSystem` for quick tests or simple interactions.

```python
import TinyAGI as agi

def main():
    # Initialize the system
    agent_system = agi.AgentSystem(config_files='config/agent_config.json')

    # Get a specific agent and chat with it
    response = agent_system.chat("Hello, who are you?")
    print(response)

if __name__ == '__main__':
    main()
```