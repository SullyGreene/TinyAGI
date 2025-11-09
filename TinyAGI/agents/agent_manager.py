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
    def __init__(self, agents_config, module_manager, base_path=None):
        """
        Initialize the AgentManager.

        :param agents_config: List of agent configurations.
        :param module_manager: Instance of ModuleManager.
        :param base_path: The base path for resolving local modules.
        """
        self.agents_config = agents_config
        self.module_manager = module_manager
        self.base_path = base_path or os.path.dirname(__file__)
        self.loaded_agents = self.load_agents()

    def load_agents(self):
        """
        Load all agents based on the configuration.
        """
        loaded_agents = {}
        for agent_info in self.agents_config:
            name = agent_info.get('name')
            module_name = agent_info.get('module')
            class_name = agent_info.get('class')
            source = agent_info.get('source', 'local')
            config = agent_info.get('config', {})

            logger.info(f"Loading agent '{name}' from module '{module_name}' with source '{source}'.")

            if source == 'github':
                repo_url = agent_info.get('repo_url')
                if not repo_url:
                    logger.error(f"Repo URL not provided for agent '{name}'. Skipping.")
                    continue
                self.load_agent_from_github(module_name, repo_url)

            try:
                module = importlib.import_module(f'TinyAGI.agents.{module_name}')
                agent_class = getattr(module, class_name)
                agent_instance = agent_class(config)
                loaded_agents[name] = agent_instance
                logger.info(f"Successfully loaded agent: {name}")
            except Exception as e:
                logger.error(f"Failed to load agent '{name}': {e}", exc_info=True)

        return loaded_agents

    def load_agent_from_github(self, module_name, repo_url):
        """
        Clone an agent from a GitHub repository if it doesn't already exist.
        """
        agents_dir = os.path.join(self.base_path)
        module_path = os.path.join(agents_dir, f"{module_name}.py")

        if not os.path.exists(module_path):
            try:
                logger.info(f"Cloning agent '{module_name}' from GitHub repository '{repo_url}'.")
                git.Repo.clone_from(repo_url, agents_dir)
                logger.info(f"Successfully cloned '{module_name}' from GitHub.")
                if agents_dir not in sys.path:
                    sys.path.insert(0, agents_dir)
            except Exception as e:
                logger.error(f"Failed to clone agent '{module_name}': {e}", exc_info=True)

    def get_agent(self, agent_name):
        """
        Retrieve a loaded agent by its name.
        """
        return self.loaded_agents.get(agent_name)

    def get_all_agents(self):
        """
        Retrieve all loaded agents.
        """
        return self.loaded_agents