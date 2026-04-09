# 配置管理文档

## 1. 配置概述

### 1.1 配置管理原则

| 原则 | 说明 |
|------|------|
| 内置默认 | 应用内置默认配置，确保开箱即用 |
| 外置优先 | 外置配置文件优先级高于内置配置 |
| 热更新 | 部分配置支持运行时更新，无需重启 |
| 持久化 | 所有配置变更持久化到 JSON 文件 |

### 1.2 配置加载流程

```
┌─────────────────────────────────────────────────────────────┐
│                      应用启动                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              检查外置配置文件是否存在                         │
│              (config.json)                                   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│     文件存在             │     │     文件不存在           │
│     直接加载             │     │     创建新文件           │
└─────────────────────────┘     └─────────────────────────┘
              │                               │
              │                               ▼
              │                 ┌─────────────────────────┐
              │                 │   使用内置默认配置       │
              │                 │   创建外置配置文件       │
              │                 └─────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  更新配置缓存                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  返回配置数据                                │
└─────────────────────────────────────────────────────────────┘
```

## 2. 配置文件结构

### 2.1 完整配置示例

```json
{
    "server": {
        "host": "127.0.0.1",
        "port": 8080,
        "debug": false,
        "threaded": true
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
        "allow_credentials": true
    },
    "ui": {
        "window": {
            "width": 600,
            "height": 500,
            "resizable": true
        },
        "theme": "default",
        "font_family": "Arial",
        "font_size": 10
    }
}
```

### 2.2 配置项说明

#### server 配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| host | string | "127.0.0.1" | 服务器监听地址 |
| port | integer | 8080 | 服务器监听端口 |
| debug | boolean | false | 是否启用调试模式 |
| threaded | boolean | true | 是否启用多线程 |

#### cache 配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| max_size | integer | 1000 | 最大缓存条数 |
| expire_time | integer | 3600 | 缓存过期时间（秒） |
| cleanup_interval | integer | 300 | 清理间隔（秒） |

#### export 配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| output_dir | string | "./exports" | 导出文件目录 |
| default_format | string | "xlsx" | 默认导出格式 |
| filename_template | string | "export_{timestamp}" | 文件名模板 |
| max_history | integer | 50 | 最大历史记录数 |

#### logging 配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| level | string | "INFO" | 日志级别 |
| file | string | "./logs/app.log" | 日志文件路径 |
| max_size | integer | 10485760 | 单个日志文件最大大小（字节） |
| backup_count | integer | 5 | 日志备份数量 |
| format | string | 见示例 | 日志格式 |

#### cors 配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| allowed_origins | array | ["*"] | 允许的来源 |
| allowed_methods | array | ["GET", "POST", "PUT", "DELETE"] | 允许的方法 |
| allowed_headers | array | ["Content-Type", "Authorization"] | 允许的头 |
| allow_credentials | boolean | true | 是否允许凭证 |

#### ui 配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| window.width | integer | 600 | 窗口宽度 |
| window.height | integer | 500 | 窗口高度 |
| window.resizable | boolean | true | 是否可调整大小 |
| theme | string | "default" | 界面主题 |
| font_family | string | "Arial" | 字体 |
| font_size | integer | 10 | 字号 |

## 3. 内置默认配置

### 3.1 default_config.py

```python
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
```

## 4. 配置管理器

### 4.1 ConfigManager 类

