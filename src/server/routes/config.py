
from flask import Blueprint, request, jsonify
from datetime import datetime

config_bp = Blueprint('config', __name__, url_prefix='/api')

_config_controller = None


def init_controllers(config_controller):
    global _config_controller
    _config_controller = config_controller


@config_bp.route('/config', methods=['GET'])
def get_config():
    from src.controller import ConfigController
    
    try:
        controller = _config_controller or ConfigController()
        
        result = controller.get_config()
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': result['message'],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': {
                    'code': 1001,
                    'message': result['message']
                },
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 1001,
                'message': '获取配置失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500


@config_bp.route('/config', methods=['PUT'])
def update_config():
    from src.controller import ConfigController
    
    try:
        controller = _config_controller or ConfigController()
        updates = request.get_json()
        
        result = controller.update_config(updates)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': result['message'],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': {
                    'code': 1002,
                    'message': result['message']
                },
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 1002,
                'message': '更新配置失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500


@config_bp.route('/config/reset', methods=['POST'])
def reset_config():
    from src.controller import ConfigController
    
    try:
        controller = _config_controller or ConfigController()
        
        result = controller.reset_config()
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': result['message'],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': {
                    'code': 1002,
                    'message': result['message']
                },
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 1002,
                'message': '重置配置失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500

