
import pytest
import time
from src.server import create_app
from src.service import ServerService


class TestServerModule:
    def test_create_app(self):
        app = create_app()
        assert app is not None
        assert app.config is not None

    def test_server_service_init(self):
        service = ServerService()
        assert service is not None
        assert service.is_running() is False

    def test_server_service_get_status(self):
        service = ServerService()
        status = service.get_status()
        assert 'status' in status
        assert 'version' in status
        assert 'uptime' in status
        assert 'port' in status

    def test_health_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'status' in data['data']

    def test_ping_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.get('/api/health/ping')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['pong'] is True

    def test_get_config_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.get('/api/config')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'server' in data['data']

    def test_update_config_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.put('/api/config', json={
            'server': {'port': 9000},
            'cache': {'max_size': 2000}
        })
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True

    def test_reset_config_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.post('/api/config/reset')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True

    def test_receive_intercept_data_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.post('/api/data/intercept', json={
            'source': {
                'url': 'https://example.com/api',
                'method': 'GET',
                'timestamp': '2024-01-01T00:00:00Z'
            },
            'response': {
                'status': 200,
                'body': {'data': 'test'}
            }
        })
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert 'id' in data['data']

    def test_get_cached_data_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.get('/api/data/cache')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert 'items' in data['data']
        assert 'pagination' in data['data']

    def test_clear_cache_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.delete('/api/data/cache')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True

    def test_export_excel_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.post('/api/export/excel', json={})
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True

    def test_export_history_route(self):
        app = create_app()
        client = app.test_client()
        
        response = client.get('/api/export/history')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True

    def test_404_error(self):
        app = create_app()
        client = app.test_client()
        
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data

