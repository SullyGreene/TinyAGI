# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/tools/tool_manager.py

import logging
import importlib
import os
import sys
import git  # Requires gitpython

logger = logging.getLogger(__name__)

class ToolManager:
    def __init__(self, tools_config):
        """
        Initialize the ToolManager with the provided tools configuration.

        :param tools_config: List of tool configurations.
        """
        self.tools_config = tools_config
        self.loaded_tools = self.load_tools()

    def load_tools(self):
        """
        Load all tools based on the configuration.

        :return: Dictionary of loaded tool instances keyed by tool name.
        """
        loaded_tools = {}
        for tool_info in self.tools_config:
            name = tool_info.get('name')
            module_name = tool_info.get('module')
            class_name = tool_info.get('class', name)
            source = tool_info.get('source', 'local')
            config = tool_info.get('config', {})

            if source == 'github':
                repo_url = tool_info.get('repo_url')
                if not repo_url:
                    logger.error(f"Repo URL not provided for tool '{name}'. Skipping.")
                    continue
                self.load_tool_from_github(module_name, repo_url)

            try:
                module = importlib.import_module(f'TinyAGI.tools.{module_name}')
                tool_class = getattr(module, class_name)
                tool_instance = tool_class(config)
                loaded_tools[name] = tool_instance
                logger.info(f"Loaded tool: {name}")
            except Exception as e:
                logger.error(f"Failed to load tool '{name}': {e}")

        return loaded_tools

    def load_tool_from_github(self, module_name, repo_url):
        """
        Clone a tool from GitHub if it's not already present.

        :param module_name: Name of the tool module.
        :param repo_url: GitHub repository URL.
        """
        tools_dir = os.path.join(os.path.dirname(__file__), module_name)
        if not os.path.exists(tools_dir):
            try:
                logger.info(f"Cloning tool '{module_name}' from GitHub repository '{repo_url}'.")
                git.Repo.clone_from(repo_url, tools_dir)
                if tools_dir not in sys.path:
                    sys.path.insert(0, tools_dir)
                logger.info(f"Successfully cloned tool '{module_name}' from GitHub.")
            except Exception as e:
                logger.error(f"Failed to clone tool '{module_name}': {e}")

    def get_tool(self, tool_name):
        """
        Retrieve a loaded tool by its name.

        :param tool_name: Name of the tool.
        :return: Tool instance or None if not found.
        """
        return self.loaded_tools.get(tool_name)

    def add_tool(self, tool_info):
        """
        Add and load a new tool dynamically.

        :param tool_info: Dictionary containing tool configuration.
        """
        self.tools_config.append(tool_info)
        name = tool_info.get('name')
        module_name = tool_info.get('module')
        class_name = tool_info.get('class', name)
        source = tool_info.get('source', 'local')
        config = tool_info.get('config', {})

        if source == 'github':
            repo_url = tool_info.get('repo_url')
            if not repo_url:
                logger.error(f"Repo URL not provided for tool '{name}'. Cannot add tool.")
                return
            self.load_tool_from_github(module_name, repo_url)

        try:
            module = importlib.import_module(f'TinyAGI.tools.{module_name}')
            tool_class = getattr(module, class_name)
            tool_instance = tool_class(config)
            self.loaded_tools[name] = tool_instance
            logger.info(f"Added and loaded new tool: {name}")
        except Exception as e:
            logger.error(f"Failed to add tool '{name}': {e}")

    def remove_tool(self, tool_name):
        """
        Remove a loaded tool by its name.

        :param tool_name: Name of the tool to remove.
        """
        if tool_name in self.loaded_tools:
            del self.loaded_tools[tool_name]
            logger.info(f"Removed tool: {tool_name}")
        else:
            logger.warning(f"Attempted to remove non-existent tool: {tool_name}")


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
