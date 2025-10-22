
# TinyAGI/plugins/plugin_manager.py

## Overview

The `plugin_manager.py` file manages the loading and lifecycle of plugins within the TinyAGI framework. It supports both local plugins and those hosted on GitHub.

## Functionality

- **Plugin Loading**: Dynamically loads plugins based on configuration settings.
- **GitHub Integration**: Clones plugins from GitHub repositories if specified.
- **Dynamic Management**: Allows adding and removing plugins at runtime.
- **Error Handling**: Logs errors encountered during plugin operations.

## Key Components

- **load_plugins**: Iterates through plugin configurations and initializes each plugin.
- **load_plugin_from_github**: Clones plugin repositories from GitHub when needed.
- **get_plugin**: Retrieves a loaded plugin by name.
- **add_plugin / remove_plugin**: Facilitates dynamic addition and removal of plugins.

## Usage

Define plugins in the configuration file and manage them through the `PluginManager`.

```python
from TinyAGI.plugins.plugin_manager import PluginManager

plugin_manager = PluginManager(plugins_config)
plugin = plugin_manager.get_plugin('GenerateText')
result = plugin.execute(agent, tool, input_data, options)
```
