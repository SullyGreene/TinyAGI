# TinyAGI Plugins

## Overview

The `plugins` directory is where you can extend the functionality of TinyAGI agents. Plugins are modular components that can be dynamically loaded to provide additional capabilities, such as data processing, external API integrations, or custom logic.

## Plugin Manager

The `plugin_manager.py` handles the loading and management of all plugins. It reads the `plugins` configuration from `config.json` and can load plugins from two sources:
- **Local:** Plugins defined as Python modules within this directory.
- **GitHub:** Plugins from remote Git repositories, which are cloned automatically.

## Creating a New Plugin

To create a new plugin:
1.  Create a new Python file in this directory (e.g., `my_plugin.py`).
2.  Define a class with the same name as your plugin. The `__init__` method should accept a `config` dictionary.
3.  Implement the methods that your plugin will expose.
4.  Add a configuration entry for your new plugin to the `plugins` list in `config.json`, specifying its `name`, `module`, and any `config` it requires.

Plugins are a powerful way to customize and enhance TinyAGI without modifying its core code.

## Example: Running a Plugin

Plugins are executed by the `TaskManager` as part of a task defined in your `config.json`. The `AgentSystem` orchestrates this process.

**1. Define the Task in `config.json`:**

```json
{
  "tasks": [
    {
      "task_id": "generate_story",
      "plugin": "GenerateText",
      "agent": "ollama_agent",
      "input": {
        "prompt": "Write a short story about a dragon who loves to cook."
      }
    }
  ]
}
```

**2. Run the `AgentSystem`:**

The `agent_system.run()` method will automatically find the `generate_story` task and execute the `GenerateText` plugin with the specified agent and input.

```python
import TinyAGI as agi

agent_system = agi.AgentSystem(config_files='config/agent_config.json')
agent_system.run()
```