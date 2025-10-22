
# TinyAGI/agents/agent_manager.py

## Overview

The `agent_manager.py` file defines the `AgentManager` class, which handles the loading, management, and retrieval of AI agents within the TinyAGI framework.

## Functionality

- **Agent Loading**: Loads agents based on configuration, supporting both local and GitHub sources.
- **Dynamic Management**: Allows adding and removing agents at runtime.
- **Error Handling**: Logs any issues encountered during agent loading and management.

## Key Components

- **load_agents**: Processes the agent configurations and initializes each agent.
- **load_agent_from_github**: Clones agent repositories from GitHub if specified.
- **get_agent**: Retrieves a loaded agent by name.
- **add_agent / remove_agent**: Dynamically manages agents within the system.

## Usage

Agents are defined in the configuration file and managed through the `AgentManager`.

```python
from TinyAGI.agents.agent_manager import AgentManager

agent_manager = AgentManager(agents_config, module_manager)
agent = agent_manager.get_agent('default_agent')
agent.generate_text("Hello, world!")
```
