import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    """
    日志工具类。
    
    功能：
    - 配置日志
    - 输出日志
    - 日志文件管理
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._loggers = {}
    
    @classmethod
    def get_instance(cls, name: str = 'app') -> 'Logger':
        """
        获取日志实例。
        
        参数：
            name: 日志名称
        
        返回：
            Logger 实例
        """
        instance = cls()
        if name not in instance._loggers:
            instance._loggers[name] = logging.getLogger(name)
            instance._loggers[name].setLevel(logging.INFO)
        return instance
    
    def configure(self, level: str = 'INFO', file: Optional[str] = None, format: Optional[str] = None, max_size: int = 10485760, backup_count: int = 5):
        """
        配置日志。
        
        参数：
            level: 日志级别
            file: 日志文件路径
            format: 日志格式
            max_size: 单个日志文件最大大小（字节）
            backup_count: 日志备份数量
        """
        for logger in self._loggers.values():
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            
            log_format = format or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(log_format)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
            if file:
                log_dir = os.path.dirname(file)
                if log_dir:
                    os.makedirs(log_dir, exist_ok=True)
                file_handler = RotatingFileHandler(
                    file,
                    maxBytes=max_size,
                    backupCount=backup_count,
                    encoding='utf-8'
                )
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            
            logger.setLevel(self._get_level(level))
    
    def debug(self, message: str, name: str = 'app'):
        """输出 DEBUG 级别日志"""
        self._loggers.get(name, self._get_default_logger()).debug(message)
    
    def info(self, message: str, name: str = 'app'):
        """输出 INFO 级别日志"""
        self._loggers.get(name, self._get_default_logger()).info(message)
    
    def warning(self, message: str, name: str = 'app'):
        """输出 WARNING 级别日志"""
        self._loggers.get(name, self._get_default_logger()).warning(message)
    
    def error(self, message: str, exc_info: bool = False, name: str = 'app'):
        """输出 ERROR 级别日志"""
        self._loggers.get(name, self._get_default_logger()).error(message, exc_info=exc_info)
    
    def critical(self, message: str, name: str = 'app'):
        """输出 CRITICAL 级别日志"""
        self._loggers.get(name, self._get_default_logger()).critical(message)
    
    def _get_default_logger(self) -> logging.Logger:
        if 'app' not in self._loggers:
            self._loggers['app'] = logging.getLogger('app')
        return self._loggers['app']
    
    @staticmethod
    def _get_level(level: str) -> int:
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return levels.get(level.upper(), logging.INFO)
