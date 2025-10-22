import pytest
from unittest.mock import MagicMock, patch
from TinyAGI.plugins.plugin_manager import PluginManager

def test_plugin_manager_initialization_and_loading(mock_config):
    """Test that PluginManager initializes and loads plugins correctly from config."""
    plugin_configs = mock_config['plugins']
    
    # Mock the dynamic import process
    with patch('importlib.import_module') as mock_import:
        mock_plugin_module = MagicMock()
        mock_plugin_class = MagicMock()
        mock_plugin_instance = MagicMock()
        
        # The class name is derived from the module name (e.g., mock_plugin_module -> MockPluginModulePlugin)
        class_name = "MockPluginModulePlugin"

        # Configure mocks to simulate successful loading
        mock_plugin_class.return_value = mock_plugin_instance
        setattr(mock_plugin_module, class_name, mock_plugin_class)
        mock_import.return_value = mock_plugin_module

        # Initialize PluginManager
        plugin_manager = PluginManager(plugin_configs)

        # Assertions
        mock_import.assert_called_with('TinyAGI.plugins.mock_plugin_module')
        mock_plugin_class.assert_called_with(plugin_configs[0].get('config', {}))
        assert 'mock_plugin' in plugin_manager.loaded_plugins
        assert plugin_manager.get_plugin('mock_plugin') is mock_plugin_instance