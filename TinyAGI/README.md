# TinyAGI Package Documentation

## Overview

This document provides an overview of the core components within the `TinyAGI` Python package. The framework is designed to be modular, allowing for easy extension and management of AI agents, plugins, tools, and tasks.

---

### `agent.py` - The `AgentSystem`

The `agent.py` file defines the `AgentSystem` class, which is the central orchestrator of the TinyAGI framework.

#### Key Responsibilities:
- **Initialization**: On creation, it loads configurations and initializes managers for agents, plugins, tools, and modules.
- **Task Execution**: It provides a `run()` method that kicks off the `TaskManager` to execute all tasks defined in the configuration.
- **Chat Interface**: It offers a `chat()` method for direct, interactive conversations with a specified agent.

#### Core Components:
- **AgentManager**: Manages the lifecycle of different AI agents (e.g., Ollama, Gemini).
- **PluginManager**: Manages plugins that define specific actions or workflows.
- **ToolManager**: Manages tools that provide agents with external capabilities (e.g., Wikipedia search).
- **ModuleManager**: Manages shared, reusable components.
- **TaskManager**: Executes the pipeline of tasks using the loaded agents, plugins, and tools.

#### Programmatic Usage

To use TinyAGI in your own project, you instantiate the `AgentSystem` and call its `run()` method.

```python
import TinyAGI as agi
import os

def main():
    # Path to your configuration file
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'agent_config.json')
    
    # Initialize and run the agent system
    agent_system = agi.AgentSystem(config_files=config_path)
    agent_system.run()

if __name__ == '__main__':
    main()
```

---

### `task_manager.py` - The `TaskManager`

The `TaskManager` is responsible for interpreting and executing the tasks defined in the `tasks` section of your configuration file.

#### Functionality:
- **Task Execution**: It iterates through each configured task and invokes the specified plugin.
- **Component Injection**: It passes the correct agent, tool, and input data to the plugin for each task.
- **Validation**: It ensures that the agents, plugins, and tools required for a task are available before attempting to run it.
- **Output Handling**: It saves the output of a task to a file if configured to do so.

---

### Component Managers (`agent_manager.py`, `plugin_manager.py`, etc.)

Each primary component (agents, plugins, tools, modules) has a corresponding manager located in its respective directory (e.g., `TinyAGI/agents/agent_manager.py`).

#### Functionality:
- **Dynamic Loading**: Managers read the configuration and load components. They can load from local Python files or clone them on-the-fly from GitHub repositories.
- **Instance Management**: They hold instances of the loaded components, making them accessible to other parts of the system.

---

### `utils.py` - Utility Functions

The `utils.py` file provides common, project-wide helper functions.

#### Key Functions:
- **`setup_logging()`**: Configures the application's logger for consistent output.
- **`load_json()`**: A robust function for loading and parsing JSON files with clear error handling.
- **`sanitize_filename()`**: A utility to clean strings so they can be used as safe filenames.

---

### `__init__.py` - Package Entry Point

The `__init__.py` file at the root of the `TinyAGI` package makes key components easily importable.

#### Functionality:
- **Versioning**: Defines the `__version__` for the package.
- **Public API**: Uses `__all__` to expose `AgentSystem` and `load_json`, allowing for clean imports like `import TinyAGI as agi`.