
# TinyAGI/tools/tool_manager.py

## Overview

The `tool_manager.py` file defines the `ToolManager` class, which manages the loading, integration, and lifecycle of external tools within the TinyAGI framework.

## Functionality

- **Tool Loading**: Dynamically loads tools based on configuration, supporting both local and GitHub sources.
- **Dynamic Management**: Allows adding and removing tools at runtime.
- **Error Handling**: Logs any issues encountered during tool loading and management.

## Key Components

- **load_tools**: Processes the tool configurations and initializes each tool.
- **load_tool_from_github**: Clones tool repositories from GitHub if specified.
- **get_tool**: Retrieves a loaded tool by name.
- **add_tool / remove_tool**: Facilitates dynamic addition and removal of tools.

## Usage

Define tools in the configuration file and manage them through the `ToolManager`.

```python
from TinyAGI.tools.tool_manager import ToolManager

tool_manager = ToolManager(tools_config)
wikipedia_tool = tool_manager.get_tool('WikipediaTool')
summary = wikipedia_tool.get_page_summary("Albert Einstein")
```
