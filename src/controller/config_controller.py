


class ConfigController:
    def __init__(self, config_service=None):
        self.config_service = config_service

    def get_config(self):
        try:
            return {
                'success': True,
                'data': self._get_default_config(),
                'message': '获取配置成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '获取配置失败: {}'.format(str(e))
            }

    def update_config(self, updates):
        try:
            updated_fields = []
            requires_restart = False

            if 'server' in updates:
                if 'port' in updates['server']:
                    updated_fields.append('server.port')
                    requires_restart = True

            if 'cache' in updates:
                if 'max_size' in updates['cache']:
                    updated_fields.append('cache.max_size')

            message = '配置更新成功' if not requires_restart else '配置更新成功，部分配置需要重启服务生效'

            return {
                'success': True,
                'data': {
                    'updated_fields': updated_fields,
                    'requires_restart': requires_restart
                },
                'message': message
            }
        except Exception as e:
            return {
                'success': False,
                'message': '更新配置失败: {}'.format(str(e))
            }

    def reset_config(self):
        try:
            return {
                'success': True,
                'data': {'reset': True},
                'message': '配置已重置为默认值'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '重置配置失败: {}'.format(str(e))
            }

    def get_config_value(self, key):
        config = self._get_default_config()
        keys = key.split('.')
        value = config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return None

    def set_config_value(self, key, value):
        try:
            return {
                'success': True,
                'message': '配置设置成功'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '设置配置失败: {}'.format(str(e))
            }

    def _get_default_config(self):
        return {
            'server': {
                'port': 8080,
                'host': '127.0.0.1'
            },
            'cache': {
                'max_size': 1000,
                'expire_time': 3600
            },
            'export': {
                'output_dir': './exports',
                'default_format': 'xlsx'
            },
            'logging': {
                'level': 'INFO',
                'file': './logs/app.log'
            }
        }

