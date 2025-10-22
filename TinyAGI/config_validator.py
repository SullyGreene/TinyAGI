# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/config_validator.py

import jsonschema
import logging

logger = logging.getLogger(__name__)

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "agents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "module": {"type": "string", "minLength": 1},
                    "class": {"type": "string", "minLength": 1},
                    "source": {"type": "string", "enum": ["local", "github"]},
                    "config": {"type": "object"}
                },
                "required": ["name", "module", "class", "source", "config"]
            }
        },
        "plugins": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "module": {"type": "string", "minLength": 1},
                    "source": {"type": "string", "enum": ["local", "github"]},
                    "config": {"type": "object"}
                },
                "required": ["name", "module", "source"]
            }
        },
        "tools": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "module": {"type": "string", "minLength": 1},
                    "class": {"type": "string", "minLength": 1},
                    "source": {"type": "string", "enum": ["local", "github"]},
                    "config": {"type": "object"}
                },
                "required": ["name", "module", "class", "source"]
            }
        },
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "minLength": 1},
                    "plugin": {"type": "string", "minLength": 1},
                    "agent": {"type": "string", "minLength": 1},
                    "tool": {"type": ["string", "null"]},
                    "input": {"type": "object"},
                    "output": {"type": "object"},
                    "options": {"type": "object"}
                },
                "required": ["task_id", "plugin", "agent", "input"]
            }
        },
        "modules": {
            "type": "array"
        }
    },
    "required": ["agents", "plugins", "tools", "tasks"]
}

def validate_config(config_data):
    """
    Validates the configuration data against the defined schema.

    :param config_data: The configuration dictionary to validate.
    :return: True if validation is successful, False otherwise.
    """
    try:
        jsonschema.validate(instance=config_data, schema=CONFIG_SCHEMA)
        logger.info("Configuration validation successful.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Configuration validation error: {e.message}")
        logger.error(f"Path to error: {list(e.path)}")
        return False
    except jsonschema.exceptions.SchemaError as e:
        logger.error(f"Configuration schema is invalid: {e.message}")
        return False