# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/plugins/tool_executor.py

import logging
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class ToolExecutor(BasePlugin):
    """
    A plugin that executes a specified tool with the given input.
    """
    def __init__(self, config):
        super().__init__(config)

    def execute(self, agent, tool, input_data, options, stream=False):
        """
        Executes the provided tool.

        :param agent: The agent instance (not directly used by this plugin but part of the interface).
        :param tool: The tool instance to execute.
        :param input_data: The input data for the tool.
        :param options: Additional options for execution.
        :param stream: Boolean indicating if the output should be streamed.
        :return: The output from the tool.
        """
        if not tool:
            raise ValueError("ToolExecutor requires a 'tool' to be specified in the task.")
        
        logger.info(f"Executing tool '{tool.name}' with input: {input_data}")
        return tool.execute(**input_data)