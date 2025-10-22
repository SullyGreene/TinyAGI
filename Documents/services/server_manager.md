# TinyAGI Server Manager

## Overview

The `server_manager.py` file sets up and runs a Flask server for the TinyAGI framework. It exposes API endpoints for various functionalities such as chat, text generation, embedding, and configuration management.

## How to Run

The recommended way to start the server is to use the `start.py` script in the root of the project:

```bash
python start.py
```

This script uses Poetry to run the server within the correct environment. Alternatively, you can run the module directly:

```bash
python -m TinyAGI.services.server_manager
```

## Functionality

- **API Endpoints**:
    - `/chat`: Handles chat interactions by processing user messages and generating responses.
    - `/generate`: Handles text generation requests based on provided prompts.
    - `/embed`: Generates embeddings for input data.
    - `/reload`: Reloads the model and configuration dynamically.
    - `/config`: Retrieves the current configuration.
- **Agent Initialization**: Initializes the `AgentSystem` and loads the agents, plugins, and tools as defined in `config/agent_config.json`.
- **Error Handling**: Logs and returns errors encountered during API operations.

## API Usage Examples

- **Chat Endpoint**:

    ```bash
    curl -X POST http://localhost:5000/chat \
         -H "Content-Type: application/json" \
         -d '{"messages": [{"role": "user", "content": "Hello!"}], "stream": false}'
    ```

- **Generate Text Endpoint**:

    ```bash
    curl -X POST http://localhost:5000/generate \
         -H "Content-Type: application/json" \
         -d '{"prompt": "Tell me a joke.", "stream": false}'
    ```

- **Embed Endpoint**:

    ```bash
    curl -X POST http://localhost:5000/embed \
         -H "Content-Type: application/json" \
         -d '{"input": "Sample text for embedding."}'
    ```

- **Reload Configuration Endpoint**:

    ```bash
    curl -X POST http://localhost:5000/reload \
         -H "Content-Type: application/json" \
         -d '{"config_file": "config/new_config.json"}'
    ```

- **Get Configuration Endpoint**:

    ```bash
    curl -X GET http://localhost:5000/config
    ```