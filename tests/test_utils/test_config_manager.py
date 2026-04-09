import pytest
import tempfile
import os
from src.config.config_manager import ConfigManager
from src.config.default_config import DEFAULT_CONFIG


class TestConfigManager:
    
    def test_load_default_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            config = manager.load()
            assert config == DEFAULT_CONFIG
    
    def test_get_config_value(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            manager.load()
            port = manager.get('server.port')
            assert port == 8080
    
    def test_get_nested_config_value(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            manager.load()
            allowed_origins = manager.get('cors.allowed_origins')
            assert allowed_origins == ['*']
    
    def test_get_with_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            manager.load()
            value = manager.get('non_existent_key', 'default_value')
            assert value == 'default_value'
    
    def test_set_config_value(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            manager.load()
            result = manager.set('server.port', 9090)
            assert result is True
            assert manager.get('server.port') == 9090
    
    def test_update_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            manager.load()
            updates = {
                'server': {'port': 9090},
                'cache': {'max_size': 2000}
            }
            result = manager.update(updates)
            assert result is True
            assert manager.get('server.port') == 9090
            assert manager.get('cache.max_size') == 2000
    
    def test_reset_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            manager.load()
            manager.set('server.port', 9090)
            result = manager.reset()
            assert result is True
            assert manager.get('server.port') == 8080
    
    def test_get_entire_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            config = manager.load()
            entire_config = manager.get()
            assert entire_config == config
    
    def test_file_created(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            manager.load()
            config_path = os.path.join(temp_dir, ConfigManager.CONFIG_FILE)
            assert os.path.exists(config_path)
