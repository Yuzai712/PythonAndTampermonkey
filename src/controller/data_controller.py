
from datetime import datetime
import uuid


class DataController:
    def __init__(self, data_service=None):
        self.data_service = data_service
        self._cached_data = {}
        self._export_history = []

    def receive_intercept_data(self, data):
        try:
            is_valid, error_msg = self.validate_intercept_data(data)
            if not is_valid:
                return {
                    'success': False,
                    'message': '数据格式错误: {}'.format(error_msg)
                }

            data_id = self._generate_data_id()
            received_at = datetime.utcnow().isoformat() + 'Z'

            self._cached_data[data_id] = {
                'id': data_id,
                **data,
                'received_at': received_at,
                'processed': False
            }

            return {
                'success': True,
                'data': {
                    'id': data_id,
                    'received_at': received_at,
                    'processed': False
                },
                'message': '数据接收成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '数据接收失败: {}'.format(str(e))
            }

    def get_cached_data(self, page=1, size=20, filters=None):
        try:
            source_url = filters.get('source_url') if filters else None

            all_items = list(self._cached_data.values())
            
            if source_url:
                all_items = [
                    item for item in all_items
                    if item.get('source', {}).get('url') == source_url
                ]

            total = len(all_items)
            total_pages = (total + size - 1) // size if total > 0 else 1
            
            start = (page - 1) * size
            end = start + size
            items = all_items[start:end]

            return {
                'success': True,
                'data': {
                    'items': [
                        {
                            'id': item['id'],
                            'source_url': item.get('source', {}).get('url'),
                            'received_at': item['received_at'],
                            'processed': item['processed']
                        }
                        for item in items
                    ],
                    'pagination': {
                        'page': page,
                        'size': size,
                        'total': total,
                        'total_pages': total_pages
                    }
                },
                'message': '查询成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '查询失败: {}'.format(str(e))
            }

    def get_data_detail(self, data_id):
        try:
            if data_id not in self._cached_data:
                return {
                    'success': False,
                    'message': '数据不存在: {}'.format(data_id)
                }

            return {
                'success': True,
                'data': self._cached_data[data_id],
                'message': '查询成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '查询失败: {}'.format(str(e))
            }

    def clear_cache(self):
        try:
            cleared_count = len(self._cached_data)
            self._cached_data.clear()

            return {
                'success': True,
                'data': {'cleared_count': cleared_count},
                'message': '缓存已清空'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '清空缓存失败: {}'.format(str(e))
            }

    def export_to_excel(self, format_config=None, filters=None):
        try:
            filename = (format_config.get('format', {}).get('filename', 'export_data') 
                       if format_config else 'export_data')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = '{}_{}.xlsx'.format(filename, timestamp)
            
            row_count = len(self._cached_data)
            file_size = 10240

            export_record = {
                'id': 'export_{}'.format(uuid.uuid4().hex[:8]),
                'filename': output_filename,
                'file_size': file_size,
                'row_count': row_count,
                'created_at': datetime.utcnow().isoformat() + 'Z'
            }
            self._export_history.append(export_record)

            return {
                'success': True,
                'data': {
                    'file_path': './exports/{}'.format(output_filename),
                    'file_size': file_size,
                    'row_count': row_count,
                    'download_url': '/api/export/download/{}'.format(output_filename)
                },
                'message': '导出成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '导出失败: {}'.format(str(e))
            }

    def get_export_history(self, page=1, size=20):
        try:
            total = len(self._export_history)
            total_pages = (total + size - 1) // size if total > 0 else 1
            
            start = (page - 1) * size
            end = start + size
            items = self._export_history[start:end]

            return {
                'success': True,
                'data': {
                    'items': items,
                    'pagination': {
                        'page': page,
                        'size': size,
                        'total': total,
                        'total_pages': total_pages
                    }
                },
                'message': '查询成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '查询失败: {}'.format(str(e))
            }

    def validate_intercept_data(self, data):
        if 'source' not in data:
            return False, '缺少 source 字段'

        source = data['source']
        if not isinstance(source, dict):
            return False, 'source 必须是对象'

        if 'url' not in source:
            return False, 'source.url 字段缺失'

        if 'method' not in source:
            return False, 'source.method 字段缺失'

        if 'response' not in data:
            return False, '缺少 response 字段'

        response = data['response']
        if not isinstance(response, dict):
            return False, 'response 必须是对象'

        if 'status' not in response:
            return False, 'response.status 字段缺失'

        return True, None

    def _generate_data_id(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return 'data_{}_{}'.format(timestamp, uuid.uuid4().hex[:6])

