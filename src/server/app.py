
from flask import Flask, jsonify
from datetime import datetime


def create_app(config=None):
    app = Flask(__name__)
    
    if config:
        app.config.update(config)
    
    register_blueprints(app)
    configure_middleware(app)
    configure_error_handlers(app)
    
    return app


def register_blueprints(app):
    from src.server.routes.health import health_bp
    from src.server.routes.data import data_bp
    from src.server.routes.export import export_bp
    from src.server.routes.config import config_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(config_bp)


def configure_middleware(app):
    from src.server.middleware.cors import add_cors_headers
    
    app.after_request(add_cors_headers)


def configure_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 404,
                'message': '资源不存在'
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 500,
                'message': '服务器内部错误'
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500

