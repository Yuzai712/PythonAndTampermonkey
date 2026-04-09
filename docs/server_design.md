# 本地服务器设计文档

## 1. 服务器概述

### 1.1 技术选型

| 组件 | 选型 | 版本 | 选型理由 |
|------|------|------|----------|
| Web 框架 | Flask | 3.0.x | 轻量级、易扩展、适合小型服务 |
| WSGI 服务器 | Werkzeug | 3.0.x | Flask 内置，开发调试方便 |
| GUI 框架 | Tkinter | 内置 | Python 标准库、跨平台、零依赖 |
| 线程管理 | threading | 内置 | 简单可靠、满足需求 |

### 1.2 服务器架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Application                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    GUI Layer                         │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │              MainWindow                      │   │   │
│  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ │   │   │
│  │  │  │ StatusBar │ │ LogPanel  │ │ ControlBar│ │   │   │
│  │  │  └───────────┘ └───────────┘ └───────────┘ │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                              │
│                              ▼                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                Controller Layer                      │   │
│  │  ┌───────────────┐ ┌───────────────┐ ┌───────────┐ │   │
│  │  │ServerController│ │ConfigController│ │DataCtrl  │ │   │
│  │  └───────────────┘ └───────────────┘ └───────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                              │
│                              ▼                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Service Layer                        │   │
│  │  ┌───────────────┐ ┌───────────────┐ ┌───────────┐ │   │
│  │  │ ServerService │ │ ConfigService │ │ DataService│ │   │
│  │  └───────────────┘ └───────────────┘ └───────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                              │
│                              ▼                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Flask Server                        │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │  Routes: /api/health, /api/data, /api/export│   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 2. GUI 模块设计

### 2.1 主窗口 (main_window.py)

```python
class MainWindow:
    """
    主窗口类，负责创建和管理应用程序主界面。
    
    功能：
    - 创建窗口布局
    - 管理子组件
    - 绑定事件处理
    - 更新界面状态
    """
    
    def __init__(self):
        """
        初始化主窗口。
        
        创建 Tkinter 根窗口，设置窗口属性，初始化子组件。
        """
        pass
    
    def create_widgets(self):
        """
        创建所有界面组件。
        
        包含：状态栏、控制栏、日志面板、设置区域。
        """
        pass
    
    def setup_layout(self):
        """
        设置组件布局。
        
        使用 grid 布局管理器，设置行列权重和组件位置。
        """
        pass
    
    def bind_events(self):
        """
        绑定事件处理函数。
        
        包括：窗口关闭事件、按钮点击事件、快捷键等。
        """
        pass
    
    def on_start_server(self):
        """
        启动服务器按钮点击事件处理。
        
        验证端口配置，调用 ServerController 启动服务，更新界面状态。
        """
        pass
    
    def on_stop_server(self):
        """
        停止服务器按钮点击事件处理。
        
        调用 ServerController 停止服务，更新界面状态，清空缓存。
        """
        pass
    
    def on_settings(self):
        """
        设置按钮点击事件处理。
        
        打开设置对话框，处理配置更新。
        """
        pass
    
    def update_status(self, status: str):
        """
        更新服务状态显示。
        
        参数：
            status: 状态字符串 (STOPPED/STARTING/RUNNING/STOPPING/ERROR)
        """
        pass
    
    def add_log(self, message: str, level: str = 'INFO'):
        """
        添加日志消息到日志面板。
        
        参数：
            message: 日志消息内容
            level: 日志级别 (INFO/WARNING/ERROR)
        """
        pass
    
    def on_closing(self):
        """
        窗口关闭事件处理。
        
        确认是否关闭，停止服务，保存配置，销毁窗口。
        """
        pass
    
    def run(self):
        """
        启动主事件循环。
        
        调用 Tkinter mainloop 方法，开始处理事件。
        """
        pass
```

### 2.2 状态栏组件 (widgets/status_bar.py)

