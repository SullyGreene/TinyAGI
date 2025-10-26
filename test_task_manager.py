import pytest
import TinyAGI as agi
from unittest.mock import MagicMock, call

@pytest.fixture
def mock_managers():
    """Fixture for mock managers."""
    return MagicMock(), MagicMock(), MagicMock()

def test_execute_simple_task(mock_managers, mock_config):
    """Test executing a single, simple task."""
    mock_agent_manager, mock_plugin_manager, mock_tool_manager = mock_managers
    
    # Setup mocks
    mock_agent = MagicMock()
    mock_plugin = MagicMock()
    mock_plugin.execute.return_value = "Mocked response"

    mock_agent_manager.get_agent.return_value = mock_agent
    mock_plugin_manager.get_plugin.return_value = mock_plugin
    mock_plugin_manager.loaded_plugins = {"mock_plugin": mock_plugin}
    mock_agent_manager.loaded_agents = {"mock_agent": mock_agent}
    mock_tool_manager.loaded_tools = {}

    # Initialize TaskManager with the first task
    task_manager = agi.TaskManager(mock_agent_manager, mock_plugin_manager, mock_tool_manager, [mock_config['tasks'][0]])
    task_manager.execute_tasks()

    # Assertions
    mock_plugin_manager.get_plugin.assert_called_with("mock_plugin")
    mock_agent_manager.get_agent.assert_called_with("mock_agent")
    mock_plugin.execute.assert_called_once()
    assert task_manager.task_results["simple_task"] == "Mocked response"

def test_task_chaining(mock_managers, mock_config):
    """Test that the output of one task is used as input for another."""
    mock_agent_manager, mock_plugin_manager, mock_tool_manager = mock_managers

    # Setup mocks
    mock_agent = MagicMock()
    mock_plugin = MagicMock()
    # The plugin will return different values on each call
    mock_plugin.execute.side_effect = ["First response", "Second response"]

    mock_agent_manager.get_agent.return_value = mock_agent
    mock_plugin_manager.get_plugin.return_value = mock_plugin
    mock_plugin_manager.loaded_plugins = {"mock_plugin": mock_plugin}
    mock_agent_manager.loaded_agents = {"mock_agent": mock_agent}
    mock_tool_manager.loaded_tools = {}

    # Use the two chained tasks from the config
    tasks = [mock_config['tasks'][1], mock_config['tasks'][2]]
    task_manager = agi.TaskManager(mock_agent_manager, mock_plugin_manager, mock_tool_manager, tasks)
    task_manager.execute_tasks()

    # Assertions
    assert mock_plugin.execute.call_count == 2
    
    # Check the first call
    first_call_args = mock_plugin.execute.call_args_list[0]
    assert first_call_args.kwargs['input_data']['prompt'] == "First step"

    # Check the second call, where the input should be the output of the first
    second_call_args = mock_plugin.execute.call_args_list[1]
    assert second_call_args.kwargs['input_data']['prompt'] == "First response"

    assert task_manager.task_results["chained_task_1"] == "First response"
    assert task_manager.task_results["chained_task_2"] == "Second response"