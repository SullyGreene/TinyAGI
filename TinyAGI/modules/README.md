# TinyAGI Modules

## Overview

The `modules` directory contains shared components and utilities that can be used across different parts of the TinyAGI framework, such as by agents or plugins. These are general-purpose modules that provide foundational capabilities.

## Module Manager

The `module_manager.py` is responsible for discovering, loading, and managing all available modules. It reads the module configurations from the main `config.json` and can dynamically load modules from:
- **Local:** Modules defined as Python modules within this directory.
- **GitHub:** Modules from remote Git repositories, which are cloned on the fly.

## Creating a New Module

To add a new module, you need to:
1.  Create a new Python file in this directory (e.g., `my_module.py`).
2.  Inside the file, define a class for your module. The `__init__` method can accept keyword arguments for configuration.
3.  Add a new entry to the `modules` list in your `config.json` file, specifying the `name`, `module`, and any `config` required for your new module.

This system allows for shared logic to be maintained and reused effectively.