
# TinyAGI/task_manager.py

## Overview

The `task_manager.py` file contains the `TaskManager` class, which is responsible for executing tasks defined in the configuration using the appropriate agents, plugins, and tools.

## Functionality

- **Task Execution**: Iterates through all configured tasks and executes them.
- **Validation**: Ensures that the specified agents, plugins, and tools exist before execution.
- **Output Handling**: Manages the saving of task outputs based on configuration.

## Key Components

- **execute_tasks**: Main method that processes each task by invoking the relevant plugin with the specified agent, tool, and input data.
- **save_output**: Saves the result of a task to a file if configured to do so.

## Usage

Define tasks in the configuration file and execute them using the `TaskManager`.

```python
from TinyAGI.task_manager import TaskManager

task_manager = TaskManager(agent_manager, plugin_manager, tool_manager, tasks_config)
task_manager.execute_tasks()
```
