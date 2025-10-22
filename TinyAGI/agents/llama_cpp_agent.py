# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/llama_cpp_agent.py

import logging
from llama_cpp import Llama
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class LlamaCppAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        model_path = self.parameters.get('model_path', '')
        if not model_path:
            logger.error("Model path not provided for LlamaCppAgent.")
            raise ValueError("Model path is required for LlamaCppAgent.")
        self.model = Llama(model_path=model_path)
        logger.info(f"LlamaCppAgent initialized with model at: {model_path}")

    def generate_text(self, prompt, stream=False):
        try:
            output = self.model(prompt, max_tokens=self.parameters.get('max_tokens', 150), stream=stream)
            if stream:
                return (chunk['choices'][0]['text'] for chunk in output)
            else:
                text = output['choices'][0]['text']
                return text
        except Exception as e:
            logger.error(f"Error generating text with LlamaCpp: {e}")
            return None

    def embed(self, input_data):
        logger.warning("Embedding is not implemented for LlamaCppAgent.")
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