```python
class StatusBar:
    """
    状态栏组件，显示服务器运行状态。
    
    功能：
    - 显示服务状态指示灯
    - 显示当前端口号
    - 显示运行时长
    """
    
    def __init__(self, parent):
        """
        初始化状态栏组件。
        
        参数：
            parent: 父容器组件
        """
        pass
    
    def create_widgets(self):
        """
        创建状态栏子组件。
        
        包含：状态标签、端口标签、运行时长标签。
        """
        pass
    
    def set_status(self, status: str):
        """
        设置服务状态。
        
        参数：
            status: 状态值 (STOPPED/RUNNING/ERROR)
        
        根据状态更新指示灯颜色和状态文本。
        """
        pass
    
    def set_port(self, port: int):
        """
        设置端口号显示。
        
        参数：
            port: 端口号
        """
        pass
    
    def set_uptime(self, seconds: int):
        """
        设置运行时长显示。
        
        参数：
            seconds: 运行秒数
        
        自动转换为 HH:MM:SS 格式显示。
        """
        pass
    
    def start_uptime_timer(self):
        """
        启动运行时长计时器。
        
        每秒更新一次运行时长显示。
        """
        pass
    
    def stop_uptime_timer(self):
        """
        停止运行时长计时器。
        """
        pass
```

### 2.3 日志面板组件 (widgets/log_panel.py)

```python
class LogPanel:
    """
    日志面板组件，显示应用程序运行日志。
    
    功能：
    - 显示日志消息
    - 按级别着色
    - 支持滚动查看
    - 支持清空日志
    """
    
    MAX_LINES = 500
    
    def __init__(self, parent):
        """
        初始化日志面板组件。
        
        参数：
            parent: 父容器组件
        """
        pass
    
    def create_widgets(self):
        """
        创建日志面板子组件。
        
        包含：文本显示区域、滚动条、清空按钮。
        """
        pass
    
    def add_log(self, message: str, level: str = 'INFO'):
        """
        添加日志消息。
        
        参数：
            message: 日志消息内容
            level: 日志级别
        
        根据级别设置文本颜色，自动滚动到最新消息。
        """
        pass
    
    def clear_logs(self):
        """
        清空所有日志消息。
        """
        pass
    
    def get_level_color(self, level: str) -> str:
        """
        获取日志级别对应的颜色。
        
        参数：
            level: 日志级别
        
        返回：
            颜色代码字符串
        """
        pass
    
    def trim_logs(self):
        """
        裁剪日志行数，保持不超过最大行数限制。
        """
        pass
```

### 2.4 设置对话框 (dialogs/settings_dialog.py)

```python
class SettingsDialog:
    """
    设置对话框，用于修改应用程序配置。
    
    功能：
    - 显示当前配置
    - 修改端口号
    - 修改缓存设置
    - 修改日志级别
    - 保存配置
    """
    
    def __init__(self, parent, config_controller):
        """
        初始化设置对话框。
        
        参数：
            parent: 父窗口
            config_controller: 配置控制器实例
        """
        pass
    
    def create_widgets(self):
        """
        创建对话框组件。
        
        包含：端口设置、缓存设置、日志设置、确定/取消按钮。
        """
        pass
    
    def load_current_config(self):
        """
        加载当前配置到界面。
        """
        pass
    
    def on_ok(self):
        """
        确定按钮点击事件处理。
        
        验证输入，保存配置，关闭对话框。
        """
        pass
    
    def on_cancel(self):
        """
        取消按钮点击事件处理。
        
        放弃修改，关闭对话框。
        """
        pass
    
    def validate_input(self) -> bool:
        """
        验证用户输入。
        
        返回：
            验证是否通过
        """
        pass
    
    def show(self):
        """
        显示对话框。
        
        以模态方式显示对话框，等待用户操作。
        """
        pass
```

## 3. Controller 模块设计

### 3.1 服务器控制器 (server_controller.py)

