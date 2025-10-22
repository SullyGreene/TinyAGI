# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/plugin_manager.py

import logging
import importlib
import os
import git  # Requires gitpython
import sys

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self, plugins_config):
        """
        Initialize the PluginManager with the provided plugins configuration.

        :param plugins_config: List of plugin configurations from the JSON config
        """
        self.plugins_config = plugins_config
        self.loaded_plugins = self.load_plugins()

    def load_plugins(self):
        """
        Load all plugins based on the configuration.

        :return: Dictionary of loaded plugin instances keyed by plugin name
        """
        loaded_plugins = {}
        for plugin_info in self.plugins_config:
            name = plugin_info.get('name')
            module_name = plugin_info.get('module')
            source = plugin_info.get('source', 'local')
            config = plugin_info.get('config', {})

            logger.info(f"Loading plugin '{name}' from module '{module_name}' with source '{source}'.")

            if source == 'github':
                repo_url = plugin_info.get('repo_url')
                if not repo_url:
                    logger.error(f"Repo URL not provided for plugin '{name}'. Skipping.")
                    continue
                self.load_plugin_from_github(module_name, repo_url)

            try:
                module = importlib.import_module(f'TinyAGI.plugins.{module_name}')
                plugin_class = getattr(module, name)
                plugin_instance = plugin_class(config)
                loaded_plugins[name] = plugin_instance
                logger.info(f"Successfully loaded plugin: {name}")
            except AttributeError:
                logger.error(f"Plugin class '{name}' not found in module '{module_name}'.")
            except Exception as e:
                logger.error(f"Failed to load plugin '{name}': {e}", exc_info=True)

        logger.debug(f"All loaded plugins: {list(loaded_plugins.keys())}")
        return loaded_plugins

    def load_plugin_from_github(self, module_name, repo_url):
        """
        Clone a plugin from GitHub if it's not already present.

        :param module_name: Name of the plugin module
        :param repo_url: GitHub repository URL
        """
        plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        module_path = os.path.join(plugins_dir, f"{module_name}.py")

        if not os.path.exists(module_path):
            try:
                logger.info(f"Cloning plugin '{module_name}' from GitHub repository '{repo_url}'.")
                git.Repo.clone_from(repo_url, plugins_dir)
                logger.info(f"Successfully cloned '{module_name}' from GitHub.")
                if plugins_dir not in sys.path:
                    sys.path.insert(0, plugins_dir)
            except Exception as e:
                logger.error(f"Failed to clone plugin '{module_name}': {e}", exc_info=True)

    def get_plugin(self, plugin_name):
        """
        Retrieve a loaded plugin by its name.

        :param plugin_name: Name of the plugin
        :return: Plugin instance or None if not found
        """
        return self.loaded_plugins.get(plugin_name)

    def add_plugin(self, plugin_info):
        """
        Add and load a new plugin dynamically.

        :param plugin_info: Dictionary containing plugin configuration
        """
        self.plugins_config.append(plugin_info)
        plugin_name = plugin_info.get('name')
        module_name = plugin_info.get('module')
        source = plugin_info.get('source', 'local')
        config = plugin_info.get('config', {})

        if source == 'github':
            repo_url = plugin_info.get('repo_url')
            if not repo_url:
                logger.error(f"Repo URL not provided for plugin '{plugin_name}'. Cannot add plugin.")
                return
            self.load_plugin_from_github(module_name, repo_url)

        try:
            module = importlib.import_module(f'TinyAGI.plugins.{module_name}')
            plugin_class = getattr(module, plugin_name)
            plugin_instance = plugin_class(config)
            self.loaded_plugins[plugin_name] = plugin_instance
            logger.info(f"Added and loaded new plugin: {plugin_name}")
        except AttributeError:
            logger.error(f"Plugin class '{plugin_name}' not found in module '{module_name}'.")
        except Exception as e:
            logger.error(f"Failed to add plugin '{plugin_name}': {e}", exc_info=True)

    def remove_plugin(self, plugin_name):
        """
        Remove a loaded plugin by its name.

        :param plugin_name: Name of the plugin to remove
        """
        if plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            logger.info(f"Removed plugin: {plugin_name}")
        else:
            logger.warning(f"Attempted to remove non-existent plugin: {plugin_name}")


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
