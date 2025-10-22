
# TinyAGI/plugins/generate_summary.py

## Overview

The `generate_summary.py` file implements the `GenerateSummary` plugin, which generates concise summaries of provided text.

## Functionality

- **Prompt Formatting**: Constructs prompts tailored to generate summaries of input text.
- **Text Summarization**: Utilizes the agent to create summaries based on the formatted prompts.

## Key Components

- **__init__**: Initializes the plugin with a summary prompt template.
- **execute**: Formats the prompt with the input text and invokes the agent to generate a summary.

## Usage

Configure the `GenerateSummary` plugin in the configuration file and execute it within tasks.

```python
from TinyAGI.plugins.generate_summary import GenerateSummary

config = {
    "prompt_template": "Provide a concise summary of the following text:

{text}"
}

plugin = GenerateSummary(config)
summary = plugin.execute(agent, tool, {"text": "Long text here..."}, options)
```
