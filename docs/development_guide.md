# 开发指南文档

## 1. 开发环境搭建

### 1.1 系统要求

| 要求 | 说明 |
|------|------|
| Python 版本 | 3.8+ |
| 操作系统 | Windows / macOS / Linux |
| 内存 | 最低 512MB |
| 磁盘空间 | 最低 100MB |

### 1.2 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd tampermonkey-framework

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 运行应用
python main.py
```

### 1.3 依赖清单

```
Flask>=3.0.0
openpyxl>=3.1.0
requests>=2.31.0
```

## 2. 项目结构说明

### 2.1 目录结构

```
tampermonkey-framework/
├── main.py                     # 应用入口
├── requirements.txt            # 依赖清单
├── config.json                 # 外置配置文件
├── README.md                   # 项目说明
├── docs/                       # 文档目录
│   ├── architecture.md
│   ├── api_design.md
│   ├── userscript_design.md
│   ├── server_design.md
│   ├── configuration.md
│   └── development_guide.md
├── src/                        # 源代码目录
│   ├── __init__.py
│   ├── server/                 # Flask 服务器模块
│   ├── controller/             # 控制器层
│   ├── service/                # 服务层
│   ├── model/                  # 数据模型层
│   ├── gui/                    # GUI 模块
│   ├── utils/                  # 工具类
│   ├── config/                 # 配置模块
│   └── userscript/             # Tampermonkey 脚本
└── tests/                      # 测试目录
```

### 2.2 模块职责

| 模块 | 职责 | 依赖 |
|------|------|------|
| server | HTTP 服务、路由、中间件 | flask |
| controller | 请求处理、参数验证、响应封装 | service |
| service | 业务逻辑、数据处理 | utils, model |
| model | 数据结构定义、数据验证 | 无 |
| gui | 用户界面、事件处理 | controller |
| utils | 通用工具函数 | 无 |
| config | 配置管理 | utils |

## 3. 编码规范

### 3.1 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块名 | 小写下划线 | `data_service.py` |
| 类名 | 大驼峰 | `DataService` |
| 函数名 | 小写下划线 | `get_data_by_id` |
| 变量名 | 小写下划线 | `data_list` |
| 常量名 | 大写下划线 | `MAX_SIZE` |
| 私有方法 | 单下划线前缀 | `_validate_input` |

### 3.2 文档字符串规范

```python
def get_data_by_id(self, data_id: str) -> dict:
    """
    根据 ID 获取数据详情。
    
    参数：
        data_id: 数据唯一标识符
    
    返回：
        包含数据详情的字典，格式如下：
        {
            'id': str,
            'source': dict,
            'response': dict,
            'metadata': dict,
            'received_at': str
        }
    
    异常：
        ValueError: 当 data_id 为空时抛出
        DataNotFoundError: 当数据不存在时抛出
    
    示例：
        >>> service = DataService()
        >>> data = service.get_data_by_id('data_001')
        >>> print(data['id'])
        'data_001'
    """
    pass
```

### 3.3 类型注解

```python
from typing import Dict, List, Optional, Any, Tuple

