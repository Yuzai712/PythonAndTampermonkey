
import pytest
from src.controller import ServerController, ConfigController, DataController


class TestServerController:
    def test_init(self):
        controller = ServerController()
        assert controller is not None
        assert controller._port == 8080
        assert controller._status == 'stopped'

    def test_validate_port_valid(self):
        controller = ServerController()
        assert controller.validate_port(9000) is True

    def test_validate_port_invalid_range_low(self):
        controller = ServerController()
        assert controller.validate_port(100) is False

    def test_validate_port_invalid_range_high(self):
        controller = ServerController()
        assert controller.validate_port(70000) is False

    def test_is_server_running_false(self):
        controller = ServerController()
        assert controller.is_server_running() is False

    def test_start_server(self):
        controller = ServerController()
        result = controller.start_server(9001)
        assert result['success'] is True
        assert controller.is_server_running() is True

    def test_stop_server(self):
        controller = ServerController()
        controller.start_server(9002)
        result = controller.stop_server()
        assert result['success'] is True
        assert controller.is_server_running() is False

    def test_get_server_status(self):
        controller = ServerController()
        status = controller.get_server_status()
        assert 'status' in status
        assert 'version' in status
        assert 'uptime' in status
        assert 'port' in status


class TestConfigController:
    def test_init(self):
        controller = ConfigController()
        assert controller is not None

    def test_get_config(self):
        controller = ConfigController()
        result = controller.get_config()
        assert result['success'] is True
        assert 'server' in result['data']
        assert 'cache' in result['data']

    def test_get_config_value(self):
        controller = ConfigController()
        port = controller.get_config_value('server.port')
        assert port == 8080

    def test_get_config_value_invalid_key(self):
        controller = ConfigController()
        value = controller.get_config_value('invalid.key')
        assert value is None

    def test_update_config(self):
        controller = ConfigController()
        result = controller.update_config({'server': {'port': 9000}})
        assert result['success'] is True
        assert 'updated_fields' in result['data']

    def test_reset_config(self):
        controller = ConfigController()
        result = controller.reset_config()
        assert result['success'] is True
        assert result['data']['reset'] is True


class TestDataController:
    def test_init(self):
        controller = DataController()
        assert controller is not None
        assert len(controller._cached_data) == 0

    def test_validate_intercept_data_valid(self):
        controller = DataController()
        data = {
            'source': {'url': 'https://example.com', 'method': 'GET', 'timestamp': '2024-01-01T00:00:00Z'},
            'response': {'status': 200, 'body': {}}
        }
        is_valid, error_msg = controller.validate_intercept_data(data)
        assert is_valid is True
        assert error_msg is None

    def test_validate_intercept_data_missing_source(self):
        controller = DataController()
        data = {'response': {'status': 200}}
        is_valid, error_msg = controller.validate_intercept_data(data)
        assert is_valid is False
        assert '缺少 source' in error_msg

    def test_validate_intercept_data_missing_response(self):
        controller = DataController()
        data = {'source': {'url': 'https://example.com', 'method': 'GET'}}
        is_valid, error_msg = controller.validate_intercept_data(data)
        assert is_valid is False
        assert '缺少 response' in error_msg

    def test_receive_intercept_data(self):
        controller = DataController()
        data = {
            'source': {'url': 'https://example.com', 'method': 'GET', 'timestamp': '2024-01-01T00:00:00Z'},
            'response': {'status': 200, 'body': {}}
        }
        result = controller.receive_intercept_data(data)
        assert result['success'] is True
        assert 'id' in result['data']
        assert len(controller._cached_data) == 1

    def test_get_cached_data_empty(self):
        controller = DataController()
        result = controller.get_cached_data()
        assert result['success'] is True
        assert len(result['data']['items']) == 0

    def test_get_cached_data_with_items(self):
        controller = DataController()
        data = {
            'source': {'url': 'https://example.com', 'method': 'GET', 'timestamp': '2024-01-01T00:00:00Z'},
            'response': {'status': 200, 'body': {}}
        }
        controller.receive_intercept_data(data)
        
        result = controller.get_cached_data()
        assert result['success'] is True
        assert len(result['data']['items']) == 1

    def test_get_data_detail_not_found(self):
        controller = DataController()
        result = controller.get_data_detail('nonexistent')
        assert result['success'] is False

    def test_get_data_detail_found(self):
        controller = DataController()
        data = {
            'source': {'url': 'https://example.com', 'method': 'GET', 'timestamp': '2024-01-01T00:00:00Z'},
            'response': {'status': 200, 'body': {}}
        }
        receive_result = controller.receive_intercept_data(data)
        data_id = receive_result['data']['id']
        
        result = controller.get_data_detail(data_id)
        assert result['success'] is True
        assert result['data']['id'] == data_id

    def test_clear_cache(self):
        controller = DataController()
        data = {
            'source': {'url': 'https://example.com', 'method': 'GET', 'timestamp': '2024-01-01T00:00:00Z'},
            'response': {'status': 200, 'body': {}}
        }
        controller.receive_intercept_data(data)
        
        result = controller.clear_cache()
        assert result['success'] is True
        assert result['data']['cleared_count'] == 1
        assert len(controller._cached_data) == 0

    def test_export_to_excel(self):
        controller = DataController()
        data = {
            'source': {'url': 'https://example.com', 'method': 'GET', 'timestamp': '2024-01-01T00:00:00Z'},
            'response': {'status': 200, 'body': {}}
        }
        controller.receive_intercept_data(data)
        
        result = controller.export_to_excel()
        assert result['success'] is True
        assert 'file_path' in result['data']
        assert 'row_count' in result['data']

    def test_get_export_history(self):
        controller = DataController()
        result = controller.get_export_history()
        assert result['success'] is True
        assert 'items' in result['data']

