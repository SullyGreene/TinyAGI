# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/tools/wikipedia_tool.py

import logging
import wikipediaapi
from .base_tool import BaseTool

logger = logging.getLogger(__name__)

class WikipediaTool(BaseTool):
    def __init__(self, config):
        """
        Initialize the WikipediaTool with the given configuration.

        :param config: Dictionary containing tool-specific configurations.
        """
        super().__init__(config)
        self.language = self.config.get('language', 'en')
        self.user_agent = self.config.get('user_agent', 'TinyAGI/1.0')
        self.wiki = wikipediaapi.Wikipedia(user_agent=self.user_agent, language=self.language)
        logger.info(f"WikipediaTool initialized with language: {self.language} and user_agent: {self.user_agent}")

    def search(self, query, results=5):
        """
        Search Wikipedia for the given query.

        :param query: The search query string.
        :param results: Number of search results to return.
        :return: List of page titles.
        """
        try:
            logger.info(f"Searching Wikipedia for query: '{query}' with {results} results.")
            search_results = self.wiki.search(query, results=results)
            logger.info(f"Found {len(search_results)} results.")
            return search_results
        except Exception as e:
            logger.error(f"Error during Wikipedia search: {e}")
            return []

    def get_page_summary(self, title, sentences=3):
        """
        Get the summary of a Wikipedia page. If the exact title isn't found, perform a search and fetch the summary of the first result.

        :param title: Title of the Wikipedia page.
        :param sentences: Number of sentences in the summary.
        :return: Summary string.
        """
        try:
            if not title.strip():
                logger.error("Empty title provided for fetching summary.")
                return "No title provided for fetching summary."

            logger.info(f"Fetching summary for Wikipedia page: '{title}'.")
            page = self.wiki.page(title)
            if page.exists():
                summary = page.summary
                logger.info("Fetched summary successfully.")
                return summary
            else:
                logger.warning(f"Page '{title}' does not exist. Performing a search.")
                search_results = self.search(title, results=1)
                if search_results:
                    first_result = search_results[0]
                    page = self.wiki.page(first_result)
                    if page.exists():
                        summary = page.summary
                        logger.info(f"Fetched summary for '{first_result}' successfully.")
                        return summary
                    else:
                        logger.error(f"Page '{first_result}' does not exist.")
                        return f"No Wikipedia page found for '{title}'."
                else:
                    logger.error(f"No search results found for query '{title}'.")
                    return f"No Wikipedia page found for '{title}'."
        except Exception as e:
            logger.error(f"Unexpected error fetching page summary: {e}", exc_info=True)
            return ""


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
