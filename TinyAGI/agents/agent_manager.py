# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/agent_manager.py

import logging
import importlib
import os
import sys
import git  # Requires gitpython

logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self, agents_config, module_manager):
        """
        Initialize the AgentManager with the provided agents configuration.

        :param agents_config: List of agent configurations.
        :param module_manager: Instance of ModuleManager.
        """
        self.agents_config = agents_config
        self.module_manager = module_manager
        self.loaded_agents = self.load_agents()

    def load_agents(self):
        """
        Load all agents based on the configuration.

        :return: Dictionary of loaded agent instances keyed by agent name.
        """
        loaded_agents = {}
        for agent_info in self.agents_config:
            name = agent_info.get('name')
            module_name = agent_info.get('module')
            class_name = agent_info.get('class', name)
            source = agent_info.get('source', 'local')
            config = agent_info.get('config', {})

            if source == 'github':
                repo_url = agent_info.get('repo_url')
                if not repo_url:
                    logger.error(f"Repo URL not provided for agent '{name}'. Skipping.")
                    continue
                self.load_agent_from_github(module_name, repo_url)

            try:
                module = importlib.import_module(f'TinyAGI.agents.{module_name}')
                agent_class = getattr(module, class_name)
                agent_instance = agent_class(config, self.module_manager)
                loaded_agents[name] = agent_instance
                logger.info(f"Loaded agent: {name}")
            except Exception as e:
                logger.error(f"Failed to load agent '{name}': {e}")

        return loaded_agents

    def load_agent_from_github(self, module_name, repo_url):
        """
        Clone an agent from GitHub if it's not already present.

        :param module_name: Name of the agent module.
        :param repo_url: GitHub repository URL.
        """
        agents_dir = os.path.join(os.path.dirname(__file__), module_name)
        if not os.path.exists(agents_dir):
            try:
                logger.info(f"Cloning agent '{module_name}' from GitHub repository '{repo_url}'.")
                git.Repo.clone_from(repo_url, agents_dir)
                if agents_dir not in sys.path:
                    sys.path.insert(0, agents_dir)
                logger.info(f"Successfully cloned agent '{module_name}' from GitHub.")
            except Exception as e:
                logger.error(f"Failed to clone agent '{module_name}': {e}")

    def get_agent(self, agent_name):
        """
        Retrieve a loaded agent by its name.

        :param agent_name: Name of the agent.
        :return: Agent instance or None if not found.
        """
        return self.loaded_agents.get(agent_name)

    def add_agent(self, agent_info):
        """
        Add and load a new agent dynamically.

        :param agent_info: Dictionary containing agent configuration.
        """
        self.agents_config.append(agent_info)
        name = agent_info.get('name')
        module_name = agent_info.get('module')
        class_name = agent_info.get('class', name)
        source = agent_info.get('source', 'local')
        config = agent_info.get('config', {})

        if source == 'github':
            repo_url = agent_info.get('repo_url')
            if not repo_url:
                logger.error(f"Repo URL not provided for agent '{name}'. Cannot add agent.")
                return
            self.load_agent_from_github(module_name, repo_url)

        try:
            module = importlib.import_module(f'TinyAGI.agents.{module_name}')
            agent_class = getattr(module, class_name)
            agent_instance = agent_class(config, self.module_manager)
            self.loaded_agents[name] = agent_instance
            logger.info(f"Added and loaded new agent: {name}")
        except Exception as e:
            logger.error(f"Failed to add agent '{name}': {e}")

    def remove_agent(self, agent_name):
        """
        Remove a loaded agent by its name.

        :param agent_name: Name of the agent to remove.
        """
        if agent_name in self.loaded_agents:
            del self.loaded_agents[agent_name]
            logger.info(f"Removed agent: {agent_name}")
        else:
            logger.warning(f"Attempted to remove non-existent agent: {agent_name}")


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
