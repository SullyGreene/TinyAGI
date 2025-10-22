
# TinyAGI/plugin_manager.py

## Overview

The `plugin_manager.py` file defines the `PluginManager` class, responsible for loading, managing, and interacting with plugins within the TinyAGI framework.

## Functionality

- **Loading Plugins**: Loads plugins based on the configuration, supporting local and GitHub sources.
- **Dynamic Management**: Allows adding and removing plugins at runtime.
- **Error Handling**: Logs errors encountered during plugin loading and management.

## Key Components

- **load_plugins**: Iterates through the plugin configurations and loads each plugin.
- **load_plugin_from_github**: Clones plugin repositories from GitHub if specified.
- **get_plugin**: Retrieves a loaded plugin by name.
- **add_plugin / remove_plugin**: Dynamically adds or removes plugins from the system.

## Usage

Plugins can be defined in the configuration file and managed through the `PluginManager`.

```python
from TinyAGI.plugin_manager import PluginManager

plugin_manager = PluginManager(plugins_config)
plugin = plugin_manager.get_plugin('GenerateText')
plugin.execute(...)
```