```python
import os
import json
from typing import Any, Dict, Optional

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
    
    def __init__(self, config_dir: str = None):
        """
        初始化配置管理器。
        
        参数：
            config_dir: 配置文件目录，默认为应用根目录
        """
        self.config_dir = config_dir or os.getcwd()
        self.config_path = os.path.join(self.config_dir, self.CONFIG_FILE)
        self._config = None
    
    def load(self) -> Dict:
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
    
    def save(self, config: Dict) -> bool:
        """
        保存配置到文件。
        
        参数：
            config: 配置字典
        
        返回：
            是否保存成功
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            self._config = config
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get(self, key: str = None, default: Any = None) -> Any:
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
    
    def update(self, updates: Dict) -> bool:
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
        return self.save(default_config)
    
    def reload(self) -> Dict:
        """
        重新加载配置。
        
        返回：
            重新加载后的配置字典
        """
        self._config = None
        return self.load()
    
    def _load_default_config(self) -> Dict:
        """
        加载内置默认配置。
        
        返回：
            默认配置字典
        """
        from src.config.default_config import DEFAULT_CONFIG
        return DEFAULT_CONFIG.copy()
    
    def _load_external_config(self) -> Dict:
        """
        加载外置配置文件。
        
        返回：
            外置配置字典
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载外置配置失败: {e}")
            return {}
    
    def _merge_config(self, base: Dict, override: Dict) -> Dict:
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
    
    def _deep_update(self, target: Dict, source: Dict):
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
    
    def _create_default_config_file(self, config: Dict):
        """
        创建默认配置文件。
        
        参数：
            config: 默认配置字典
        """
        self.save(config)
```

## 5. 配置验证

### 5.1 配置验证器

```python
from typing import Dict, List, Tuple

class ConfigValidator:
    """
    配置验证器，验证配置项的有效性。
    """
    
    VALIDATION_RULES = {
        'server.port': {
            'type': int,
            'min': 1024,
            'max': 65535,
            'message': '端口号必须在 1024-65535 之间'
        },
        'server.host': {
            'type': str,
            'pattern': r'^[\d.]+$|^localhost$',
            'message': '主机地址格式无效'
        },
        'cache.max_size': {
            'type': int,
            'min': 1,
            'max': 10000,
            'message': '缓存大小必须在 1-10000 之间'
        },
        'cache.expire_time': {
            'type': int,
            'min': 60,
            'max': 86400,
            'message': '过期时间必须在 60-86400 秒之间'
        },
        'logging.level': {
            'type': str,
            'choices': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            'message': '日志级别必须是 DEBUG/INFO/WARNING/ERROR/CRITICAL 之一'
        }
    }
    
    @classmethod
    def validate(cls, config: Dict) -> Tuple[bool, List[str]]:
        """
        验证配置。
        
        参数：
            config: 配置字典
        
        返回：
            (是否有效, 错误消息列表) 元组
        """
        errors = []
        
        for key, rule in cls.VALIDATION_RULES.items():
            value = cls._get_nested_value(config, key)
            if value is None:
                continue
            
            error = cls._validate_value(key, value, rule)
            if error:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    @classmethod
    def _get_nested_value(cls, config: Dict, key: str) -> Any:
        """
        获取嵌套配置值。
        
        参数：
            config: 配置字典
            key: 配置键名
        
        返回：
            配置值
        """
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return value
    
    @classmethod
    def _validate_value(cls, key: str, value: Any, rule: Dict) -> str:
        """
        验证单个配置值。
        
        参数：
            key: 配置键名
            value: 配置值
            rule: 验证规则
        
        返回：
            错误消息，验证通过返回 None
        """
        if 'type' in rule and not isinstance(value, rule['type']):
            return f"{key}: 类型错误，期望 {rule['type'].__name__}"
        
        if 'min' in rule and value < rule['min']:
            return f"{key}: {rule['message']}"
        
        if 'max' in rule and value > rule['max']:
            return f"{key}: {rule['message']}"
        
        if 'choices' in rule and value not in rule['choices']:
            return f"{key}: {rule['message']}"
        
        if 'pattern' in rule:
            import re
            if not re.match(rule['pattern'], str(value)):
                return f"{key}: {rule['message']}"
        
        return None
```

## 6. 配置热更新

### 6.1 可热更新配置项

| 配置项 | 是否支持热更新 | 说明 |
|--------|----------------|------|
| server.port | 否 | 需要重启服务 |
| server.host | 否 | 需要重启服务 |
| server.debug | 是 | 立即生效 |
| cache.max_size | 是 | 立即生效 |
| cache.expire_time | 是 | 立即生效 |
| logging.level | 是 | 立即生效 |
| export.* | 是 | 立即生效 |
| ui.* | 是 | 立即生效 |

### 6.2 配置变更通知