```python
class ServerController:
    """
    服务器控制器，处理服务器启停相关的业务逻辑。
    
    职责：
    - 接收 GUI 层的服务启停请求
    - 调用 Service 层执行具体操作
    - 返回操作结果给 GUI 层
    """
    
    def __init__(self, server_service):
        """
        初始化服务器控制器。
        
        参数：
            server_service: 服务器服务实例
        """
        pass
    
    def start_server(self, port: int) -> dict:
        """
        启动服务器。
        
        参数：
            port: 监听端口号
        
        返回：
            操作结果字典，包含 success 和 message 字段
        
        流程：
        1. 验证端口有效性
        2. 检查服务是否已运行
        3. 调用 ServerService 启动服务
        4. 返回操作结果
        """
        pass
    
    def stop_server(self) -> dict:
        """
        停止服务器。
        
        返回：
            操作结果字典
        
        流程：
        1. 检查服务是否在运行
        2. 调用 ServerService 停止服务
        3. 清空缓存数据
        4. 返回操作结果
        """
        pass
    
    def get_server_status(self) -> dict:
        """
        获取服务器状态。
        
        返回：
            状态字典，包含 status, port, uptime 等字段
        """
        pass
    
    def is_server_running(self) -> bool:
        """
        检查服务器是否在运行。
        
        返回：
            是否运行中
        """
        pass
    
    def validate_port(self, port: int) -> bool:
        """
        验证端口号有效性。
        
        参数：
            port: 端口号
        
        返回：
            是否有效
        
        验证规则：
        - 端口范围：1024-65535
        - 端口未被占用
        """
        pass
```

### 3.2 配置控制器 (config_controller.py)

```python
class ConfigController:
    """
    配置控制器，处理配置相关的业务逻辑。
    
    职责：
    - 接收配置读写请求
    - 验证配置有效性
    - 调用 Service 层执行配置操作
    """
    
    def __init__(self, config_service):
        """
        初始化配置控制器。
        
        参数：
            config_service: 配置服务实例
        """
        pass
    
    def get_config(self) -> dict:
        """
        获取当前配置。
        
        返回：
            配置字典
        """
        pass
    
    def update_config(self, updates: dict) -> dict:
        """
        更新配置。
        
        参数：
            updates: 配置更新字典
        
        返回：
            操作结果字典
        
        流程：
        1. 验证配置项有效性
        2. 合并配置
        3. 调用 ConfigService 保存配置
        4. 返回操作结果
        """
        pass
    
    def reset_config(self) -> dict:
        """
        重置配置为默认值。
        
        返回：
            操作结果字典
        """
        pass
    
    def get_config_value(self, key: str) -> any:
        """
        获取单个配置项的值。
        
        参数：
            key: 配置项键名，支持点分隔符（如 'server.port'）
        
        返回：
            配置值
        """
        pass
    
    def set_config_value(self, key: str, value: any) -> dict:
        """
        设置单个配置项的值。
        
        参数：
            key: 配置项键名
            value: 配置值
        
        返回：
            操作结果字典
        """
        pass
```

### 3.3 数据控制器 (data_controller.py)

