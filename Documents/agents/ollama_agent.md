
# TinyAGI/agents/ollama_agent.py

## Overview

The `ollama_agent.py` file implements the `OllamaAgent` class, a concrete agent that interfaces with the Ollama server to generate text.

## Functionality

- **Text Generation**: Communicates with the Ollama server to generate responses based on prompts.
- **Streaming Support**: Supports streaming responses for real-time text generation.
- **Error Handling**: Handles potential response errors from the Ollama server.

## Key Components

- **__init__**: Initializes the agent with Ollama server configurations and model details.
- **generate_text**: Sends prompts to the Ollama server and retrieves generated text.
- **embed**: Placeholder for embedding functionality (not implemented).

## Usage

Instantiate the `OllamaAgent` with the required configurations and use its methods to generate text.

```python
from TinyAGI.agents.ollama_agent import OllamaAgent

config = {
    "name": "llama2",
    "host": "http://localhost:11434",
    "parameters": {}
}

agent = OllamaAgent(config, module_manager)
response = agent.generate_text("Explain the theory of relativity.")
```