```python
from typing import Callable, Dict, List

class ConfigObserver:
    """
    配置观察者，监听配置变更并通知订阅者。
    """
    
    _observers: Dict[str, List[Callable]] = {}
    
    @classmethod
    def subscribe(cls, key: str, callback: Callable):
        """
        订阅配置变更。
        
        参数：
            key: 配置键名，支持通配符 '*'
            callback: 回调函数，接收 (key, old_value, new_value) 参数
        """
        if key not in cls._observers:
            cls._observers[key] = []
        cls._observers[key].append(callback)
    
    @classmethod
    def unsubscribe(cls, key: str, callback: Callable):
        """
        取消订阅。
        
        参数：
            key: 配置键名
            callback: 回调函数
        """
        if key in cls._observers:
            cls._observers[key].remove(callback)
    
    @classmethod
    def notify(cls, key: str, old_value: Any, new_value: Any):
        """
        通知配置变更。
        
        参数：
            key: 配置键名
            old_value: 旧值
            new_value: 新值
        """
        if key in cls._observers:
            for callback in cls._observers[key]:
                callback(key, old_value, new_value)
        
        if '*' in cls._observers:
            for callback in cls._observers['*']:
                callback(key, old_value, new_value)
```

## 7. 配置迁移

### 7.1 版本迁移策略

```python
class ConfigMigration:
    """
    配置迁移器，处理不同版本配置的兼容性。
    """
    
    MIGRATIONS = {
        '1.0.0': None,
        '1.1.0': 'migrate_1_0_to_1_1',
        '1.2.0': 'migrate_1_1_to_1_2'
    }
    
    @classmethod
    def migrate(cls, config: Dict, from_version: str, to_version: str) -> Dict:
        """
        迁移配置。
        
        参数：
            config: 配置字典
            from_version: 源版本
            to_version: 目标版本
        
        返回：
            迁移后的配置
        """
        versions = list(cls.MIGRATIONS.keys())
        start_idx = versions.index(from_version) if from_version in versions else -1
        end_idx = versions.index(to_version) if to_version in versions else len(versions) - 1
        
        for i in range(start_idx + 1, end_idx + 1):
            version = versions[i]
            migration_func = cls.MIGRATIONS.get(version)
            if migration_func:
                config = getattr(cls, migration_func)(config)
        
        return config
    
    @classmethod
    def migrate_1_0_to_1_1(cls, config: Dict) -> Dict:
        """
        从 1.0.0 迁移到 1.1.0。
        
        变更：
        - 添加 cache.cleanup_interval 配置项
        """
        if 'cache' not in config:
            config['cache'] = {}
        if 'cleanup_interval' not in config['cache']:
            config['cache']['cleanup_interval'] = 300
        return config
    
    @classmethod
    def migrate_1_1_to_1_2(cls, config: Dict) -> Dict:
        """
        从 1.1.0 迁移到 1.2.0。
        
        变更：
        - 添加 cors 配置节
        """
        if 'cors' not in config:
            config['cors'] = {
                'allowed_origins': ['*'],
                'allowed_methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'allowed_headers': ['Content-Type', 'Authorization'],
                'allow_credentials': True
            }
        return config
```

## 8. 配置使用示例

### 8.1 在服务中使用配置

```python
from src.config.config_manager import ConfigManager

class ServerService:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()
    
    def start(self):
        port = self.config_manager.get('server.port')
        host = self.config_manager.get('server.host')
        
        print(f"启动服务器: {host}:{port}")
```

### 8.2 在 GUI 中修改配置

```python
from src.config.config_manager import ConfigManager

class SettingsDialog:
    def __init__(self):
        self.config_manager = ConfigManager()
    
    def save_settings(self):
        new_port = self.port_entry.get()
        
        if self.config_manager.set('server.port', int(new_port)):
            print("配置保存成功")
        else:
            print("配置保存失败")
```

### 8.3 监听配置变更

```python
from src.config.config_manager import ConfigManager
from src.config.config_observer import ConfigObserver

def on_log_level_change(key, old_value, new_value):
    print(f"日志级别从 {old_value} 变更为 {new_value}")
    update_logger_level(new_value)

ConfigObserver.subscribe('logging.level', on_log_level_change)
```
