# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/base_agent.py

import logging

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, model_config):
        """
        Initialize the Base Agent with the given configuration.

        :param model_config: Dictionary containing model configuration parameters.
        """
        self.model_config = model_config
        self.model_name = model_config.get('name', '')
        self.parameters = model_config.get('parameters', {})
        logger.info(f"{self.__class__.__name__} initialized with model: {self.model_name}")

    def generate_text(self, prompt, stream=False):
        """
        Generate text using the model.

        :param prompt: The prompt string to send to the model.
        :param stream: Boolean indicating whether to stream responses.
        :return: Generated text or a generator for streaming.
        """
        raise NotImplementedError("generate_text method must be implemented by the agent.")

    def embed(self, input_data):
        """
        Generate embeddings using the model.

        :param input_data: String or list of strings to embed.
        :return: Embedding vector(s).
        """
        raise NotImplementedError("embed method must be implemented by the agent.")


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
