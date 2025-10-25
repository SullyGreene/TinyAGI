
# TinyAGI/config/agent_config.json

## Overview

The `agent_config.json` file is the primary configuration file for the TinyAGI framework. It defines the agents, plugins, tools, tasks, and modules that the system will use.

## Configuration Sections

- **agents**: Lists the AI agents to be loaded, including their modules, classes, sources, and specific configurations.
- **plugins**: Defines the plugins to extend the system's capabilities, specifying their modules, sources, and configurations.
- **tools**: Specifies external tools to integrate, detailing their modules, classes, sources, and configurations.
- **tasks**: Outlines the tasks to be executed by the system, linking them to specific agents, plugins, and tools.
- **modules**: (Optional) Lists additional modules that the system can load for extended functionalities.

## Example Configuration

```json
{
  "agents": [
    {
      "name": "default_agent",
      "module": "openai_agent",
      "class": "OpenAIAgent",
      "source": "local",
      "config": {
        "type": "chat",
        "name": "gpt-3.5-turbo",
        "parameters": {
          "api_key": "YOUR_OPENAI_API_KEY",
          "temperature": 0.7,
          "max_tokens": 150
        }
      }
    }
  ],
  "plugins": [
    {
      "name": "GenerateText",
      "module": "generate_text",
      "source": "local",
      "config": {
        "prompt_template": "{prompt}"
      }
    },
    {
      "name": "GenerateSummary",
      "module": "generate_summary",
      "source": "local",
      "config": {
        "prompt_template": "Provide a concise summary of the following text:

{text}"
      }
    },
    {
      "name": "GenerateReferences",
      "module": "generate_references",
      "source": "local",
      "config": {
        "prompt_template": "Identify and list any references or sources mentioned in the following text:

{text}

List them as a JSON array."
      }
    },
    {
      "name": "GenerateTags",
      "module": "generate_tags",
      "source": "local",
      "config": {
        "max_tags": 10
      }
    },
    {
      "name": "CodeFormatter",
      "module": "code_formatter",
      "source": "local",
      "config": {
        "languages": ["python"],
        "style": "black"
      }
    }
  ],
  "tools": [
    {
      "name": "WikipediaTool",
      "module": "wikipedia_tool",
      "class": "WikipediaTool",
      "source": "local",
      "config": {
        "language": "en"
      }
    }
  ],
  "tasks": [
    {
      "task_id": "wiki_summary_task",
      "plugin": "GenerateText",
      "agent": "default_agent",
      "tool": "WikipediaTool",
      "input": {
        "prompt": "Explain the theory of relativity."
      },
      "output": {
        "save_to_file": true,
        "file_path": "outputs/relativity_summary.json"
      },
      "options": {
        "generate_summary": true,
        "generate_references": true,
        "generate_tags": true
      }
    }
  ],
  "modules": [
    // Add module configurations here if needed
  ]
}
```

## Notes

- **API Keys**: Ensure that sensitive information like API keys is securely managed, preferably using environment variables or secure storage solutions.
- **Dynamic Loading**: The configuration supports dynamic loading of components from local sources or GitHub repositories.
- **Extensibility**: Easily add new agents, plugins, tools, or modules by updating this configuration file.
