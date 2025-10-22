# TinyAGI Wikipedia Tool

## Overview

The `wikipedia_tool.py` file implements the `WikipediaTool` class, which interfaces with the Wikipedia API to fetch summaries and perform searches. It is designed to be a simple and effective way to bring Wikipedia's vast knowledge into the TinyAGI system.

## Functionality

- **Language Support**: Configurable to fetch Wikipedia content in different languages.
- **User-Agent**: Requires a user-agent to be set, as per Wikipedia's API policy.
- **Search**: Allows searching for Wikipedia pages based on a query.
- **Summary Retrieval**: Fetches concise summaries of specified Wikipedia pages.
- **Error Handling**: Manages disambiguation and page not found errors gracefully.

## Key Components

- **__init__**: Initializes the tool with language and user-agent settings from the configuration.
- **search**: Searches Wikipedia for a given query and returns a list of page titles.
- **get_page_summary**: Retrieves a summary for a specified Wikipedia page.

## Usage

Instantiate the `WikipediaTool` with a configuration dictionary that includes the `language` and `user_agent`.

```python
from TinyAGI.tools.wikipedia_tool import WikipediaTool

# Example configuration
config = {
    "language": "en",
    "user_agent": "MyCoolApp/1.0 (https://example.com/my-cool-app; my-email@example.com)"
}

wikipedia_tool = WikipediaTool(config)

# Search for a topic
search_results = wikipedia_tool.search("Artificial Intelligence", results=5)
print(f"Search results: {search_results}")

# Get a page summary
summary = wikipedia_tool.get_page_summary("Artificial Intelligence")
print(f"Summary: {summary}")
```