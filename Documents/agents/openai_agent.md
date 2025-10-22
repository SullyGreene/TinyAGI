
# TinyAGI/agents/openai_agent.py

## Overview

The `openai_agent.py` file implements the `OpenAIAgent` class, a concrete agent that interacts with OpenAI's GPT models to generate text and embeddings.

## Functionality

- **Text Generation**: Uses OpenAI's API to generate responses based on prompts.
- **Embedding Generation**: Generates embeddings for input data using OpenAI's embedding models.
- **Streaming Support**: Supports streaming responses for real-time text generation.

## Key Components

- **__init__**: Initializes the agent with OpenAI API configurations and model details.
- **generate_text**: Communicates with OpenAI's API to generate text based on prompts.
- **embed**: Generates embeddings for given input data.

## Usage

Instantiate the `OpenAIAgent` with the required configurations and use its methods to generate text or embeddings.

```python
from TinyAGI.agents.openai_agent import OpenAIAgent

config = {
    "type": "chat",
    "name": "gpt-3.5-turbo",
    "parameters": {
        "api_key": "YOUR_OPENAI_API_KEY",
        "temperature": 0.7,
        "max_tokens": 150
    }
}

agent = OpenAIAgent(config)
response = agent.generate_text("What is the capital of France?")
embeddings = agent.embed("Sample text for embedding.")
```