```python
class DataController:
    """
    数据控制器，处理数据相关的业务逻辑。
    
    职责：
    - 接收数据处理请求
    - 验证数据有效性
    - 调用 Service 层执行数据处理
    - 返回处理结果
    """
    
    def __init__(self, data_service):
        """
        初始化数据控制器。
        
        参数：
            data_service: 数据服务实例
        """
        pass
    
    def receive_intercept_data(self, data: dict) -> dict:
        """
        接收拦截数据。
        
        参数：
            data: 拦截的数据字典
        
        返回：
            操作结果字典，包含数据 ID
        
        流程：
        1. 验证数据格式
        2. 调用 DataService 存储数据
        3. 返回数据 ID
        """
        pass
    
    def get_cached_data(self, page: int = 1, size: int = 20, filters: dict = None) -> dict:
        """
        获取缓存数据列表。
        
        参数：
            page: 页码
            size: 每页数量
            filters: 过滤条件
        
        返回：
            分页数据字典
        """
        pass
    
    def get_data_detail(self, data_id: str) -> dict:
        """
        获取数据详情。
        
        参数：
            data_id: 数据 ID
        
        返回：
            数据详情字典
        """
        pass
    
    def clear_cache(self) -> dict:
        """
        清空缓存数据。
        
        返回：
            操作结果字典，包含清空数量
        """
        pass
    
    def export_to_excel(self, format_config: dict = None, filters: dict = None) -> dict:
        """
        导出数据到 Excel。
        
        参数：
            format_config: 格式配置
            filters: 过滤条件
        
        返回：
            操作结果字典，包含文件路径
        """
        pass
    
    def validate_intercept_data(self, data: dict) -> tuple:
        """
        验证拦截数据格式。
        
        参数：
            data: 待验证的数据
        
        返回：
            (是否有效, 错误消息) 元组
        """
        pass
```

## 4. Service 模块设计

### 4.1 服务器服务 (server_service.py)

```python
class ServerService:
    """
    服务器服务，处理服务器生命周期管理。
    
    职责：
    - 创建和销毁 Flask 应用
    - 管理服务线程
    - 处理服务状态变更
    """
    
    def __init__(self, app_factory, config_service):
        """
        初始化服务器服务。
        
        参数：
            app_factory: Flask 应用工厂
            config_service: 配置服务实例
        """
        pass
    
    def start(self, port: int) -> bool:
        """
        启动服务器。
        
        参数：
            port: 监听端口号
        
        返回：
            是否启动成功
        
        流程：
        1. 创建 Flask 应用实例
        2. 创建服务线程
        3. 启动服务线程
        4. 等待服务就绪
        """
        pass
    
    def stop(self) -> bool:
        """
        停止服务器。
        
        返回：
            是否停止成功
        
        流程：
        1. 设置停止标志
        2. 发送停止请求
        3. 等待线程结束
        4. 清理资源
        """
        pass
    
    def is_running(self) -> bool:
        """
        检查服务是否在运行。
        
        返回：
            是否运行中
        """
        pass
    
    def get_status(self) -> dict:
        """
        获取服务状态。
        
        返回：
            状态字典
        """
        pass
    
    def _run_server(self, app, port: int):
        """
        在线程中运行服务器。
        
        参数：
            app: Flask 应用实例
            port: 端口号
        
        内部方法，在独立线程中执行。
        """
        pass
    
    def _wait_for_server_ready(self, timeout: int = 10) -> bool:
        """
        等待服务器就绪。
        
        参数：
            timeout: 超时时间（秒）
        
        返回：
            是否就绪
        """
        pass
```

### 4.2 配置服务 (config_service.py)

```python
class ConfigService:
    """
    配置服务，处理配置的加载、保存和缓存。
    
    职责：
    - 从文件加载配置
    - 保存配置到文件
    - 管理配置缓存
    - 配置变更通知
    """
    
    def __init__(self, config_manager):
        """
        初始化配置服务。
        
        参数：
            config_manager: 配置管理器实例
        """
        pass
    
    def load_config(self) -> dict:
        """
        加载配置。
        
        返回：
            配置字典
        
        流程：
        1. 从 ConfigManager 加载配置
        2. 更新缓存
        3. 返回配置
        """
        pass
    
    def save_config(self, config: dict) -> bool:
        """
        保存配置。
        
        参数：
            config: 配置字典
        
        返回：
            是否保存成功
        """
        pass
    
    def get_cached_config(self) -> dict:
        """
        获取缓存的配置。
        
        返回：
            配置字典
        """
        pass
    
    def update_config(self, updates: dict) -> bool:
        """
        更新配置。
        
        参数：
            updates: 配置更新字典
        
        返回：
            是否更新成功
        """
        pass
    
    def reset_to_default(self) -> bool:
        """
        重置为默认配置。
        
        返回：
            是否重置成功
        """
        pass
    
    def get_value(self, key: str, default: any = None) -> any:
        """
        获取配置值。
        
        参数：
            key: 配置键名
            default: 默认值
        
        返回：
            配置值
        """
        pass
    
    def set_value(self, key: str, value: any) -> bool:
        """
        设置配置值。
        
        参数：
            key: 配置键名
            value: 配置值
        
        返回：
            是否设置成功
        """
        pass
    
    def clear_cache(self):
        """
        清空配置缓存。
        """
        pass
```

