# 架构设计文档

## 1. 设计原则

### 1.1 第一性原理分析

本项目的核心本质是**建立浏览器脚本与本地应用之间的双向通信桥梁**。从这个本质出发，我们需要解决以下基础问题：

| 基础问题 | 解决方案 |
|----------|----------|
| 如何实现跨环境通信 | HTTP 协议作为通用通信层 |
| 如何保证通信安全 | 本地回环地址 + 可配置端口 |
| 如何持久化配置 | JSON 文件存储 |
| 如何提供用户交互 | GUI 界面 + 脚本 UI 双入口 |

### 1.2 奥卡姆剃刀原则

在架构设计中，我们遵循"如无必要，勿增实体"的原则：

- **不引入数据库**：配置和数据量小，JSON 文件足够
- **不使用 WebSocket**：HTTP 轮询足以满足实时性需求
- **不引入 ORM**：直接操作 JSON，减少抽象层
- **不使用复杂框架**：Flask + Tkinter 足够轻量

### 1.3 分层架构设计

采用经典的三层架构 + 工具层设计：

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  ┌─────────────────────┐    ┌─────────────────────┐       │
│  │   GUI (Tkinter)     │    │  Tampermonkey UI    │       │
│  └─────────────────────┘    └─────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Controller Layer                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  接收请求、参数验证、调用 Service、返回响应           │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  业务逻辑处理、数据转换、调用 Utils、状态管理         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Utils Layer                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Excel 处理、JSON 处理、HTTP 请求、文件操作、日志     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 2. 模块设计

### 2.1 模块依赖关系

```
main.py
    │
    ├── src/gui/main_window.py
    │       │
    │       ├── src/controller/server_controller.py
    │       │       │
    │       │       └── src/service/server_service.py
    │       │               │
    │       │               └── src/utils/logger.py
    │       │
    │       ├── src/controller/config_controller.py
    │       │       │
    │       │       └── src/service/config_service.py
    │       │               │
    │       │               ├── src/config/config_manager.py
    │       │               └── src/utils/json_util.py
    │       │
    │       └── src/controller/data_controller.py
    │               │
    │               └── src/service/data_service.py
    │                       │
    │                       ├── src/utils/excel_util.py
    │                       └── src/utils/file_util.py
    │
    └── src/server/app.py
            │
            ├── src/server/routes/*.py
            │       │
            │       └── src/controller/*.py
            │
            └── src/server/middleware/*.py
```

### 2.2 核心模块职责

#### 2.2.1 GUI 模块 (src/gui/)

