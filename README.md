# Tampermonkey Framework

## 项目概述

Tampermonkey Framework 是一个基于 Python 的本地应用服务器框架，旨在帮助开发者快速构建 Tampermonkey 脚本与本地应用的交互能力。通过该框架，开发者可以轻松实现：

- 页面元素自动化操作（点击、输入等）
- 拦截并处理网络请求响应数据
- 数据处理与 Excel 导出
- 本地服务器与浏览器脚本的双向通信

## 核心特性

| 特性 | 描述 |
|------|------|
| 开箱即用 | 内置完整的 GUI 界面与配置管理，无需从零搭建 |
| 模块化架构 | 采用分层设计，各模块职责清晰，易于扩展 |
| 快速开发 | 预置常用工具类与接口模板，开发者仅需关注业务逻辑 |
| 配置持久化 | JSON 格式配置文件，支持热更新与版本管理 |
| 跨平台支持 | 基于 Python 与 Tkinter，支持 Windows/macOS/Linux |

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        浏览器环境                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Tampermonkey Script                         │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐   │   │
│  │  │  UI 模块   │  │ 通信模块  │  │ 功能模块(点击/拦截) │   │   │
│  │  └───────────┘  └───────────┘  └───────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP/WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      本地应用服务器                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    GUI Layer (Tkinter)                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Controller Layer                         │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │ServerCtrl    │  │ ConfigCtrl   │  │ DataCtrl     │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Service Layer                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │ServerService │  │ ConfigService│  │ DataService  │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Utils Layer                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │ ExcelUtil    │  │ HttpUtil     │  │ JsonUtil     │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 目录结构

```
tampermonkey-framework/
├── README.md                   # 项目说明文档
├── requirements.txt            # Python 依赖清单
├── main.py                     # 应用程序入口
├── config.json                 # 外置配置文件（运行时生成）
├── docs/                       # 文档目录
│   ├── architecture.md         # 架构设计文档
│   ├── api_design.md           # API 接口设计文档
│   ├── userscript_design.md    # Tampermonkey 脚本设计文档
│   ├── server_design.md        # 本地服务器设计文档
│   ├── configuration.md        # 配置管理文档
│   └── development_guide.md    # 开发指南
├── src/                        # 源代码目录
│   ├── server/                 # 服务器模块
│   │   ├── __init__.py
│   │   ├── app.py              # Flask 应用工厂
│   │   ├── routes/             # 路由模块
│   │   │   ├── __init__.py
│   │   │   ├── health.py       # 健康检查路由
│   │   │   ├── data.py         # 数据处理路由
│   │   │   └── action.py       # 操作执行路由
│   │   └── middleware/         # 中间件模块
│   │       ├── __init__.py
│   │       └── cors.py         # CORS 中间件
│   ├── controller/             # 控制器层
│   │   ├── __init__.py
│   │   ├── server_controller.py    # 服务器控制器
│   │   ├── config_controller.py    # 配置控制器
│   │   └── data_controller.py      # 数据控制器
│   ├── service/                # 服务层
│   │   ├── __init__.py
│   │   ├── server_service.py   # 服务器服务
│   │   ├── config_service.py   # 配置服务
│   │   └── data_service.py     # 数据服务
│   ├── model/                  # 数据模型层
│   │   ├── __init__.py
│   │   ├── config_model.py     # 配置模型
│   │   └── data_model.py       # 数据模型
│   ├── gui/                    # GUI 模块
│   │   ├── __init__.py
│   │   ├── main_window.py      # 主窗口
│   │   ├── widgets/            # 自定义组件
│   │   │   ├── __init__.py
│   │   │   ├── status_bar.py   # 状态栏组件
│   │   │   └── log_panel.py    # 日志面板组件
│   │   └── dialogs/            # 对话框
│   │       ├── __init__.py
│   │       └── settings_dialog.py  # 设置对话框
│   ├── utils/                  # 工具类模块
│   │   ├── __init__.py
│   │   ├── excel_util.py       # Excel 处理工具
│   │   ├── json_util.py        # JSON 处理工具
│   │   ├── http_util.py        # HTTP 请求工具
│   │   ├── file_util.py        # 文件操作工具
│   │   └── logger.py           # 日志工具
│   ├── config/                 # 配置模块
│   │   ├── __init__.py
│   │   ├── default_config.py   # 内置默认配置
│   │   └── config_manager.py   # 配置管理器
│   └── userscript/             # Tampermonkey 脚本
│       └── template.js         # 脚本模板
└── tests/                      # 测试目录
    ├── __init__.py
    ├── test_utils/
    ├── test_services/
    └── test_controllers/
```

## 技术选型

### 后端技术栈

| 组件 | 技术方案 | 版本 | 选型理由 |
|------|----------|------|----------|
| Web 框架 | Flask | 3.0.x | 轻量级、易扩展、适合小型服务 |
| GUI 框架 | Tkinter | 内置 | Python 标准库、跨平台、零依赖 |
| Excel 处理 | openpyxl | 3.1.x | 支持 xlsx 格式、功能完善 |
| 异步任务 | threading | 内置 | 简单可靠、满足需求 |
| 日志系统 | logging | 内置 | 标准库、功能完备 |

### 前端技术栈（Tampermonkey 脚本）

| 组件 | 技术方案 | 选型理由 |
|------|----------|----------|
| UI 框架 | 原生 CSS | 无依赖、兼容性好 |
| HTTP 请求 | fetch API | 现代浏览器原生支持 |
| 数据存储 | GM_setValue/GM_getValue | Tampermonkey 原生 API |

## 快速开始

### 环境要求

- Python 3.8+
- 支持 ES6 的现代浏览器
- Tampermonkey 浏览器扩展

### 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd tampermonkey-framework

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
python main.py
```

### 安装 Tampermonkey 脚本

1. 打开 Tampermonkey 扩展管理页面
2. 创建新脚本
3. 复制 `src/userscript/template.js` 内容
4. 保存并启用脚本

## 文档索引

| 文档 | 说明 |
|------|------|
| [架构设计文档](docs/architecture.md) | 系统架构详细设计说明 |
| [API 接口设计文档](docs/api_design.md) | HTTP 接口规范与示例 |
| [Tampermonkey 脚本设计文档](docs/userscript_design.md) | 脚本功能模块设计 |
| [本地服务器设计文档](docs/server_design.md) | 服务器模块详细设计 |
| [配置管理文档](docs/configuration.md) | 配置系统设计说明 |
| [开发指南](docs/development_guide.md) | 开发规范与最佳实践 |

## 许可证

MIT License
