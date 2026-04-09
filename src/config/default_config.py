DEFAULT_CONFIG = {
    "server": {
        "host": "127.0.0.1",
        "port": 8080,
        "debug": False,
        "threaded": True
    },
    "cache": {
        "max_size": 1000,
        "expire_time": 3600,
        "cleanup_interval": 300
    },
    "export": {
        "output_dir": "./exports",
        "default_format": "xlsx",
        "filename_template": "export_{timestamp}",
        "max_history": 50
    },
    "logging": {
        "level": "INFO",
        "file": "./logs/app.log",
        "max_size": 10485760,
        "backup_count": 5,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "cors": {
        "allowed_origins": ["*"],
        "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
        "allowed_headers": ["Content-Type", "Authorization"],
        "allow_credentials": True
    },
    "ui": {
        "window": {
            "width": 600,
            "height": 500,
            "resizable": True
        },
        "theme": "default",
        "font_family": "Arial",
        "font_size": 10
    }
}
