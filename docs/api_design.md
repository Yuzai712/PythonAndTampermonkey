# API 接口设计文档

## 1. 接口概述

### 1.1 基础信息

| 项目 | 说明 |
|------|------|
| 基础 URL | `http://127.0.0.1:{port}` |
| 默认端口 | 8080 |
| 协议 | HTTP |
| 数据格式 | JSON |
| 编码 | UTF-8 |

### 1.2 通用响应格式

#### 成功响应

```json
{
    "success": true,
    "data": {},
    "message": "操作成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

#### 错误响应

```json
{
    "success": false,
    "error": {
        "code": 1001,
        "message": "错误描述",
        "details": "详细错误信息"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 1.3 错误码定义

| 错误码范围 | 类型 | 说明 |
|------------|------|------|
| 1000-1999 | 配置错误 | 配置相关错误 |
| 2000-2999 | 服务错误 | 服务运行相关错误 |
| 3000-3999 | 数据错误 | 数据处理相关错误 |
| 4000-4999 | 网络错误 | 网络请求相关错误 |

| 错误码 | 说明 |
|--------|------|
| 1001 | 配置文件不存在 |
| 1002 | 配置格式错误 |
| 1003 | 配置项缺失 |
| 2001 | 服务未启动 |
| 2002 | 服务已运行 |
| 2003 | 端口被占用 |
| 3001 | 数据格式错误 |
| 3002 | 数据验证失败 |
| 3003 | 数据处理失败 |
| 4001 | 请求超时 |
| 4002 | 连接失败 |

## 2. 健康检查接口

### 2.1 检查服务状态

检查服务器是否在线运行。

**请求**

```
GET /api/health
```

**请求参数**

无

**响应示例**

```json
{
    "success": true,
    "data": {
        "status": "running",
        "version": "1.0.0",
        "uptime": 3600,
        "port": 8080
    },
    "message": "服务正常运行",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

**响应字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | 服务状态：running/stopped |
| version | string | 服务版本号 |
| uptime | integer | 运行时长（秒） |
| port | integer | 当前监听端口 |

### 2.2 心跳检测

用于 Tampermonkey 脚本定期检测服务器连接状态。

**请求**

```
GET /api/health/ping
```

**响应示例**

```json
{
    "success": true,
    "data": {
        "pong": true,
        "server_time": "2024-01-01T12:00:00Z"
    },
    "message": "pong",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 3. 数据处理接口

### 3.1 接收拦截数据

接收 Tampermonkey 脚本拦截的接口响应数据。

**请求**

```
POST /api/data/intercept
```

**请求头**

| 头部 | 值 |
|------|------|
| Content-Type | application/json |

**请求体**

```json
{
    "source": {
        "url": "https://example.com/api/data",
        "method": "GET",
        "timestamp": "2024-01-01T12:00:00Z"
    },
    "response": {
        "status": 200,
        "headers": {
            "content-type": "application/json"
        },
        "body": {
            "data": []
        }
    },
    "metadata": {
        "page_url": "https://example.com/page",
        "user_agent": "Mozilla/5.0..."
    }
}
```

**请求字段说明**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | object | 是 | 数据来源信息 |
| source.url | string | 是 | 原始请求 URL |
| source.method | string | 是 | 请求方法 |
| source.timestamp | string | 是 | 请求时间戳 |
| response | object | 是 | 响应数据 |
| response.status | integer | 是 | HTTP 状态码 |
| response.headers | object | 否 | 响应头 |
| response.body | any | 是 | 响应体 |
| metadata | object | 否 | 元数据 |

**响应示例**

```json
{
    "success": true,
    "data": {
        "id": "data_20240101120000_001",
        "received_at": "2024-01-01T12:00:00Z",
        "processed": false
    },
    "message": "数据接收成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 3.2 批量接收数据

批量接收多条拦截数据。

**请求**

```
POST /api/data/intercept/batch
```

**请求体**

```json
{
    "items": [
        {
            "source": {...},
            "response": {...},
            "metadata": {...}
        },
        {
            "source": {...},
            "response": {...},
            "metadata": {...}
        }
    ]
}
```

**响应示例**

```json
{
    "success": true,
    "data": {
        "total": 2,
        "received": 2,
        "ids": ["data_001", "data_002"]
    },
    "message": "批量数据接收成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 3.3 查询缓存数据

查询已缓存的数据列表。

**请求**

```
GET /api/data/cache
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | integer | 否 | 页码，默认 1 |
| size | integer | 否 | 每页数量，默认 20 |
| source_url | string | 否 | 按来源 URL 过滤 |

**响应示例**

```json
{
    "success": true,
    "data": {
        "items": [
            {
                "id": "data_001",
                "source_url": "https://example.com/api/data",
                "received_at": "2024-01-01T12:00:00Z",
                "processed": false
            }
        ],
        "pagination": {
            "page": 1,
            "size": 20,
            "total": 100,
            "total_pages": 5
        }
    },
    "message": "查询成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 3.4 获取数据详情

获取指定数据的详细信息。

**请求**

```
GET /api/data/cache/{data_id}
```

**路径参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| data_id | string | 数据 ID |

**响应示例**

```json
{
    "success": true,
    "data": {
        "id": "data_001",
        "source": {
            "url": "https://example.com/api/data",
            "method": "GET",
            "timestamp": "2024-01-01T12:00:00Z"
        },
        "response": {
            "status": 200,
            "headers": {},
            "body": {}
        },
        "metadata": {},
        "received_at": "2024-01-01T12:00:00Z",
        "processed": false
    },
    "message": "查询成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 3.5 清空缓存数据

清空所有缓存的数据。

**请求**

```
DELETE /api/data/cache
```

**响应示例**

```json
{
    "success": true,
    "data": {
        "cleared_count": 100
    },
    "message": "缓存已清空",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 4. 导出接口

### 4.1 导出为 Excel

将缓存数据导出为 Excel 文件。

**请求**

```
POST /api/export/excel
```

**请求体**

```json
{
    "format": {
        "filename": "export_data",
        "sheet_name": "数据",
        "columns": [
            {
                "field": "source.url",
                "title": "来源URL",
                "width": 30
            },
            {
                "field": "response.body.data",
                "title": "数据内容",
                "width": 50
            },
            {
                "field": "received_at",
                "title": "接收时间",
                "width": 20
            }
        ]
    },
    "filter": {
        "source_url": "https://example.com/api/data",
        "start_time": "2024-01-01T00:00:00Z",
        "end_time": "2024-01-31T23:59:59Z"
    },
    "options": {
        "include_headers": true,
        "auto_width": true,
        "style": "default"
    }
}
```

**请求字段说明**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| format | object | 否 | 格式配置 |
| format.filename | string | 否 | 文件名（不含扩展名） |
| format.sheet_name | string | 否 | 工作表名称 |
| format.columns | array | 否 | 列配置 |
| filter | object | 否 | 过滤条件 |
| options | object | 否 | 导出选项 |

**响应示例**

```json
{
    "success": true,
    "data": {
        "file_path": "/path/to/export/export_data_20240101.xlsx",
        "file_size": 10240,
        "row_count": 100,
        "download_url": "/api/export/download/export_data_20240101.xlsx"
    },
    "message": "导出成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 4.2 下载导出文件

下载已生成的导出文件。

**请求**

```
GET /api/export/download/{filename}
```

**路径参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| filename | string | 文件名 |

**响应**

文件流（Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet）

### 4.3 获取导出历史

获取历史导出记录。

**请求**

```
GET /api/export/history
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | integer | 否 | 页码 |
| size | integer | 否 | 每页数量 |

**响应示例**

```json
{
    "success": true,
    "data": {
        "items": [
            {
                "id": "export_001",
                "filename": "export_data_20240101.xlsx",
                "file_size": 10240,
                "row_count": 100,
                "created_at": "2024-01-01T12:00:00Z"
            }
        ],
        "pagination": {
            "page": 1,
            "size": 20,
            "total": 10
        }
    },
    "message": "查询成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 5. 配置接口

### 5.1 获取配置

获取当前服务器配置。

**请求**

```
GET /api/config
```

**响应示例**

```json
{
    "success": true,
    "data": {
        "server": {
            "port": 8080,
            "host": "127.0.0.1"
        },
        "cache": {
            "max_size": 1000,
            "expire_time": 3600
        },
        "export": {
            "output_dir": "./exports",
            "default_format": "xlsx"
        },
        "logging": {
            "level": "INFO",
            "file": "./logs/app.log"
        }
    },
    "message": "获取成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 5.2 更新配置

更新服务器配置。

**请求**

```
PUT /api/config
```

**请求体**

```json
{
    "server": {
        "port": 8081
    },
    "cache": {
        "max_size": 2000
    }
}
```

**响应示例**

```json
{
    "success": true,
    "data": {
        "updated_fields": ["server.port", "cache.max_size"],
        "requires_restart": true
    },
    "message": "配置更新成功，部分配置需要重启服务生效",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 5.3 重置配置

重置为默认配置。

**请求**

```
POST /api/config/reset
```

**响应示例**

```json
{
    "success": true,
    "data": {
        "reset": true
    },
    "message": "配置已重置为默认值",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 6. 操作接口

### 6.1 执行页面操作

通知 Tampermonkey 脚本执行页面操作（反向通信，通过轮询机制实现）。

**请求**

```
POST /api/action/execute
```

**请求体**

```json
{
    "action": "click",
    "selector": "#button-id",
    "options": {
        "wait_time": 1000,
        "retry_count": 3
    }
}
```

**请求字段说明**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | 是 | 操作类型：click/input/scroll |
| selector | string | 是 | CSS 选择器 |
| options | object | 否 | 操作选项 |
| options.wait_time | integer | 否 | 等待时间（毫秒） |
| options.retry_count | integer | 否 | 重试次数 |

**响应示例**

```json
{
    "success": true,
    "data": {
        "action_id": "action_001",
        "status": "pending"
    },
    "message": "操作已提交",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 6.2 查询操作状态

查询操作的执行状态。

**请求**

```
GET /api/action/status/{action_id}
```

**响应示例**

```json
{
    "success": true,
    "data": {
        "action_id": "action_001",
        "status": "completed",
        "result": {
            "success": true,
            "message": "点击成功"
        },
        "executed_at": "2024-01-01T12:00:00Z"
    },
    "message": "查询成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 6.3 获取待执行操作

Tampermonkey 脚本轮询获取待执行的操作。

**请求**

```
GET /api/action/pending
```

**响应示例**

```json
{
    "success": true,
    "data": {
        "actions": [
            {
                "action_id": "action_001",
                "action": "click",
                "selector": "#button-id",
                "options": {}
            }
        ],
        "count": 1
    },
    "message": "查询成功",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 6.4 上报操作结果

Tampermonkey 脚本上报操作执行结果。

**请求**

```
POST /api/action/result
```

**请求体**

```json
{
    "action_id": "action_001",
    "success": true,
    "message": "点击成功",
    "details": {
        "element_found": true,
        "click_executed": true
    }
}
```

**响应示例**

```json
{
    "success": true,
    "data": {},
    "message": "结果已记录",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 7. 接口调用示例

### 7.1 JavaScript (fetch)

```javascript
async function sendDataToServer(data) {
    const response = await fetch('http://127.0.0.1:8080/api/data/intercept', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            source: {
                url: data.url,
                method: data.method,
                timestamp: new Date().toISOString()
            },
            response: {
                status: data.status,
                body: data.body
            }
        })
    });
    return response.json();
}
```

### 7.2 Python (requests)

```python
import requests

def send_data_to_server(data):
    response = requests.post(
        'http://127.0.0.1:8080/api/data/intercept',
        json={
            'source': {
                'url': data['url'],
                'method': data['method'],
                'timestamp': datetime.now().isoformat()
            },
            'response': {
                'status': data['status'],
                'body': data['body']
            }
        }
    )
    return response.json()
```

## 8. 接口版本管理

当前版本：v1

所有接口路径均以 `/api` 开头，后续版本可通过 `/api/v2` 等方式扩展。