### 4.3 数据服务 (data_service.py)

```python
class DataService:
    """
    数据服务，处理数据的存储、查询和导出。
    
    职责：
    - 存储拦截数据
    - 查询缓存数据
    - 导出数据到 Excel
    - 管理数据缓存
    """
    
    def __init__(self, excel_util, file_util):
        """
        初始化数据服务。
        
        参数：
            excel_util: Excel 工具实例
            file_util: 文件工具实例
        """
        pass
    
    def store_data(self, data: dict) -> str:
        """
        存储数据。
        
        参数：
            data: 数据字典
        
        返回：
            数据 ID
        """
        pass
    
    def get_data(self, data_id: str) -> dict:
        """
        获取数据。
        
        参数：
            data_id: 数据 ID
        
        返回：
            数据字典
        """
        pass
    
    def get_data_list(self, page: int, size: int, filters: dict = None) -> dict:
        """
        获取数据列表。
        
        参数：
            page: 页码
            size: 每页数量
            filters: 过滤条件
        
        返回：
            分页数据字典
        """
        pass
    
    def clear_all_data(self) -> int:
        """
        清空所有数据。
        
        返回：
            清空的数据数量
        """
        pass
    
    def export_to_excel(self, format_config: dict = None, filters: dict = None) -> str:
        """
        导出数据到 Excel。
        
        参数：
            format_config: 格式配置
            filters: 过滤条件
        
        返回：
            导出文件路径
        """
        pass
    
    def get_data_count(self, filters: dict = None) -> int:
        """
        获取数据数量。
        
        参数：
            filters: 过滤条件
        
        返回：
            数据数量
        """
        pass
    
    def _generate_data_id(self) -> str:
        """
        生成数据 ID。
        
        返回：
            唯一的数据 ID
        """
        pass
    
    def _apply_filters(self, data: dict, filters: dict) -> bool:
        """
        应用过滤条件。
        
        参数：
            data: 数据字典
            filters: 过滤条件
        
        返回：
            是否符合条件
        """
        pass
```

## 5. Flask 应用设计

### 5.1 应用工厂 (app.py)

```python
def create_app(config: dict) -> Flask:
    """
    创建 Flask 应用实例。
    
    参数：
        config: 配置字典
    
    返回：
        Flask 应用实例
    
    流程：
    1. 创建 Flask 应用
    2. 加载配置
    3. 注册蓝图
    4. 配置中间件
    5. 返回应用实例
    """
    pass

def register_blueprints(app: Flask):
    """
    注册所有蓝图。
    
    参数：
        app: Flask 应用实例
    
    注册蓝图：
    - health_bp: 健康检查路由
    - data_bp: 数据处理路由
    - action_bp: 操作执行路由
    - config_bp: 配置管理路由
    - export_bp: 导出路由
    """
    pass

def configure_middleware(app: Flask):
    """
    配置中间件。
    
    参数：
        app: Flask 应用实例
    
    配置：
    - CORS 中间件
    - 请求日志中间件
    - 错误处理中间件
    """
    pass
```

### 5.2 路由模块

#### 健康检查路由 (routes/health.py)

```python
health_bp = Blueprint('health', __name__, url_prefix='/api')

@health_bp.route('/health', methods=['GET'])
def check_health():
    """
    检查服务健康状态。
    
    返回：
        JSON 响应，包含服务状态信息
    """
    pass

@health_bp.route('/health/ping', methods=['GET'])
def ping():
    """
    心跳检测接口。
    
    返回：
        JSON 响应，包含 pong 标识
    """
    pass
```

