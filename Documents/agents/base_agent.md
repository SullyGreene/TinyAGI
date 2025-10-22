
# TinyAGI/agents/base_agent.py

## Overview

The `base_agent.py` file defines the `BaseAgent` abstract class, which serves as a blueprint for all AI agents within the TinyAGI framework.

## Functionality

- **Initialization**: Sets up basic configurations and parameters for agents.
- **Abstract Methods**: Declares methods that must be implemented by all concrete agent classes.

## Key Components

- **__init__**: Initializes the agent with model configurations.
- **generate_text**: Abstract method to generate text based on a prompt.
- **embed**: Abstract method to generate embeddings from input data.

## Usage

Create concrete agent classes by inheriting from `BaseAgent` and implementing the required methods.

```python
from TinyAGI.agents.base_agent import BaseAgent

class OpenAIAgent(BaseAgent):
    def generate_text(self, prompt, stream=False):
        # Implementation here
        pass
    
    def embed(self, input_data):
        # Implementation here
        pass
```
