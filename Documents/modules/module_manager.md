
# TinyAGI/modules/module_manager.py

## Overview

The `module_manager.py` file defines the `ModuleManager` class, responsible for loading, managing, and interacting with various modules within the TinyAGI framework.

## Functionality

- **Module Loading**: Loads modules based on configuration, supporting both local and GitHub sources.
- **Dynamic Management**: Allows adding and removing modules at runtime.
- **Error Handling**: Logs any issues encountered during module loading and management.

## Key Components

- **load_modules**: Processes the module configurations and initializes each module.
- **load_module_from_github**: Clones module repositories from GitHub if specified.
- **get_module**: Retrieves a loaded module by name.
- **add_module / remove_module**: Dynamically manages modules within the system.

## Usage

Modules are defined in the configuration file and managed through the `ModuleManager`.

```python
from TinyAGI.modules.module_manager import ModuleManager

module_manager = ModuleManager(modules_config)
module = module_manager.get_module('AlpacaXModule')
module.perform_task()
```
