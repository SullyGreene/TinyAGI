# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/plugins/generate_summary.py

import logging
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class GenerateSummary(BasePlugin):
    def __init__(self, config):
        super().__init__(config)
        self.prompt_template = self.config.get('prompt_template', "Provide a concise summary of the following text:\n{text}")

    def execute(self, agent, tool, input_data, options, stream=False):
        text = input_data.get('text', '')
        prompt = self.prompt_template.format(text=text)
        response = agent.generate_text(prompt, stream=stream)
        logger.info("Generated summary using GenerateSummary plugin.")
        return response


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
