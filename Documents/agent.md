
# TinyAGI/agent.py

## Overview

The `agent.py` file defines the `AgentSystem` class, which orchestrates the interaction between agents, plugins, tools, and tasks within the TinyAGI framework.

## Functionality

- **Initialization**: Loads configurations, initializes managers for modules, agents, plugins, and tools, and sets up the task manager.
- **Execution**: Provides a `run` method to execute all configured tasks.

## Key Components

- **ModuleManager**: Manages loading and interaction with various modules.
- **AgentManager**: Handles the loading and management of different AI agents.
- **PluginManager**: Manages plugins that extend the system's capabilities.
- **ToolManager**: Integrates external tools like Wikipedia for enhanced functionalities.
- **TaskManager**: Executes predefined tasks using the loaded agents, plugins, and tools.

## Usage

Instantiate the `AgentSystem` with a configuration file and call the `run` method to execute tasks.

```python
from TinyAGI.agent import AgentSystem

def main():
    agent_system = AgentSystem(config_file='config/agent_config.json')
    agent_system.run()

if __name__ == '__main__':
    main()
```
