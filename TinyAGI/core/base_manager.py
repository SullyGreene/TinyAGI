# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/core/base_manager.py

import logging
import importlib
import os
import sys
import git

logger = logging.getLogger(__name__)

class BaseManager:
    """
    A base class for managing components (agents, plugins, tools, modules).
    Handles dynamic loading from local files and GitHub repositories.
    """
    def __init__(self, config_list, component_type, base_path, import_prefix):
        """
        Initializes the BaseManager.

        :param config_list: List of component configurations.
        :param component_type: The type of component being managed (e.g., 'agent', 'plugin').
        :param base_path: The base directory for local components.
        :param import_prefix: The Python import prefix for the components.
        """
        self.config_list = config_list
        self.component_type = component_type
        self.base_path = base_path
        self.import_prefix = import_prefix
        self.loaded_components = {}

    def _load_from_github(self, module_name, repo_url):
        """
        Clones a component from a GitHub repository if it's not already present.

        :param module_name: The name of the module (which will be the directory name).
        :param repo_url: The URL of the GitHub repository.
        """
        component_dir = os.path.join(self.base_path, module_name)
        if not os.path.exists(component_dir):
            try:
                logger.info(f"Cloning {self.component_type} '{module_name}' from GitHub: {repo_url}")
                git.Repo.clone_from(repo_url, component_dir)
                # Add the new directory to the Python path to make it importable
                if component_dir not in sys.path:
                    sys.path.insert(0, component_dir)
                logger.info(f"Successfully cloned {self.component_type} '{module_name}'.")
            except Exception as e:
                logger.error(f"Failed to clone {self.component_type} '{module_name}': {e}")
                raise

    def get_component(self, name):
        """
        Retrieves a loaded component by its name.

        :param name: The name of the component.
        :return: The component instance or None if not found.
        """
        return self.loaded_components.get(name)

    def remove_component(self, name):
        """
        Removes a loaded component by its name.

        :param name: The name of the component to remove.
        """
        if name in self.loaded_components:
            del self.loaded_components[name]
            logger.info(f"Removed {self.component_type}: {name}")
        else:
            logger.warning(f"Attempted to remove non-existent {self.component_type}: {name}")

    def get_all_components(self):
        """Returns a dictionary of all loaded components."""
        return self.loaded_components

    def load_components(self):
        """
        A placeholder method that child classes must implement to handle
        the specific logic of loading their components.
        """
        raise NotImplementedError("Subclasses must implement the 'load_components' method.")