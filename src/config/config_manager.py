import os
from typing import Dict, Any, Optional
from src.utils.json_util import JsonUtil
from src.config.default_config import DEFAULT_CONFIG


class ConfigManager:
    """
    配置管理器，负责配置的加载、保存和管理。
    
    功能：
    - 加载内置默认配置
    - 加载外置配置文件
    - 合并配置
    - 保存配置到文件
    - 配置项访问
    """
    
    CONFIG_FILE = "config.json"
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化配置管理器。
        
        参数：
            config_dir: 配置文件目录，默认为应用根目录
        """
        self.config_dir = config_dir or os.getcwd()
        self.config_path = os.path.join(self.config_dir, self.CONFIG_FILE)
        self._config = None
    
    def load(self) -> Dict[str, Any]:
        """
        加载配置。
        
        返回：
            配置字典
        
        流程：
        1. 加载内置默认配置
        2. 检查外置配置文件
        3. 如果存在，加载并合并
        4. 如果不存在，创建默认配置文件
        5. 返回最终配置
        """
        config = self._load_default_config()
        
        if os.path.exists(self.config_path):
            external_config = self._load_external_config()
            config = self._merge_config(config, external_config)
        else:
            self._create_default_config_file(config)
        
        self._config = config
        return config
    
    def save(self, config: Dict[str, Any]) -> bool:
        """
        保存配置到文件。
        
        参数：
            config: 配置字典
        
        返回：
            是否保存成功
        """
        try:
            JsonUtil.write(self.config_path, config)
            self._config = config
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get(self, key: Optional[str] = None, default: Any = None) -> Any:
        """
        获取配置值。
        
        参数：
            key: 配置键名，支持点分隔符（如 'server.port'）
                 如果为 None，返回整个配置
            default: 默认值
        
        返回：
            配置值
        """
        if self._config is None:
            self.load()
        
        if key is None:
            return self._config
        
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值。
        
        参数：
            key: 配置键名，支持点分隔符
            value: 配置值
        
        返回：
            是否设置成功
        """
        if self._config is None:
            self.load()
        
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        return self.save(self._config)
    
    def update(self, updates: Dict[str, Any]) -> bool:
        """
        批量更新配置。
        
        参数：
            updates: 配置更新字典
        
        返回：
            是否更新成功
        """
        if self._config is None:
            self.load()
        
        self._deep_update(self._config, updates)
        return self.save(self._config)
    
    def reset(self) -> bool:
        """
        重置为默认配置。
        
        返回：
            是否重置成功
        """
        default_config = self._load_default_config()
        result = self.save(default_config)
        self._config = default_config
        return result
    
    def reload(self) -> Dict[str, Any]:
        """
        重新加载配置。
        
        返回：
            重新加载后的配置字典
        """
        self._config = None
        return self.load()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """
        加载内置默认配置。
        
        返回：
            默认配置字典
        """
        import copy
        return copy.deepcopy(DEFAULT_CONFIG)
    
    def _load_external_config(self) -> Dict[str, Any]:
        """
        加载外置配置文件。
        
        返回：
            外置配置字典
        """
        try:
            return JsonUtil.read(self.config_path)
        except Exception as e:
            print(f"加载外置配置失败: {e}")
            return {}
    
    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并配置。
        
        参数：
            base: 基础配置
            override: 覆盖配置
        
        返回：
            合并后的配置
        """
        result = base.copy()
        self._deep_update(result, override)
        return result
    
    def _deep_update(self, target: Dict[str, Any], source: Dict[str, Any]):
        """
        深度更新字典。
        
        参数：
            target: 目标字典
            source: 源字典
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def _create_default_config_file(self, config: Dict[str, Any]):
        """
        创建默认配置文件。
        
        参数：
            config: 默认配置字典
        """
        self.save(config)
