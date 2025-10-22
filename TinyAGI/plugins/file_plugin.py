# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/plugins/file_plugin.py

import os
import logging

logger = logging.getLogger(__name__)

class FilePluginPlugin:
    """
    A plugin for reading from and writing to local files.
    """
    def __init__(self, config):
        self.config = config

    def execute(self, agent, tool, input_data, options, stream=False):
        """
        Executes the file operation (read or write).

        :param input_data: A dictionary containing:
                           - 'action': 'read' or 'write'
                           - 'file_path': The path to the file.
                           - 'content': The content to write (for 'write' action).
        :return: The content of the file for 'read', or a success message for 'write'.
        """
        action = input_data.get('action')
        file_path = input_data.get('file_path')

        if not action or not file_path:
            raise ValueError("'action' and 'file_path' are required in input_data for FilePlugin.")

        if action == 'read':
            return self._read_file(file_path)
        elif action == 'write':
            content = input_data.get('content')
            if content is None:
                raise ValueError("'content' is required for 'write' action in FilePlugin.")
            return self._write_file(file_path, content)
        else:
            raise ValueError(f"Unsupported action '{action}'. Use 'read' or 'write'.")

    def _read_file(self, file_path):
        """Reads content from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading from file {file_path}: {e}")
            raise

    def _write_file(self, file_path, content):
        """Writes content to a file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(content)) # Ensure content is a string
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            logger.error(f"Error writing to file {file_path}: {e}")
            raise