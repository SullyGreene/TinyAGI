import pytest

@pytest.fixture
def mock_config():
    """Provides a mock configuration for testing."""
    return {
        "agents": [
            {
                "name": "mock_agent",
                "module": "mock_agent_module",
                "class": "MockAgent",
                "source": "local",
                "config": {}
            }
        ],
        "plugins": [
            {
                "name": "mock_plugin",
                "module": "mock_plugin_module",
                "source": "local",
                "config": {}
            }
        ],
        "tools": [
            {
                "name": "mock_tool",
                "module": "mock_tool_module",
                "class": "MockTool",
                "source": "local",
                "config": {}
            }
        ],
        "tasks": [
            {
                "task_id": "simple_task",
                "plugin": "mock_plugin",
                "agent": "mock_agent",
                "input": {"prompt": "Hello"},
            },
            {
                "task_id": "chained_task_1",
                "plugin": "mock_plugin",
                "agent": "mock_agent",
                "input": {"prompt": "First step"},
            },
            {
                "task_id": "chained_task_2",
                "plugin": "mock_plugin",
                "agent": "mock_agent",
                "input": {"prompt": "{{tasks.chained_task_1.output}}"},
            }
        ],
        "modules": []
    }