def process_data(
    data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> Tuple[bool, str]:
    """
    处理数据。
    
    参数：
        data: 输入数据
        options: 可选的处理选项
    
    返回：
        (是否成功, 消息) 元组
    """
    pass

class DataCache:
    def __init__(self, max_size: int = 1000) -> None:
        self.max_size: int = max_size
        self._cache: Dict[str, Any] = {}
    
    def get(self, key: str) -> Optional[Any]:
        pass
    
    def set(self, key: str, value: Any) -> None:
        pass
```

### 3.4 异常处理

```python
class FrameworkError(Exception):
    """框架基础异常类"""
    pass

class ConfigError(FrameworkError):
    """配置相关异常"""
    pass

class DataError(FrameworkError):
    """数据处理相关异常"""
    pass

class ServiceError(FrameworkError):
    """服务运行相关异常"""
    pass

def load_config(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"配置文件不存在: {path}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"配置文件格式错误: {e}")
```

## 4. 工具类使用指南

### 4.1 ExcelUtil - Excel 处理工具

```python
from src.utils.excel_util import ExcelUtil

class ExcelUtil:
    """
    Excel 文件处理工具类。
    
    功能：
    - 创建 Excel 文件
    - 写入数据
    - 设置样式
    - 保存文件
    """
    
    @staticmethod
    def create_workbook() -> Workbook:
        """
        创建新的工作簿。
        
        返回：
            openpyxl.Workbook 实例
        """
        pass
    
    @staticmethod
    def create_sheet(workbook: Workbook, name: str) -> Worksheet:
        """
        创建工作表。
        
        参数：
            workbook: 工作簿实例
            name: 工作表名称
        
        返回：
            Worksheet 实例
        """
        pass
    
    @staticmethod
    def write_data(sheet: Worksheet, data: List[List], start_row: int = 1, start_col: int = 1):
        """
        写入数据到工作表。
        
        参数：
            sheet: 工作表实例
            data: 二维数据列表
            start_row: 起始行号（从 1 开始）
            start_col: 起始列号（从 1 开始）
        """
        pass
    
    @staticmethod
    def write_headers(sheet: Worksheet, headers: List[str], row: int = 1):
        """
        写入表头。
        
        参数：
            sheet: 工作表实例
            headers: 表头列表
            row: 行号
        """
        pass
    
    @staticmethod
    def set_column_width(sheet: Worksheet, column: str, width: int):
        """
        设置列宽。
        
        参数：
            sheet: 工作表实例
            column: 列标识（如 'A', 'B'）
            width: 宽度值
        """
        pass
    
    @staticmethod
    def auto_fit_columns(sheet: Worksheet):
        """
        自动调整所有列宽。
        
        参数：
            sheet: 工作表实例
        """
        pass
    
    @staticmethod
    def apply_header_style(sheet: Worksheet, row: int = 1):
        """
        应用表头样式。
        
        参数：
            sheet: 工作表实例
            row: 表头行号
        """
        pass
    
    @staticmethod
    def save(workbook: Workbook, path: str):
        """
        保存工作簿。
        
        参数：
            workbook: 工作簿实例
            path: 保存路径
        """
        pass
```

**使用示例：**

```python
from src.utils.excel_util import ExcelUtil

wb = ExcelUtil.create_workbook()
ws = ExcelUtil.create_sheet(wb, "数据")

headers = ["ID", "URL", "状态", "时间"]
ExcelUtil.write_headers(ws, headers)

data = [
    ["001", "https://example.com/api", 200, "2024-01-01 12:00:00"],
    ["002", "https://example.com/api", 200, "2024-01-01 12:01:00"]
]
ExcelUtil.write_data(ws, data, start_row=2)

ExcelUtil.apply_header_style(ws)
ExcelUtil.auto_fit_columns(ws)

ExcelUtil.save(wb, "./exports/data.xlsx")
```

### 4.2 JsonUtil - JSON 处理工具

```python
from src.utils.json_util import JsonUtil

class JsonUtil:
    """
    JSON 文件处理工具类。
    
    功能：
    - 读取 JSON 文件
    - 写入 JSON 文件
    - 格式化 JSON
    - 验证 JSON
    """
    
    @staticmethod
    def read(path: str, encoding: str = 'utf-8') -> dict:
        """
        读取 JSON 文件。
        
        参数：
            path: 文件路径
            encoding: 编码格式
        
        返回：
            解析后的字典
        
        异常：
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON 格式错误
        """
        pass
    
    @staticmethod
    def write(path: str, data: dict, encoding: str = 'utf-8', indent: int = 4):
        """
        写入 JSON 文件。
        
        参数：
            path: 文件路径
            data: 数据字典
            encoding: 编码格式
            indent: 缩进空格数
        """
        pass
    
    @staticmethod
    def dumps(data: dict, indent: int = 4) -> str:
        """
        将字典转换为 JSON 字符串。
        
        参数：
            data: 数据字典
            indent: 缩进空格数
        
        返回：
            JSON 字符串
        """
        pass
    
    @staticmethod
    def loads(json_str: str) -> dict:
        """
        将 JSON 字符串解析为字典。
        
        参数：
            json_str: JSON 字符串
        
        返回：
            数据字典
        """
        pass
    
    @staticmethod
    def is_valid(json_str: str) -> bool:
        """
        验证 JSON 字符串是否有效。
        
        参数：
            json_str: JSON 字符串
        
        返回：
            是否有效
        """
        pass
    
    @staticmethod
    def merge(base: dict, override: dict) -> dict:
        """
        深度合并两个字典。
        
        参数：
            base: 基础字典
            override: 覆盖字典
        
        返回：
            合并后的字典
        """
        pass
```

### 4.3 FileUtil - 文件操作工具

```python
from src.utils.file_util import FileUtil

class FileUtil:
    """
    文件操作工具类。
    
    功能：
    - 文件读写
    - 目录操作
    - 路径处理
    - 文件搜索
    """
    
    @staticmethod
    def ensure_dir(path: str):
        """
        确保目录存在，不存在则创建。
        
        参数：
            path: 目录路径
        """
        pass
    
    @staticmethod
    def exists(path: str) -> bool:
        """
        检查文件或目录是否存在。
        
        参数：
            path: 路径
        
        返回：
            是否存在
        """
        pass
    
    @staticmethod
    def delete(path: str) -> bool:
        """
        删除文件或目录。
        
        参数：
            path: 路径
        
        返回：
            是否删除成功
        """
        pass
    
    @staticmethod
    def get_filename(path: str) -> str:
        """
        获取文件名（含扩展名）。
        
        参数：
            path: 文件路径
        
        返回：
            文件名
        """
        pass
    
    @staticmethod
    def get_extension(path: str) -> str:
        """
        获取文件扩展名。
        
        参数：
            path: 文件路径
        
        返回：
            扩展名（不含点）
        """
        pass
    
    @staticmethod
    def join(*paths) -> str:
        """
        连接路径。
        
        参数：
            *paths: 路径片段
        
        返回：
            连接后的路径
        """
        pass
    
    @staticmethod
    def list_files(dir_path: str, pattern: str = '*') -> List[str]:
        """
        列出目录下的文件。
        
        参数：
            dir_path: 目录路径
            pattern: 文件模式（如 '*.xlsx'）
        
        返回：
            文件路径列表
        """
        pass
    
    @staticmethod
    def get_size(path: str) -> int:
        """
        获取文件大小。
        
        参数：
            path: 文件路径
        
        返回：
            文件大小（字节）
        """
        pass
    
    @staticmethod
    def copy(src: str, dst: str) -> bool:
        """
        复制文件。
        
        参数：
            src: 源文件路径
            dst: 目标文件路径
        
        返回：
            是否复制成功
        """
        pass
```

### 4.4 HttpUtil - HTTP 请求工具

```python
from src.utils.http_util import HttpUtil

class HttpUtil:
    """
    HTTP 请求工具类。
    
    功能：
    - 发送 HTTP 请求
    - 处理响应
    - 超时控制
    - 重试机制
    """
    
    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None, timeout: int = 30) -> dict:
        """
        发送 GET 请求。
        
        参数：
            url: 请求 URL
            params: 查询参数
            headers: 请求头
            timeout: 超时时间（秒）
        
        返回：
            响应数据字典
        """
        pass
    
    @staticmethod
    def post(url: str, data: dict = None, json: dict = None, headers: dict = None, timeout: int = 30) -> dict:
        """
        发送 POST 请求。
        
        参数：
            url: 请求 URL
            data: 表单数据
            json: JSON 数据
            headers: 请求头
            timeout: 超时时间（秒）
        
        返回：
            响应数据字典
        """
        pass
    
    @staticmethod
    def request(method: str, url: str, **kwargs) -> dict:
        """
        发送通用 HTTP 请求。
        
        参数：
            method: 请求方法
            url: 请求 URL
            **kwargs: 其他参数
        
        返回：
            响应数据字典
        """
        pass
```

### 4.5 Logger - 日志工具

```python
from src.utils.logger import Logger

class Logger:
    """
    日志工具类。
    
    功能：
    - 配置日志
    - 输出日志
    - 日志文件管理
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls, name: str = 'app') -> 'Logger':
        """
        获取日志实例。
        
        参数：
            name: 日志名称
        
        返回：
            Logger 实例
        """
        pass
    
    def configure(self, level: str = 'INFO', file: str = None, format: str = None):
        """
        配置日志。
        
        参数：
            level: 日志级别
            file: 日志文件路径
            format: 日志格式
        """
        pass
    
    def debug(self, message: str):
        """输出 DEBUG 级别日志"""
        pass
    
    def info(self, message: str):
        """输出 INFO 级别日志"""
        pass
    
    def warning(self, message: str):
        """输出 WARNING 级别日志"""
        pass
    
    def error(self, message: str, exc_info: bool = False):
        """输出 ERROR 级别日志"""
        pass
    
    def critical(self, message: str):
        """输出 CRITICAL 级别日志"""
        pass
```

**使用示例：**

```python
from src.utils.logger import Logger

logger = Logger.get_instance('my_module')
logger.configure(level='DEBUG', file='./logs/app.log')

logger.info("应用启动")
logger.debug("调试信息")
logger.error("发生错误", exc_info=True)
```

## 5. 扩展开发指南

### 5.1 添加新的 API 接口

**步骤 1：创建路由文件**

在 `src/server/routes/` 目录下创建新文件，如 `custom.py`：

```python
from flask import Blueprint, request, jsonify

custom_bp = Blueprint('custom', __name__, url_prefix='/api/custom')

@custom_bp.route('/action', methods=['POST'])
def custom_action():
    """
    自定义操作接口。
    """
    data = request.get_json()
    
    result = {
        'success': True,
        'data': {},
        'message': '操作成功'
    }
    
    return jsonify(result)
```

**步骤 2：注册蓝图**

在 `src/server/app.py` 中注册新蓝图：

```python
from src.server.routes.custom import custom_bp

def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(custom_bp)  # 添加这行
```

### 5.2 添加新的工具类

**步骤 1：创建工具类文件**

在 `src/utils/` 目录下创建新文件，如 `string_util.py`：

```python
class StringUtil:
    """
    字符串处理工具类。
    """
    
    @staticmethod
    def truncate(text: str, max_length: int = 100, suffix: str = '...') -> str:
        """
        截断字符串。
        
        参数：
            text: 原始字符串
            max_length: 最大长度
            suffix: 截断后缀
        
        返回：
            截断后的字符串
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
```

**步骤 2：导出工具类**

在 `src/utils/__init__.py` 中添加导出：

```python
from .string_util import StringUtil

__all__ = ['ExcelUtil', 'JsonUtil', 'FileUtil', 'HttpUtil', 'Logger', 'StringUtil']
```

### 5.3 添加新的 GUI 组件

**步骤 1：创建组件文件**

在 `src/gui/widgets/` 目录下创建新文件：

```python
import tkinter as tk
from tkinter import ttk

class DataTable:
    """
    数据表格组件。
    """
    
    def __init__(self, parent, columns: list):
        """
        初始化数据表格。
        
        参数：
            parent: 父容器
            columns: 列配置列表
        """
        self.frame = ttk.Frame(parent)
        self.tree = ttk.Treeview(self.frame, columns=[c['id'] for c in columns], show='headings')
        
        for col in columns:
            self.tree.heading(col['id'], text=col['title'])
            self.tree.column(col['id'], width=col.get('width', 100))
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def insert_data(self, data: list):
        """
        插入数据。
        
        参数：
            data: 数据列表
        """
        for item in data:
            self.tree.insert('', 'end', values=item)
    
    def clear(self):
        """清空数据"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
```

### 5.4 添加新的数据模型

**步骤 1：创建模型文件**

在 `src/model/` 目录下创建新文件：

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class InterceptData:
    """
    拦截数据模型。
    """
    
    id: str
    source_url: str
    source_method: str
    response_status: int
    response_body: Any
    metadata: Optional[Dict[str, Any]] = None
    received_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'InterceptData':
        """
        从字典创建实例。
        
        参数：
            data: 数据字典
        
        返回：
            InterceptData 实例
        """
        return cls(
            id=data.get('id'),
            source_url=data.get('source', {}).get('url'),
            source_method=data.get('source', {}).get('method'),
            response_status=data.get('response', {}).get('status'),
            response_body=data.get('response', {}).get('body'),
            metadata=data.get('metadata'),
            received_at=datetime.now()
        )
    
    def to_dict(self) -> dict:
        """
        转换为字典。
        
        返回：
            数据字典
        """
        return {
            'id': self.id,
            'source': {
                'url': self.source_url,
                'method': self.source_method
            },
            'response': {
                'status': self.response_status,
                'body': self.response_body
            },
            'metadata': self.metadata,
            'received_at': self.received_at.isoformat() if self.received_at else None
        }
```

## 6. 测试指南

### 6.1 测试目录结构

```
tests/
├── __init__.py
├── conftest.py              # pytest 配置
├── test_utils/              # 工具类测试
│   ├── __init__.py
│   ├── test_excel_util.py
│   ├── test_json_util.py
│   └── test_file_util.py
├── test_services/           # 服务层测试
│   ├── __init__.py
│   ├── test_config_service.py
│   └── test_data_service.py
└── test_controllers/        # 控制器测试
    ├── __init__.py
    └── test_data_controller.py
```

### 6.2 测试示例

```python
import pytest
from src.utils.excel_util import ExcelUtil
from openpyxl import Workbook

class TestExcelUtil:
    
    def test_create_workbook(self):
        """测试创建工作簿"""
        wb = ExcelUtil.create_workbook()
        assert isinstance(wb, Workbook)
    
    def test_write_headers(self):
        """测试写入表头"""
        wb = ExcelUtil.create_workbook()
        ws = wb.active
        
        headers = ['ID', 'Name', 'Value']
        ExcelUtil.write_headers(ws, headers)
        
        assert ws.cell(1, 1).value == 'ID'
        assert ws.cell(1, 2).value == 'Name'
        assert ws.cell(1, 3).value == 'Value'
    
    def test_write_data(self):
        """测试写入数据"""
        wb = ExcelUtil.create_workbook()
        ws = wb.active
        
        data = [
            [1, 'Item1', 100],
            [2, 'Item2', 200]
        ]
        ExcelUtil.write_data(ws, data, start_row=2)
        
        assert ws.cell(2, 1).value == 1
        assert ws.cell(3, 2).value == 'Item2'
```

### 6.3 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_utils/test_excel_util.py

# 运行指定测试方法
pytest tests/test_utils/test_excel_util.py::TestExcelUtil::test_create_workbook

# 显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 7. 调试技巧

### 7.1 启用调试模式

修改配置文件 `config.json`：

```json
{
    "server": {
        "debug": true
    },
    "logging": {
        "level": "DEBUG"
    }
}
```

### 7.2 使用断点调试

```python
import pdb

def some_function():
    x = 10
    y = 20
    pdb.set_trace()  # 设置断点
    z = x + y
    return z
```

### 7.3 查看日志

```bash
# 实时查看日志
tail -f logs/app.log

# 搜索错误日志
grep "ERROR" logs/app.log
```

## 8. 发布指南

### 8.1 版本号规范

使用语义化版本号：`MAJOR.MINOR.PATCH`

- MAJOR：不兼容的 API 变更
- MINOR：向后兼容的功能新增
- PATCH：向后兼容的问题修复

### 8.2 发布检查清单

- [ ] 更新版本号
- [ ] 更新 CHANGELOG
- [ ] 运行所有测试
- [ ] 检查代码风格
- [ ] 更新文档
- [ ] 创建 Git 标签

### 8.3 打包发布

```bash
# 创建发布包
python setup.py sdist bdist_wheel

# 上传到 PyPI（可选）
twine upload dist/*
```

## 9. 常见问题

### Q1: 端口被占用怎么办？

修改 `config.json` 中的 `server.port` 配置，或通过 GUI 界面修改端口号。

### Q2: 如何修改日志级别？

修改 `config.json` 中的 `logging.level` 配置，可选值：DEBUG、INFO、WARNING、ERROR、CRITICAL。

### Q3: 如何清空缓存数据？

通过 GUI 界面点击"清空缓存"按钮，或调用 API：`DELETE /api/data/cache`。

### Q4: 如何添加新的拦截规则？

在 Tampermonkey 脚本中修改 `GlobalConfig.interceptor.patterns` 数组，添加需要拦截的 URL 模式。
