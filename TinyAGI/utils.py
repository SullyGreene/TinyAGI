# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/utils.py

import json
import re
import nltk
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_logging():
    """
    Configure the logging settings.
    """
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def load_json(file_path):
    """
    Load JSON data from a file.

    :param file_path: Path to the JSON file.
    :return: Dictionary containing JSON data.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info(f"Loaded JSON data from '{file_path}'.")
        return data
    except FileNotFoundError:
        logging.error(f"JSON file not found at '{file_path}'.")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from '{file_path}': {e}")
        return {}
    except Exception as e:
        logging.error(f"Error loading JSON from '{file_path}': {e}")
        return {}

def sanitize_filename(title):
    """
    Sanitize a string to be used as a safe filename.

    :param title: Original string.
    :return: Sanitized string.
    """
    sanitized = re.sub(r'\W+', '_', title.lower()).strip('_')
    logging.debug(f"Sanitized filename: Original='{title}', Sanitized='{sanitized}'")
    return sanitized

def download_nltk_resources():
    """
    Ensure NLTK resources are available.
    """
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        logging.info("NLTK resources downloaded successfully.")
    except Exception as e:
        logging.error(f"Error downloading NLTK resources: {e}")


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
