# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/agent_manager.py

import logging
import importlib
from ..core.base_manager import BaseManager

logger = logging.getLogger(__name__)

class AgentManager(BaseManager):
    def __init__(self, agents_config, module_manager, base_path):
        """
        Initialize the AgentManager with the provided agents configuration.

        :param agents_config: List of agent configurations.
        :param module_manager: Instance of ModuleManager.
        :param base_path: The base directory for agents.
        """
        super().__init__(
            config_list=agents_config,
            component_type='agent',
            base_path=base_path,
            import_prefix='TinyAGI.agents'
        )
        self.module_manager = module_manager
        self.loaded_components = self.load_components()

    def load_components(self):
        """
        Load all agents based on the configuration.

        :return: Dictionary of loaded agent instances keyed by agent name.
        """
        for agent_info in self.config_list:
            name = agent_info.get('name')
            module_name = agent_info.get('module')
            class_name = agent_info.get('class', name)
            source = agent_info.get('source', 'local')
            config = agent_info.get('config', {})

            try:
                if source == 'github':
                    repo_url = agent_info.get('repo_url')
                    if not repo_url:
                        logger.error(f"Repo URL not provided for GitHub agent '{name}'. Skipping.")
                        continue
                    self._load_from_github(module_name, repo_url)
                
                module = importlib.import_module(f'{self.import_prefix}.{module_name}')
                agent_class = getattr(module, class_name)
                agent_instance = agent_class(config, self.module_manager)
                self.loaded_components[name] = agent_instance
                logger.info(f"Loaded agent: {name}")
            except Exception as e:
                logger.error(f"Failed to load agent '{name}': {e}")

        return self.loaded_components

    def get_agent(self, agent_name):
        return self.get_component(agent_name)

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
