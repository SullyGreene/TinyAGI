
# TinyAGI/tools/base_tool.py

## Overview

The `base_tool.py` file defines the `BaseTool` abstract class, which serves as a blueprint for all external tools integrated into the TinyAGI framework.

## Functionality

- **Initialization**: Sets up basic configurations for tools.
- **Abstract Methods**: Declares methods that must be implemented by all concrete tool classes.

## Key Components

- **__init__**: Initializes the tool with its specific configurations.
- **execute**: Abstract method to perform the tool's primary function.

## Usage

Create concrete tool classes by inheriting from `BaseTool` and implementing the required methods.

```python
from TinyAGI.tools.base_tool import BaseTool

class CustomTool(BaseTool):
    def execute(self, *args, **kwargs):
        # Implementation here
        pass
```
