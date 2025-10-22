# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/modules/module_manager.py

import logging
import importlib
import sys
import os
import git  # Requires gitpython

logger = logging.getLogger(__name__)

class ModuleManager:
    def __init__(self, modules_config):
        """
        Initialize the ModuleManager with the provided modules configuration.

        :param modules_config: List of module configurations.
        """
        self.modules_config = modules_config
        self.loaded_modules = self.load_modules()

    def load_modules(self):
        """
        Load all modules based on the configuration.

        :return: Dictionary of loaded module instances keyed by module name.
        """
        loaded_modules = {}
        for module_info in self.modules_config:
            name = module_info.get('name')
            module_name = module_info.get('module')
            source = module_info.get('source', 'local')
            config = module_info.get('config', {})

            if source == 'github':
                repo_url = module_info.get('repo_url')
                if not repo_url:
                    logger.error(f"Repo URL not provided for module '{name}'. Skipping.")
                    continue
                self.load_module_from_github(module_name, repo_url)

            try:
                module = importlib.import_module(f'TinyAGI.modules.{module_name}')
                module_class = getattr(module, name)
                module_instance = module_class(**config)
                loaded_modules[name] = module_instance
                logger.info(f"Loaded module: {name}")
            except Exception as e:
                logger.error(f"Failed to load module {name}: {e}")

        return loaded_modules

    def load_module_from_github(self, module_name, repo_url):
        """
        Clone a module from GitHub if it's not already present.

        :param module_name: Name of the module.
        :param repo_url: GitHub repository URL.
        """
        modules_dir = os.path.join(os.path.dirname(__file__), module_name)
        if not os.path.exists(modules_dir):
            try:
                logger.info(f"Cloning module '{module_name}' from GitHub repository '{repo_url}'.")
                git.Repo.clone_from(repo_url, modules_dir)
                if modules_dir not in sys.path:
                    sys.path.insert(0, modules_dir)
                logger.info(f"Successfully cloned module '{module_name}' from GitHub.")
            except Exception as e:
                logger.error(f"Failed to clone module '{module_name}': {e}")

    def get_module(self, module_name):
        """
        Retrieve a loaded module by its name.

        :param module_name: Name of the module.
        :return: Module instance or None if not found.
        """
        return self.loaded_modules.get(module_name)

    def add_module(self, module_info):
        """
        Add and load a new module dynamically.

        :param module_info: Dictionary containing module configuration.
        """
        self.modules_config.append(module_info)
        name = module_info.get('name')
        module_name = module_info.get('module')
        source = module_info.get('source', 'local')
        config = module_info.get('config', {})

        if source == 'github':
            repo_url = module_info.get('repo_url')
            if not repo_url:
                logger.error(f"Repo URL not provided for module '{name}'. Cannot add module.")
                return
            self.load_module_from_github(module_name, repo_url)

        try:
            module = importlib.import_module(f'TinyAGI.modules.{module_name}')
            module_class = getattr(module, name)
            module_instance = module_class(**config)
            self.loaded_modules[name] = module_instance
            logger.info(f"Added and loaded new module: {name}")
        except Exception as e:
            logger.error(f"Failed to add module '{name}': {e}")

    def remove_module(self, module_name):
        """
        Remove a loaded module by its name.

        :param module_name: Name of the module to remove.
        """
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            logger.info(f"Removed module: {module_name}")
        else:
            logger.warning(f"Attempted to remove non-existent module: {module_name}")


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
