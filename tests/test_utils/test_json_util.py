import pytest
import tempfile
import os
from src.utils.json_util import JsonUtil


class TestJsonUtil:
    
    def test_write_and_read(self):
        data = {'name': 'test', 'value': 123}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            JsonUtil.write(temp_path, data)
            result = JsonUtil.read(temp_path)
            assert result == data
        finally:
            os.unlink(temp_path)
    
    def test_dumps_and_loads(self):
        data = {'name': 'test', 'value': 123}
        json_str = JsonUtil.dumps(data)
        result = JsonUtil.loads(json_str)
        assert result == data
    
    def test_is_valid(self):
        valid_json = '{"name": "test"}'
        invalid_json = '{name: test}'
        assert JsonUtil.is_valid(valid_json) is True
        assert JsonUtil.is_valid(invalid_json) is False
    
    def test_merge(self):
        base = {'a': 1, 'b': {'x': 10}}
        override = {'b': {'y': 20}, 'c': 3}
        result = JsonUtil.merge(base, override)
        assert result == {'a': 1, 'b': {'x': 10, 'y': 20}, 'c': 3}
