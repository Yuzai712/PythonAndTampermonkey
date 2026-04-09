
from flask import Blueprint, request, jsonify
from datetime import datetime

export_bp = Blueprint('export', __name__, url_prefix='/api/export')

_data_controller = None


def init_controllers(data_controller):
    global _data_controller
    _data_controller = data_controller


@export_bp.route('/excel', methods=['POST'])
def export_excel():
    from src.controller import DataController
    
    try:
        controller = _data_controller or DataController()
        config = request.get_json()
        
        result = controller.export_to_excel(config)
        
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
                    'code': 3003,
                    'message': result['message']
                },
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 3003,
                'message': '导出失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500


@export_bp.route('/download/&lt;filename&gt;', methods=['GET'])
def download_file(filename):
    return jsonify({
        'success': False,
        'error': {
            'code': 404,
            'message': '下载功能待实现'
        },
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 404


@export_bp.route('/history', methods=['GET'])
def get_export_history():
    from src.controller import DataController
    
    try:
        controller = _data_controller or DataController()
        
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        
        result = controller.get_export_history(page, size)
        
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
                    'code': 3003,
                    'message': result['message']
                },
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 3003,
                'message': '查询失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500

