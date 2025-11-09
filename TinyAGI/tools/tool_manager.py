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
    def __init__(self, tools_config, base_path=None):
        """
        Initialize the ToolManager.

        :param tools_config: List of tool configurations.
        :param base_path: The base path for resolving local modules.
        """
        self.tools_config = tools_config
        self.base_path = base_path or os.path.dirname(__file__)
        self.loaded_tools = self.load_tools()

    def load_tools(self):
        """
        Load all tools based on the configuration.
        """
        loaded_tools = {}
        for tool_info in self.tools_config:
            name = tool_info.get('name')
            module_name = tool_info.get('module')
            class_name = tool_info.get('class')
            source = tool_info.get('source', 'local')
            config = tool_info.get('config', {})

            logger.info(f"Loading tool '{name}' from module '{module_name}' with source '{source}'.")

            if source == 'github':
                repo_url = tool_info.get('repo_url')
                if not repo_url:
                    logger.error(f"Repo URL not provided for tool '{name}'. Skipping.")
                    continue
                self.load_tool_from_github(module_name, repo_url)

            try:
                # Dynamically import the module from the tools directory
                module = importlib.import_module(f'TinyAGI.tools.{module_name}')
                tool_class = getattr(module, class_name)
                tool_instance = tool_class(config)
                loaded_tools[name] = tool_instance
                logger.info(f"Successfully loaded tool: {name}")
            except AttributeError:
                logger.error(f"Tool class '{class_name}' not found in module '{module_name}'.")
            except Exception as e:
                logger.error(f"Failed to load tool '{name}': {e}", exc_info=True)

        logger.debug(f"All loaded tools: {list(loaded_tools.keys())}")
        return loaded_tools

    def load_tool_from_github(self, module_name, repo_url):
        """
        Clone a tool from a GitHub repository if it doesn't already exist.
        """
        tools_dir = os.path.join(self.base_path)
        # This assumes the repo contains a file named `module_name.py`
        module_path = os.path.join(tools_dir, f"{module_name}.py")

        if not os.path.exists(module_path):
            try:
                logger.info(f"Cloning tool '{module_name}' from GitHub repository '{repo_url}'.")
                # This is a simplified clone; a real implementation might need to handle subdirectories
                git.Repo.clone_from(repo_url, tools_dir)
                logger.info(f"Successfully cloned '{module_name}' from GitHub.")
                if tools_dir not in sys.path:
                    sys.path.insert(0, tools_dir)
            except Exception as e:
                logger.error(f"Failed to clone tool '{module_name}': {e}", exc_info=True)

    def get_tool(self, tool_name):
        """
        Retrieve a loaded tool by its name.
        """
        return self.loaded_tools.get(tool_name)


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