# TinyAGI Tools

## Overview

The `tools` directory contains modules that provide agents with specific capabilities, such as searching the web, accessing APIs, or performing calculations. Tools are distinct from plugins and are typically used by agents to complete tasks.

## Tool Manager

The `tool_manager.py` is responsible for loading and managing all available tools. It reads the `tools` configuration from `config.json` and can load them from:
- **Local:** Tools defined as Python modules within this directory.
- **GitHub:** Tools from remote Git repositories, which are cloned on the fly.

## Creating a New Tool

To add a new tool:
1.  Create a new Python file in this directory (e.g., `my_tool.py`).
2.  Define a class for your tool. The `__init__` method should accept a `config` dictionary.
3.  Implement the methods that your tool will provide. For example, a Wikipedia tool might have a `search(query)` method.
4.  Add a configuration entry for your new tool to the `tools` list in `config.json`, specifying its `name`, `module`, `class`, and any `config` it needs.

By creating new tools, you can easily expand the range of tasks your AI agents can perform.

## Example: Using a Tool in a Task

Tools are made available to plugins during task execution. You specify which tool to use in the task definition within your `config.json`.

**1. Define the Task in `config.json`:**

This task uses the `GenerateText` plugin, but provides it with the `WikipediaTool` to gather information before generating a response.

```json
{
  "tasks": [
    {
      "task_id": "summarize_topic",
      "plugin": "GenerateText",
      "agent": "ollama_agent",
      "tool": "WikipediaTool",
      "input": {
        "prompt": "Artificial Intelligence"
      }
    }
  ]
}
```

**2. Run the `AgentSystem`:**

When `agent_system.run()` is called, the `TaskManager` will provide the `WikipediaTool` instance to the `GenerateText` plugin, allowing it to search Wikipedia for "Artificial Intelligence" as part of its execution.

```python
import TinyAGI as agi

agent_system = agi.AgentSystem(config_files='config/agent_config.json')
agent_system.run()
```