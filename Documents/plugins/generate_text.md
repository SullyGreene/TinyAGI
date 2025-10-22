
# TinyAGI/plugins/generate_text.py

## Overview

The `generate_text.py` file implements the `GenerateText` plugin, which facilitates text generation using a specified agent and optional tools.

## Functionality

- **Prompt Handling**: Formats prompts based on a template and integrates additional information from tools if available.
- **Text Generation**: Utilizes the agent to generate text based on the processed prompt.
- **Streaming Support**: Supports streaming responses for real-time text generation.

## Key Components

- **__init__**: Initializes the plugin with a prompt template.
- **execute**: Formats the prompt, optionally enriches it using a tool (e.g., WikipediaTool), and invokes the agent to generate text.

## Usage

Configure the `GenerateText` plugin in the configuration file and execute it within tasks.

```python
from TinyAGI.plugins.generate_text import GenerateText

config = {
    "prompt_template": "{prompt}"
}

plugin = GenerateText(config)
response = plugin.execute(agent, tool, {"prompt": "Hello, world!"}, options)
```
