# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/tabitha_agent.py

import logging
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class TabithaAgent(BaseAgent):
    def __init__(self, model_config, module_manager):
        super().__init__(model_config)
        # Assuming Tabitha is a custom module loaded via ModuleManager
        tabitha_module = module_manager.get_module('TabithaModule')
        if not tabitha_module:
            logger.error("TabithaModule not found in ModuleManager.")
            raise ValueError("TabithaModule is required for TabithaAgent.")
        self.tabitha = tabitha_module
        logger.info("TabithaAgent initialized using TabithaModule.")

    def generate_text(self, prompt, stream=False):
        try:
            return self.tabitha.generate(prompt, stream=stream)
        except Exception as e:
            logger.error(f"Error generating text with TabithaAgent: {e}")
            return None

    def embed(self, input_data):
        logger.warning("Embedding is not implemented for TabithaAgent.")
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
