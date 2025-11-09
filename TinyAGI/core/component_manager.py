# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/core/component_manager.py

import logging
import os
import sys
import subprocess
import importlib
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class BaseComponentManager:
    """
    A base class for managing components (agents, plugins, tools) that can be
    loaded from local or remote sources.
    """
    def __init__(self, component_type: str, configs: List[Dict[str, Any]], base_path: str):
        self.component_type = component_type
        self.configs = configs
        self.base_path = base_path
        self.external_dir = os.path.join(self.base_path, 'external', f'{self.component_type}s')
        os.makedirs(self.external_dir, exist_ok=True)
        self.loaded_components = {}

    def _install_from_git(self, url: str, name: str) -> str:
        """Clones a git repository into the external components directory."""
        target_dir = os.path.join(self.external_dir, name)
        if not os.path.exists(target_dir):
            logger.info(f"Installing {self.component_type} '{name}' from {url}...")
            try:
                subprocess.run(['git', 'clone', url, target_dir], check=True, capture_output=True, text=True)
                logger.info(f"Successfully installed '{name}' to {target_dir}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone repository for '{name}'. Error: {e.stderr}")
                return None
        else:
            logger.debug(f"Component '{name}' already exists at {target_dir}. Skipping installation.")
        
        # Add the parent directory to sys.path to allow for relative imports within the module
        if target_dir not in sys.path:
            sys.path.insert(0, target_dir)
        return target_dir

    def _load_component_class(self, module_name: str, class_name: str, source_info: str):
        """Dynamically imports and returns a class from a module."""
        try:
            module = importlib.import_module(module_name)
            component_class = getattr(module, class_name)
            return component_class
        except ImportError:
            logger.error(f"Could not import module '{module_name}' for {self.component_type} from {source_info}.")
        except AttributeError:
            logger.error(f"Could not find class '{class_name}' in module '{module_name}' for {self.component_type}.")
        return None

    def load_components(self):
        """Loads all components based on their configuration."""
        raise NotImplementedError("Subclasses must implement load_components.")

    def get_component(self, name: str):
        """Retrieves a loaded component by name."""
        return self.loaded_components.get(name)