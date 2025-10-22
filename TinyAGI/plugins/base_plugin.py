# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/plugins/base_plugin.py

import logging

logger = logging.getLogger(__name__)

class BasePlugin:
    def __init__(self, config):
        """
        Initialize the plugin with its configuration.

        :param config: Dictionary containing plugin-specific configurations.
        """
        self.config = config
        logger.info(f"{self.__class__.__name__} initialized with config: {self.config}")

    def execute(self, agent, tool, data, options, stream=False):
        """
        Execute the plugin's primary function.

        :param agent: Instance of a model agent to interact with the model backend.
        :param tool: Instance of a tool (optional).
        :param data: Input data for the plugin (e.g., text to summarize).
        :param options: Dictionary containing additional options.
        :param stream: Boolean indicating whether to handle streaming responses.
        :return: Result of the plugin's execution.
        """
        raise NotImplementedError("Execute method must be implemented by the plugin.")


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
