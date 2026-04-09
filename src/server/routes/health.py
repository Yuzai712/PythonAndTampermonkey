
from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint('health', __name__, url_prefix='/api')

_server_controller = None


def init_controllers(server_controller):
    global _server_controller
    _server_controller = server_controller


@health_bp.route('/health', methods=['GET'])
def check_health():
    from src.controller import ServerController
    
    controller = _server_controller or ServerController()
    status = controller.get_server_status()
    
    return jsonify({
        'success': True,
        'data': status,
        'message': '服务正常运行',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })


@health_bp.route('/health/ping', methods=['GET'])
def ping():
    return jsonify({
        'success': True,
        'data': {
            'pong': True,
            'server_time': datetime.utcnow().isoformat() + 'Z'
        },
        'message': 'pong',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })

