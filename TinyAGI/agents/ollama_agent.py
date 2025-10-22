# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/ollama_agent.py

import logging
import ollama
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class OllamaAgent(BaseAgent):
    def __init__(self, model_config, module_manager):
        super().__init__(model_config)
        self.model_name = self.model_config.get('name', 'llama3.2:1b')
        self.host = self.parameters.get('host', 'http://localhost:11434')
        self.client = ollama.Client(host=self.host)
        logger.info(f"OllamaAgent initialized with model: {self.model_name} at host: {self.host}")

    def generate_text(self, prompt, stream=False):
        try:
            if stream:
                response_stream = self.client.generate(
                    model=self.model_name,
                    prompt=prompt,
                    stream=True
                )
                return (chunk.get('response', '') for chunk in response_stream)
            else:
                response = self.client.generate(
                    model=self.model_name,
                    prompt=prompt
                )
                content = response.get('response', '')
                return content
        except ollama.ResponseError as e:
            logger.error(f"Ollama ResponseError: {e.error} (Status Code: {e.status_code})")
            return None

    def embed(self, input_data):
        logger.warning("Embedding is not implemented for OllamaAgent.")
        return []


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
