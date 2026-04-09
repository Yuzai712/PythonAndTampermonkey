
import socket
from typing import Dict, Any


class ServerController:
    def __init__(self, server_service=None):
        self.server_service = server_service
        self._port = 8080
        self._status = 'stopped'

    def start_server(self, port):
        try:
            if not self.validate_port(port):
                return {
                    'success': False,
                    'message': '端口 {} 无效或已被占用'.format(port)
                }

            if self.is_server_running():
                return {
                    'success': False,
                    'message': '服务已在运行中'
                }

            self._port = port
            self._status = 'running'

            return {
                'success': True,
                'message': '服务启动成功',
                'data': {
                    'port': port
                }
            }
        except Exception as e:
            return {
                'success': False,
                'message': '启动服务失败: {}'.format(str(e))
            }

    def stop_server(self):
        try:
            if not self.is_server_running():
                return {
                    'success': False,
                    'message': '服务未在运行'
                }

            self._status = 'stopped'

            return {
                'success': True,
                'message': '服务已停止'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '停止服务失败: {}'.format(str(e))
            }

    def get_server_status(self):
        return {
            'status': self._status,
            'version': '1.0.0',
            'uptime': 3600,
            'port': self._port
        }

    def is_server_running(self):
        return self._status == 'running'

    def validate_port(self, port):
        if not isinstance(port, int) or port < 1024 or port > 65535:
            return False

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result != 0
        except:
            return True

