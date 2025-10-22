import pytest
from unittest.mock import MagicMock, patch
from TinyAGI.agents.agent_manager import AgentManager

@pytest.fixture
def mock_module_manager():
    """Fixture for a mock ModuleManager."""
    return MagicMock()

def test_agent_manager_initialization_and_loading(mock_config, mock_module_manager):
    """Test that AgentManager initializes and loads agents correctly from config."""
    agent_configs = mock_config['agents']
    
    # Mock the dynamic import process
    with patch('importlib.import_module') as mock_import:
        mock_agent_module = MagicMock()
        mock_agent_class = MagicMock()
        mock_agent_instance = MagicMock()
        
        # Configure the mocks to simulate successful loading
        mock_agent_class.return_value = mock_agent_instance
        setattr(mock_agent_module, 'MockAgent', mock_agent_class)
        mock_import.return_value = mock_agent_module

        # Initialize AgentManager
        agent_manager = AgentManager(agent_configs, mock_module_manager)

        # Assertions
        # Verify that it tried to import the correct module
        mock_import.assert_called_with('TinyAGI.agents.mock_agent_module')
        # Verify that the agent class was instantiated with its config
        mock_agent_class.assert_called_with(agent_configs[0]['config'])
        # Verify that the loaded agent is available
        assert 'mock_agent' in agent_manager.loaded_agents
        assert agent_manager.get_agent('mock_agent') is mock_agent_instance