#### 数据处理路由 (routes/data.py)

```python
data_bp = Blueprint('data', __name__, url_prefix='/api/data')

@data_bp.route('/intercept', methods=['POST'])
def receive_intercept():
    """
    接收拦截数据。
    
    请求体：
        JSON 格式的拦截数据
    
    返回：
        JSON 响应，包含数据 ID
    """
    pass

@data_bp.route('/intercept/batch', methods=['POST'])
def receive_intercept_batch():
    """
    批量接收拦截数据。
    
    请求体：
        JSON 格式的数据数组
    
    返回：
        JSON 响应，包含接收统计
    """
    pass

@data_bp.route('/cache', methods=['GET'])
def get_cached_data():
    """
    获取缓存数据列表。
    
    查询参数：
        page: 页码
        size: 每页数量
        source_url: 来源 URL 过滤
    
    返回：
        JSON 响应，包含分页数据
    """
    pass

@data_bp.route('/cache/<data_id>', methods=['GET'])
def get_data_detail(data_id):
    """
    获取数据详情。
    
    路径参数：
        data_id: 数据 ID
    
    返回：
        JSON 响应，包含数据详情
    """
    pass

@data_bp.route('/cache', methods=['DELETE'])
def clear_cache():
    """
    清空缓存数据。
    
    返回：
        JSON 响应，包含清空数量
    """
    pass
```

#### 导出路由 (routes/export.py)

```python
export_bp = Blueprint('export', __name__, url_prefix='/api/export')

@export_bp.route('/excel', methods=['POST'])
def export_excel():
    """
    导出数据到 Excel。
    
    请求体：
        JSON 格式的导出配置
    
    返回：
        JSON 响应，包含文件路径
    """
    pass

@export_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    下载导出文件。
    
    路径参数：
        filename: 文件名
    
    返回：
        文件流
    """
    pass

@export_bp.route('/history', methods=['GET'])
def get_export_history():
    """
    获取导出历史。
    
    查询参数：
        page: 页码
        size: 每页数量
    
    返回：
        JSON 响应，包含导出历史列表
    """
    pass
```

### 5.3 中间件 (middleware/cors.py)

```python
def init_cors(app: Flask):
    """
    初始化 CORS 中间件。
    
    参数：
        app: Flask 应用实例
    
    配置：
    - 允许的来源
    - 允许的方法
    - 允许的头
    """
    pass

@staticmethod
def add_cors_headers(response):
    """
    添加 CORS 响应头。
    
    参数：
        response: Flask 响应对象
    
    返回：
        添加了 CORS 头的响应对象
    """
    pass
```

## 6. 线程管理

### 6.1 服务线程

```python
import threading
import time

class ServerThread(threading.Thread):
    """
    服务器线程类，在独立线程中运行 Flask 服务。
    """
    
    def __init__(self, app: Flask, host: str, port: int):
        """
        初始化服务器线程。
        
        参数：
            app: Flask 应用实例
            host: 主机地址
            port: 端口号
        """
        super().__init__(daemon=True)
        self.app = app
        self.host = host
        self.port = port
        self.stop_event = threading.Event()
        self.server = None
    
    def run(self):
        """
        运行服务器。
        
        使用 Werkzeug 开发服务器运行 Flask 应用。
        """
        pass
    
    def stop(self):
        """
        停止服务器。
        
        设置停止事件，关闭服务器。
        """
        pass
    
    def is_running(self) -> bool:
        """
        检查线程是否在运行。
        
        返回：
            是否运行中
        """
        pass
```

### 6.2 线程安全的数据缓存

