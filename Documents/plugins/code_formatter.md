
# TinyAGI/plugins/code_formatter.py

## Overview

The `code_formatter.py` file implements the `CodeFormatter` plugin, which formats code snippets according to specified styles and languages.

## Functionality

- **Language Support**: Supports multiple programming languages (currently Python).
- **Formatting Styles**: Applies formatting styles using external libraries (e.g., Black for Python).
- **Error Handling**: Logs warnings if the necessary formatter is not installed or if formatting fails.

## Key Components

- **__init__**: Initializes the plugin with supported languages and formatting styles.
- **execute**: Formats the provided code snippet based on the specified language and style.
- **format_code**: Applies the actual formatting using the appropriate formatter library.

## Usage

Configure the `CodeFormatter` plugin in the configuration file and execute it within tasks.

```python
from TinyAGI.plugins.code_formatter import CodeFormatter

config = {
    "languages": ["python"],
    "style": "black"
}

plugin = CodeFormatter(config)
formatted_code = plugin.execute(agent, tool, {"code": "def foo():
    return 'bar'", "language": "python"}, options)
```
