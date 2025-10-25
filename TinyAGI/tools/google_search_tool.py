# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/tools/google_search_tool.py

import os
import logging
from googleapiclient.discovery import build
from .base_tool import BaseTool

logger = logging.getLogger(__name__)

class GoogleSearchTool(BaseTool):
    def __init__(self, config):
        super().__init__(config)
        self.name = "GoogleSearchTool"
        self.description = "Performs a Google search and returns the top results."
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cse_id = os.getenv("GOOGLE_CSE_ID")
        self.num_results = config.get("num_results", 5)
        if not self.api_key or not self.cse_id:
            raise ValueError("GOOGLE_API_KEY and GOOGLE_CSE_ID must be set in the environment variables.")
        self.service = build("customsearch", "v1", developerKey=self.api_key)

    def execute(self, query: str):
        """
        Performs a Google search.

        :param query: The search query.
        :return: A formatted string of search results or an error message.
        """
        try:
            result = self.service.cse().list(q=query, cx=self.cse_id, num=self.num_results).execute()
            items = result.get('items', [])
            if not items:
                return "No results found."
            
            formatted_results = "\n".join([f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n" for item in items])
            return formatted_results
        except Exception as e:
            logger.error(f"Error performing Google search for query '{query}': {e}")
            return f"An error occurred during the Google search."