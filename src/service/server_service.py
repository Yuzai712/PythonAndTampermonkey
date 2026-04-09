
import threading
import time
from werkzeug.serving import make_server


class ServerThread(threading.Thread):
    def __init__(self, app, host='127.0.0.1', port=8080):
        super().__init__(daemon=True)
        self.app = app
        self.host = host
        self.port = port
        self.server = None
        self.stop_event = threading.Event()

    def run(self):
        self.server = make_server(self.host, self.port, self.app)
        self.server.serve_forever()

    def stop(self):
        if self.server:
            self.server.shutdown()


class ServerService:
    def __init__(self, app_factory=None, config_service=None):
        self.app_factory = app_factory
        self.config_service = config_service
        self.server_thread = None
        self.app = None
        self._start_time = None

    def start(self, port=8080):
        try:
            if self.is_running():
                return False

            if self.app_factory:
                self.app = self.app_factory()
            else:
                from src.server import create_app
                self.app = create_app()

            self.server_thread = ServerThread(self.app, '127.0.0.1', port)
            self.server_thread.start()
            self._start_time = time.time()
            
            time.sleep(0.5)
            return True
        except Exception:
            return False

    def stop(self):
        try:
            if not self.is_running():
                return False

            if self.server_thread:
                self.server_thread.stop()
                self.server_thread.join(timeout=2)
                self.server_thread = None
                self.app = None
                self._start_time = None
            return True
        except Exception:
            return False

    def is_running(self):
        return self.server_thread is not None and self.server_thread.is_alive()

    def get_status(self):
        uptime = 0
        if self._start_time:
            uptime = int(time.time() - self._start_time)
        
        return {
            'status': 'running' if self.is_running() else 'stopped',
            'version': '1.0.0',
            'uptime': uptime,
            'port': 8080
        }

