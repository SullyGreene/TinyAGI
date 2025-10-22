
# TinyAGI/requirements.txt

## Overview

The `requirements.txt` file lists all Python dependencies required to run the TinyAGI framework. It ensures that all necessary packages are installed in the virtual environment.

## Dependencies

- **openai**: Interfaces with OpenAI's API for text generation and embeddings.
- **gitpython**: Allows cloning of repositories from GitHub for dynamic component loading.
- **flask**: Web framework used to create API endpoints.
- **wikipedia**: Interfaces with the Wikipedia API to fetch summaries and perform searches.
- **nltk**: Natural Language Toolkit for text processing tasks like tokenization and stopword removal.
- **python-dotenv**: Loads environment variables from a `.env` file.
- **llama-cpp-python**: Interfaces with LLaMA models for text generation.
- **ollama**: Client for interacting with the Ollama server.
- **black**: Python code formatter.
- **Additional Dependencies**: Add other required packages as needed.

## Installation

Install all dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Notes

- **Version Pinning**: For reproducibility, consider specifying exact versions for each package.
- **Virtual Environment**: It's recommended to install dependencies within a virtual environment to avoid conflicts.