| 文件 | 职责 | 依赖 |
|------|------|------|
| main_window.py | 主窗口布局、事件绑定、状态更新 | controller/* |
| widgets/status_bar.py | 服务状态显示组件 | 无 |
| widgets/log_panel.py | 日志显示面板组件 | utils/logger.py |
| dialogs/settings_dialog.py | 配置设置对话框 | controller/config_controller.py |

#### 2.2.2 Controller 模块 (src/controller/)

| 文件 | 职责 | 依赖 |
|------|------|------|
| server_controller.py | 服务启停控制、端口管理 | service/server_service.py |
| config_controller.py | 配置读写控制、配置验证 | service/config_service.py |
| data_controller.py | 数据处理控制、导出控制 | service/data_service.py |

#### 2.2.3 Service 模块 (src/service/)

| 文件 | 职责 | 依赖 |
|------|------|------|
| server_service.py | Flask 应用生命周期管理、线程管理 | utils/logger.py |
| config_service.py | 配置加载、配置保存、配置缓存 | config/config_manager.py |
| data_service.py | 数据处理、Excel 生成、数据缓存 | utils/excel_util.py |

#### 2.2.4 Utils 模块 (src/utils/)

| 文件 | 职责 | 依赖 |
|------|------|------|
| excel_util.py | Excel 文件创建、数据写入、样式设置 | openpyxl |
| json_util.py | JSON 文件读写、格式化、验证 | 无 |
| http_util.py | HTTP 请求封装、响应处理 | requests |
| file_util.py | 文件操作、目录管理、路径处理 | 无 |
| logger.py | 日志配置、日志输出、日志级别管理 | logging |

#### 2.2.5 Config 模块 (src/config/)

| 文件 | 职责 | 依赖 |
|------|------|------|
| default_config.py | 内置默认配置定义 | 无 |
| config_manager.py | 配置文件管理、配置合并、配置迁移 | utils/json_util.py |

#### 2.2.6 Server 模块 (src/server/)

| 文件 | 职责 | 依赖 |
|------|------|------|
| app.py | Flask 应用工厂、蓝图注册 | flask |
| routes/health.py | 健康检查路由 | flask |
| routes/data.py | 数据处理路由 | controller/data_controller.py |
| routes/action.py | 操作执行路由 | controller/data_controller.py |
| middleware/cors.py | CORS 中间件 | flask |

## 3. 数据流设计

### 3.1 服务启动流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   用户点击   │────▶│  Controller │────▶│   Service   │
│  启动按钮   │     │  验证端口    │     │  创建应用   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  GUI 更新   │◀────│  Controller │◀────│  启动线程   │
│  状态显示   │     │  返回结果    │     │  运行服务   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 3.2 配置加载流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   应用启动   │────▶│ConfigManager│────▶│ 检查外置    │
│             │     │             │     │ 配置文件    │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                          ┌────────────────────┴────────────────────┐
                          ▼                                         ▼
                   ┌─────────────┐                           ┌─────────────┐
                   │  文件存在   │                           │  文件不存在  │
                   │  直接加载   │                           │  创建文件   │
                   └─────────────┘                           └─────────────┘
                          │                                         │
                          │                                         ▼
                          │                                  ┌─────────────┐
                          │                                  │ 使用内置    │
                          │                                  │ 默认配置    │
                          │                                  └─────────────┘
                          │                                         │
                          └────────────────────┬────────────────────┘
                                               ▼
                                        ┌─────────────┐
                                        │ 更新缓存    │
                                        │ 返回配置    │
                                        └─────────────┘
```

### 3.3 数据处理流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│Tampermonkey │────▶│ HTTP 接口   │────▶│ Controller  │
│  发送数据   │     │  接收请求   │     │  参数验证   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  返回响应   │◀────│ Controller  │◀────│   Service   │
│  结果通知   │     │  结果封装   │     │  处理数据   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │ ExcelUtil   │
                                        │ 导出文件    │
                                        └─────────────┘
```

## 4. 状态管理

### 4.1 应用状态

| 状态 | 说明 | 触发条件 |
|------|------|----------|
| STOPPED | 服务已停止 | 应用启动、服务关闭 |
| STARTING | 服务启动中 | 点击启动按钮 |
| RUNNING | 服务运行中 | 启动成功 |
| STOPPING | 服务停止中 | 点击停止按钮 |
| ERROR | 服务异常 | 启动/运行错误 |

### 4.2 配置缓存

```python
class ConfigCache:
    _instance = None
    _config = None
    _last_modified = None
    
    @classmethod
    def get_config(cls):
        if cls._config is None or cls._is_stale():
            cls._reload_config()
        return cls._config
    
    @classmethod
    def update_config(cls, new_config):
        cls._config = new_config
        cls._persist_config()
    
    @classmethod
    def clear(cls):
        cls._config = None
        cls._last_modified = None
```

### 4.3 数据缓存

```python
class DataCache:
    _instance = None
    _data_store = {}
    _max_size = 1000
    
    @classmethod
    def add_data(cls, key, data):
        if len(cls._data_store) >= cls._max_size:
            cls._evict_oldest()
        cls._data_store[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    @classmethod
    def get_data(cls, key):
        return cls._data_store.get(key, {}).get('data')
    
    @classmethod
    def clear(cls):
        cls._data_store.clear()
```

## 5. 错误处理

### 5.1 错误分类

| 错误类型 | 错误码 | 处理方式 |
|----------|--------|----------|
| 配置错误 | 1000-1999 | 日志记录 + 用户提示 |
| 服务错误 | 2000-2999 | 日志记录 + 自动恢复 |
| 数据错误 | 3000-3999 | 日志记录 + 返回错误响应 |
| 网络错误 | 4000-4999 | 日志记录 + 重试机制 |

### 5.2 错误响应格式

```json
{
    "success": false,
    "error": {
        "code": 3001,
        "message": "数据格式错误",
        "details": "字段 'name' 不能为空"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 6. 扩展设计

### 6.1 插件机制

框架预留插件扩展点：

```python
class PluginInterface:
    def on_data_received(self, data):
        pass
    
    def on_data_processed(self, result):
        pass
    
    def on_export_complete(self, file_path):
        pass

class PluginManager:
    _plugins = []
    
    @classmethod
    def register(cls, plugin):
        if isinstance(plugin, PluginInterface):
            cls._plugins.append(plugin)
    
    @classmethod
    def trigger(cls, event_name, *args, **kwargs):
        for plugin in cls._plugins:
            method = getattr(plugin, f'on_{event_name}', None)
            if method:
                method(*args, **kwargs)
```

### 6.2 路由扩展

新增路由只需：

1. 在 `src/server/routes/` 创建新文件
2. 定义蓝图并注册路由
3. 在 `src/server/app.py` 中注册蓝图

```python
from flask import Blueprint

custom_bp = Blueprint('custom', __name__)

@custom_bp.route('/custom/action', methods=['POST'])
def custom_action():
    pass
```

### 6.3 工具类扩展

新增工具类只需：

1. 在 `src/utils/` 创建新文件
2. 实现工具类方法
3. 在 `src/utils/__init__.py` 中导出

## 7. 安全设计

### 7.1 访问控制

| 措施 | 说明 |
|------|------|
| 本地绑定 | 服务仅监听 127.0.0.1 |
| 端口限制 | 可配置端口，避免冲突 |
| CORS 配置 | 仅允许特定来源访问 |

### 7.2 数据安全

| 措施 | 说明 |
|------|------|
| 输入验证 | 所有输入数据进行格式验证 |
| 路径限制 | 文件操作限制在指定目录 |
| 敏感数据 | 配置文件不存储敏感信息 |

## 8. 性能设计

### 8.1 并发处理

- 使用线程池处理并发请求
- 配置最大工作线程数
- 请求队列管理

### 8.2 资源管理

- 配置文件按需加载
- 数据缓存设置上限
- 定期清理过期数据

### 8.3 日志管理

- 日志文件大小限制
- 日志文件轮转
- 日志级别可配置
