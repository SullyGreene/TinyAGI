
# TinyAGI/utils.py

## Overview

The `utils.py` file provides utility functions and setup configurations essential for the TinyAGI framework.

## Functionality

- **Logging Setup**: Configures the logging settings for consistent log formatting and levels.
- **JSON Loading**: Provides a function to load JSON data from files with error handling.
- **Filename Sanitization**: Offers a utility to sanitize strings for safe file naming.

## Key Components

- **setup_logging**: Initializes the logging configuration.
- **load_json**: Loads and parses JSON files, handling potential errors gracefully.
- **sanitize_filename**: Cleans strings to create safe filenames by removing or replacing invalid characters.

## Usage

Import and use the utility functions as needed within the project.

```python
from TinyAGI.utils import load_json, sanitize_filename

config = load_json('config/agent_config.json')
safe_filename = sanitize_filename("Example Title!")
```
