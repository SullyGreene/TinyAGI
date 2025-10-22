import pytest
from TinyAGI.config_validator import validate_config
import copy

def test_validate_config_valid(mock_config):
    """Test that a valid configuration passes validation."""
    assert validate_config(mock_config) is True

def test_validate_config_missing_required_top_level_key(mock_config):
    """Test that a config missing a required top-level key (e.g., 'agents') fails."""
    invalid_config = copy.deepcopy(mock_config)
    del invalid_config['agents']
    assert validate_config(invalid_config) is False

def test_validate_config_missing_required_task_key(mock_config):
    """Test that a task missing a required key (e.g., 'task_id') fails."""
    invalid_config = copy.deepcopy(mock_config)
    del invalid_config['tasks'][0]['task_id']
    assert validate_config(invalid_config) is False

def test_validate_config_invalid_source_enum(mock_config):
    """Test that an invalid 'source' enum value fails validation."""
    invalid_config = copy.deepcopy(mock_config)
    invalid_config['agents'][0]['source'] = 'invalid_source'
    assert validate_config(invalid_config) is False

def test_validate_config_wrong_type(mock_config):
    """Test that a property with the wrong data type fails validation."""
    invalid_config = copy.deepcopy(mock_config)
    invalid_config['agents'] = "this should be a list"
    assert validate_config(invalid_config) is False