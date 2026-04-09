
from flask import Blueprint, request, jsonify
from datetime import datetime

data_bp = Blueprint('data', __name__, url_prefix='/api/data')

_data_controller = None


def init_controllers(data_controller):
    global _data_controller
    _data_controller = data_controller


@data_bp.route('/intercept', methods=['POST'])
def receive_intercept():
    from src.controller import DataController
    
    try:
        controller = _data_controller or DataController()
        data = request.get_json()
        
        result = controller.receive_intercept_data(data)
        
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
                    'code': 3001,
                    'message': result['message']
                },
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 3003,
                'message': '数据处理失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500


@data_bp.route('/intercept/batch', methods=['POST'])
def receive_intercept_batch():
    from src.controller import DataController
    
    try:
        controller = _data_controller or DataController()
        data = request.get_json()
        
        items = data.get('items', [])
        ids = []
        received_count = 0
        
        for item in items:
            result = controller.receive_intercept_data(item)
            if result['success']:
                ids.append(result['data']['id'])
                received_count += 1
        
        return jsonify({
            'success': True,
            'data': {
                'total': len(items),
                'received': received_count,
                'ids': ids
            },
            'message': '批量数据接收成功',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 3003,
                'message': '批量数据处理失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500


@data_bp.route('/cache', methods=['GET'])
def get_cached_data():
    from src.controller import DataController
    
    try:
        controller = _data_controller or DataController()
        
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        source_url = request.args.get('source_url')
        
        filters = {}
        if source_url:
            filters['source_url'] = source_url
        
        result = controller.get_cached_data(page, size, filters)
        
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


@data_bp.route('/cache/&lt;data_id&gt;', methods=['GET'])
def get_data_detail(data_id):
    from src.controller import DataController
    
    try:
        controller = _data_controller or DataController()
        
        result = controller.get_data_detail(data_id)
        
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
                    'code': 3001,
                    'message': result['message']
                },
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 3003,
                'message': '查询失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500


@data_bp.route('/cache', methods=['DELETE'])
def clear_cache():
    from src.controller import DataController
    
    try:
        controller = _data_controller or DataController()
        
        result = controller.clear_cache()
        
        return jsonify({
            'success': True,
            'data': result['data'],
            'message': result['message'],
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 3003,
                'message': '清空缓存失败: {}'.format(str(e))
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500

