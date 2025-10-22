
# TinyAGI/plugins/generate_references.py

## Overview

The `generate_references.py` file implements the `GenerateReferences` plugin, which extracts and lists references or sources mentioned in a given text.

## Functionality

- **Prompt Construction**: Creates prompts designed to identify references within the input text.
- **JSON Parsing**: Parses the agent's response to extract references in JSON format.

## Key Components

- **__init__**: Initializes the plugin with a references prompt template.
- **execute**: Formats the prompt with the input text, invokes the agent, and processes the JSON response to extract references.

## Usage

Configure the `GenerateReferences` plugin in the configuration file and execute it within tasks.

```python
from TinyAGI.plugins.generate_references import GenerateReferences

config = {
    "prompt_template": "Identify and list any references or sources mentioned in the following text:

{text}

List them as a JSON array."
}

plugin = GenerateReferences(config)
references = plugin.execute(agent, tool, {"text": "Text with references..."}, options)
```
