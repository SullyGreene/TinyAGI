# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/plugins/code_formatter.py

import logging
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class CodeFormatter(BasePlugin):
    def __init__(self, config):
        super().__init__(config)
        self.languages = self.config.get('languages', [])
        self.style = self.config.get('style', 'default')

    def execute(self, agent, tool, input_data, options, stream=False):
        code = input_data.get('code', '')
        language = input_data.get('language', 'python')
        formatted_code = self.format_code(code, language)
        logger.info("Formatted code using CodeFormatter plugin.")
        return formatted_code

    def format_code(self, code, language):
        if language.lower() == 'python':
            try:
                import black
                formatted_code = black.format_str(code, mode=black.FileMode())
                return formatted_code
            except ImportError:
                logger.warning("Black formatter is not installed.")
                return code
            except Exception as e:
                logger.error(f"Error formatting code: {e}")
                return code
        else:
            logger.warning(f"No formatter implemented for language: {language}")
            return code


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