```python
import threading
from collections import OrderedDict
from datetime import datetime

class ThreadSafeCache:
    """
    线程安全的数据缓存。
    
    特性：
    - 线程安全的读写操作
    - LRU 淘汰策略
    - 最大容量限制
    """
    
    def __init__(self, max_size: int = 1000):
        """
        初始化缓存。
        
        参数：
            max_size: 最大容量
        """
        self.max_size = max_size
        self._cache = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: str) -> any:
        """
        获取缓存值。
        
        参数：
            key: 缓存键
        
        返回：
            缓存值，不存在返回 None
        """
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                return self._cache[key]
            return None
    
    def set(self, key: str, value: any):
        """
        设置缓存值。
        
        参数：
            key: 缓存键
            value: 缓存值
        """
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            
            while len(self._cache) > self.max_size:
                self._cache.popitem(last=False)
    
    def delete(self, key: str) -> bool:
        """
        删除缓存值。
        
        参数：
            key: 缓存键
        
        返回：
            是否删除成功
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> int:
        """
        清空缓存。
        
        返回：
            清空的数据数量
        """
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count
    
    def size(self) -> int:
        """
        获取缓存大小。
        
        返回：
            当前缓存数量
        """
        with self._lock:
            return len(self._cache)
    
    def keys(self) -> list:
        """
        获取所有缓存键。
        
        返回：
            缓存键列表
        """
        with self._lock:
            return list(self._cache.keys())
    
    def values(self) -> list:
        """
        获取所有缓存值。
        
        返回：
            缓存值列表
        """
        with self._lock:
            return list(self._cache.values())
```

## 7. 依赖注入

### 7.1 服务容器

```python
class ServiceContainer:
    """
    服务容器，管理服务的创建和依赖注入。
    
    特性：
    - 单例模式管理服务实例
    - 懒加载服务
    - 依赖自动注入
    """
    
    _instance = None
    _services = {}
    
    @classmethod
    def get_instance(cls):
        """
        获取服务容器单例。
        
        返回：
            服务容器实例
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register(self, name: str, factory: callable):
        """
        注册服务工厂。
        
        参数：
            name: 服务名称
            factory: 服务工厂函数
        """
        self._services[name] = {'factory': factory, 'instance': None}
    
    def get(self, name: str) -> any:
        """
        获取服务实例。
        
        参数：
            name: 服务名称
        
        返回：
            服务实例
        """
        if name not in self._services:
            raise ValueError(f"Service '{name}' not registered")
        
        service = self._services[name]
        if service['instance'] is None:
            service['instance'] = service['factory']()
        return service['instance']
    
    def reset(self):
        """
        重置所有服务实例。
        """
        for service in self._services.values():
            service['instance'] = None
```

### 7.2 服务初始化

```python
def initialize_services():
    """
    初始化所有服务。
    
    按依赖顺序创建服务实例，注册到服务容器。
    """
    container = ServiceContainer.get_instance()
    
    container.register('config_manager', lambda: ConfigManager())
    container.register('json_util', lambda: JsonUtil())
    container.register('file_util', lambda: FileUtil())
    container.register('excel_util', lambda: ExcelUtil())
    container.register('logger', lambda: Logger())
    
    container.register('config_service', 
        lambda: ConfigService(container.get('config_manager')))
    
    container.register('data_service',
        lambda: DataService(container.get('excel_util'), container.get('file_util')))
    
    container.register('server_service',
        lambda: ServerService(create_app, container.get('config_service')))
    
    container.register('server_controller',
        lambda: ServerController(container.get('server_service')))
    
    container.register('config_controller',
        lambda: ConfigController(container.get('config_service')))
    
    container.register('data_controller',
        lambda: DataController(container.get('data_service')))
```

## 8. 启动流程

```python
def main():
    """
    应用程序入口函数。
    
    流程：
    1. 初始化服务容器
    2. 加载配置
    3. 创建主窗口
    4. 启动 GUI 事件循环
    """
    initialize_services()
    
    config_service = ServiceContainer.get_instance().get('config_service')
    config = config_service.load_config()
    
    root = tk.Tk()
    main_window = MainWindow(root, config)
    main_window.run()

if __name__ == '__main__':
    main()
```
