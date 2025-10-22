# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/alpaca_x_agent.py

import logging
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class AlpacaXAgent(BaseAgent):
    def __init__(self, model_config, module_manager):
        super().__init__(model_config)
        # Assuming AlpacaX is a custom module loaded via ModuleManager
        alpaca_x_module = module_manager.get_module('AlpacaXModule')
        if not alpaca_x_module:
            logger.error("AlpacaXModule not found in ModuleManager.")
            raise ValueError("AlpacaXModule is required for AlpacaXAgent.")
        self.alpaca_x = alpaca_x_module
        logger.info("AlpacaXAgent initialized using AlpacaXModule.")

    def generate_text(self, prompt, stream=False):
        try:
            return self.alpaca_x.generate(prompt, stream=stream)
        except Exception as e:
            logger.error(f"Error generating text with AlpacaXAgent: {e}")
            return None

    def embed(self, input_data):
        logger.warning("Embedding is not implemented for AlpacaXAgent.")
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
