import pytest
import tempfile
import os
from src.service.cache_service import ThreadSafeCache
from src.service.data_service import DataService


class TestThreadSafeCache:
    
    def test_set_and_get(self):
        cache = ThreadSafeCache(max_size=10)
        cache.set('key1', {'data': 'value1'})
        result = cache.get('key1')
        assert result == {'data': 'value1'}
    
    def test_get_non_existent(self):
        cache = ThreadSafeCache()
        result = cache.get('non_existent')
        assert result is None
    
    def test_delete(self):
        cache = ThreadSafeCache()
        cache.set('key1', {'data': 'value1'})
        result = cache.delete('key1')
        assert result is True
        assert cache.get('key1') is None
    
    def test_clear(self):
        cache = ThreadSafeCache()
        cache.set('key1', {'data': 'value1'})
        cache.set('key2', {'data': 'value2'})
        count = cache.clear()
        assert count == 2
        assert cache.size() == 0
    
    def test_max_size(self):
        cache = ThreadSafeCache(max_size=3)
        cache.set('key1', {'data': 'value1'})
        cache.set('key2', {'data': 'value2'})
        cache.set('key3', {'data': 'value3'})
        cache.set('key4', {'data': 'value4'})
        assert cache.size() == 3
        assert cache.get('key1') is None


class TestDataService:
    
    def test_store_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = DataService(export_dir=temp_dir)
            data = {
                'source': {
                    'url': 'https://example.com/api',
                    'method': 'GET'
                },
                'response': {
                    'status': 200,
                    'body': {'data': []}
                }
            }
            data_id = service.store_data(data)
            assert data_id.startswith('data_')
            assert service.get_data(data_id) is not None
    
    def test_get_data_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = DataService(export_dir=temp_dir)
            
            for i in range(5):
                service.store_data({
                    'source': {'url': f'https://example.com/api/{i}', 'method': 'GET'},
                    'response': {'status': 200, 'body': {}}
                })
            
            result = service.get_data_list(page=1, size=3)
            assert len(result['items']) == 3
            assert result['pagination']['total'] == 5
            assert result['pagination']['total_pages'] == 2
    
    def test_clear_all_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = DataService(export_dir=temp_dir)
            
            service.store_data({
                'source': {'url': 'https://example.com/api', 'method': 'GET'},
                'response': {'status': 200, 'body': {}}
            })
            
            count = service.clear_all_data()
            assert count == 1
            assert service.get_data_count() == 0
    
    def test_export_to_excel(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = DataService(export_dir=temp_dir)
            
            service.store_data({
                'source': {'url': 'https://example.com/api', 'method': 'GET'},
                'response': {'status': 200, 'body': {}}
            })
            
            file_path = service.export_to_excel()
            assert os.path.exists(file_path)
            assert file_path.endswith('.xlsx')
