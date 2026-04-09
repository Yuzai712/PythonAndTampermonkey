# Tampermonkey 脚本设计文档

## 1. 脚本概述

### 1.1 脚本元信息

```javascript
// ==UserScript==
// @name         Tampermonkey Framework Client
// @namespace    http://tampermonkey.net/
// @version      1.0.0
// @description  Tampermonkey Framework 客户端脚本，提供页面操作与数据拦截功能
// @author       Your Name
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_deleteValue
// @grant        GM_registerMenuCommand
// @grant        GM_unregisterMenuCommand
// @grant        GM_notification
// @connect      127.0.0.1
// @run-at       document-end
// ==/UserScript==
```

### 1.2 核心功能

| 功能模块 | 说明 |
|----------|------|
| UI 模块 | 悬浮窗界面、状态显示、操作按钮 |
| 通信模块 | HTTP 请求封装、服务器连接管理 |
| 拦截模块 | 拦截指定接口响应数据 |
| 操作模块 | 页面元素点击、输入等操作 |
| 配置模块 | 全局变量管理、配置持久化 |

## 2. 模块设计

### 2.1 模块结构

```
Tampermonkey Script
├── Config (配置模块)
│   ├── 全局配置变量
│   ├── 服务器地址配置
│   └── 拦截规则配置
├── UI (界面模块)
│   ├── 悬浮窗容器
│   ├── 状态显示区
│   ├── 操作按钮区
│   └── 日志显示区
├── Communication (通信模块)
│   ├── HTTP 请求封装
│   ├── 服务器连接检测
│   └── 数据发送/接收
├── Interceptor (拦截模块)
│   ├── XHR 拦截器
│   ├── Fetch 拦截器
│   └── 数据过滤器
└── Action (操作模块)
    ├── 元素选择器
    ├── 点击执行器
    └── 操作队列
```

### 2.2 模块依赖关系

```
Config
    │
    ├──▶ UI (读取配置显示)
    │
    ├──▶ Communication (使用服务器地址)
    │        │
    │        ├──▶ Interceptor (发送拦截数据)
    │        │
    │        └──▶ Action (接收操作指令)
    │
    └──▶ Interceptor (使用拦截规则)
```

## 3. 配置模块设计

### 3.1 全局配置变量

```javascript
const GlobalConfig = {
    server: {
        host: '127.0.0.1',
        port: 8080,
        timeout: 5000,
        reconnectInterval: 3000
    },
    ui: {
        position: { x: 20, y: 20 },
        size: { width: 320, height: 400 },
        opacity: 0.95,
        theme: 'dark'
    },
    interceptor: {
        enabled: true,
        patterns: [
            '/api/data',
            '/api/list'
        ],
        methods: ['GET', 'POST']
    },
    action: {
        autoCheckInterval: 5000,
        retryCount: 3,
        retryDelay: 1000
    },
    debug: false
};
```

### 3.2 配置管理方法

| 方法 | 功能 | 参数 | 返回值 |
|------|------|------|--------|
| `loadConfig()` | 从存储加载配置 | 无 | Object |
| `saveConfig(config)` | 保存配置到存储 | config: Object | void |
| `resetConfig()` | 重置为默认配置 | 无 | void |
| `updateConfig(key, value)` | 更新单个配置项 | key: string, value: any | void |

```javascript
const ConfigManager = {
    STORAGE_KEY: 'tm_framework_config',
    
    loadConfig() {
        try {
            const saved = GM_getValue(this.STORAGE_KEY);
            if (saved) {
                return { ...GlobalConfig, ...JSON.parse(saved) };
            }
        } catch (e) {
            console.error('加载配置失败:', e);
        }
        return { ...GlobalConfig };
    },
    
    saveConfig(config) {
        try {
            GM_setValue(this.STORAGE_KEY, JSON.stringify(config));
        } catch (e) {
            console.error('保存配置失败:', e);
        }
    },
    
    resetConfig() {
        GM_deleteValue(this.STORAGE_KEY);
    },
    
    updateConfig(key, value) {
        const config = this.loadConfig();
        const keys = key.split('.');
        let obj = config;
        for (let i = 0; i < keys.length - 1; i++) {
            obj = obj[keys[i]];
        }
        obj[keys[keys.length - 1]] = value;
        this.saveConfig(config);
    }
};
```

## 4. UI 模块设计

### 4.1 悬浮窗结构

```
┌─────────────────────────────────────┐
│  ┌───────────────────────────────┐  │
│  │  [状态指示灯] 服务器: 已连接   │  │ ← 标题栏（可拖拽）
│  │                    [最小化]   │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │         状态显示区             │  │
│  │  拦截数据: 12 条               │  │
│  │  最后更新: 12:00:00           │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │         操作按钮区             │  │
│  │  [连接服务器] [点击元素]       │  │
│  │  [开始拦截] [导出数据]         │  │
│  │  [清空缓存] [设置]             │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │         日志显示区             │  │
│  │  [12:00:00] 服务器连接成功     │  │
│  │  [12:00:05] 拦截到数据...      │  │
│  │  [12:00:10] 数据已发送         │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### 4.2 样式定义

```javascript
const UIStyles = `
    .tm-framework-panel {
        position: fixed;
        z-index: 999999;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #0f3460;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 12px;
        color: #e8e8e8;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .tm-framework-panel.minimized {
        height: 40px !important;
    }
    
    .tm-framework-panel .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 15px;
        background: rgba(15, 52, 96, 0.5);
        cursor: move;
        user-select: none;
    }
    
    .tm-framework-panel .header .status-indicator {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        transition: background-color 0.3s ease;
    }
    
    .tm-framework-panel .header .status-indicator.connected {
        background-color: #00ff88;
        box-shadow: 0 0 10px #00ff88;
    }
    
    .tm-framework-panel .header .status-indicator.disconnected {
        background-color: #ff4757;
        box-shadow: 0 0 10px #ff4757;
    }
    
    .tm-framework-panel .header .minimize-btn {
        background: transparent;
        border: none;
        color: #e8e8e8;
        cursor: pointer;
        font-size: 16px;
        padding: 0 5px;
    }
    
    .tm-framework-panel .status-area {
        padding: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .tm-framework-panel .status-area .stat-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    
    .tm-framework-panel .status-area .stat-label {
        color: #a0a0a0;
    }
    
    .tm-framework-panel .status-area .stat-value {
        color: #00ff88;
        font-weight: bold;
    }
    
    .tm-framework-panel .button-area {
        padding: 15px;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .tm-framework-panel .btn {
        padding: 10px 15px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 12px;
        font-weight: 500;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .tm-framework-panel .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .tm-framework-panel .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .tm-framework-panel .btn-secondary {
        background: rgba(255, 255, 255, 0.1);
        color: #e8e8e8;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .tm-framework-panel .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .tm-framework-panel .btn-danger {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
    }
    
    .tm-framework-panel .log-area {
        padding: 10px 15px;
        max-height: 150px;
        overflow-y: auto;
    }
    
    .tm-framework-panel .log-area::-webkit-scrollbar {
        width: 6px;
    }
    
    .tm-framework-panel .log-area::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 3px;
    }
    
    .tm-framework-panel .log-item {
        padding: 5px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 11px;
    }
    
    .tm-framework-panel .log-item .time {
        color: #666;
        margin-right: 10px;
    }
    
    .tm-framework-panel .log-item.success {
        color: #00ff88;
    }
    
    .tm-framework-panel .log-item.error {
        color: #ff4757;
    }
    
    .tm-framework-panel .log-item.info {
        color: #70a1ff;
    }
`;
```

### 4.3 UI 管理类

```javascript
class UIManager {
    constructor(config) {
        this.config = config;
        this.panel = null;
        this.isMinimized = false;
        this.isDragging = false;
        this.dragOffset = { x: 0, y: 0 };
    }
    
    init() {
        this.injectStyles();
        this.createPanel();
        this.bindEvents();
        this.loadPosition();
    }
    
    injectStyles() {
        const style = document.createElement('style');
        style.textContent = UIStyles;
        document.head.appendChild(style);
    }
    
    createPanel() {
        this.panel = document.createElement('div');
        this.panel.className = 'tm-framework-panel';
        this.panel.innerHTML = this.getPanelHTML();
        document.body.appendChild(this.panel);
    }
    
    getPanelHTML() {
        return `
            <div class="header">
                <div style="display: flex; align-items: center;">
                    <span class="status-indicator disconnected" id="tm-status-indicator"></span>
                    <span>服务器: <span id="tm-server-status">未连接</span></span>
                </div>
                <button class="minimize-btn" id="tm-minimize-btn">−</button>
            </div>
            <div class="status-area" id="tm-status-area">
                <div class="stat-item">
                    <span class="stat-label">拦截数据</span>
                    <span class="stat-value" id="tm-intercept-count">0 条</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">最后更新</span>
                    <span class="stat-value" id="tm-last-update">--:--:--</span>
                </div>
            </div>
            <div class="button-area" id="tm-button-area">
                <button class="btn btn-primary" id="tm-connect-btn">连接服务器</button>
                <button class="btn btn-secondary" id="tm-click-btn">点击元素</button>
                <button class="btn btn-secondary" id="tm-intercept-btn">开始拦截</button>
                <button class="btn btn-secondary" id="tm-export-btn">导出数据</button>
                <button class="btn btn-danger" id="tm-clear-btn">清空缓存</button>
                <button class="btn btn-secondary" id="tm-settings-btn">设置</button>
            </div>
            <div class="log-area" id="tm-log-area"></div>
        `;
    }
    
    bindEvents() {
        const header = this.panel.querySelector('.header');
        header.addEventListener('mousedown', (e) => this.startDrag(e));
        document.addEventListener('mousemove', (e) => this.drag(e));
        document.addEventListener('mouseup', () => this.endDrag());
        
        document.getElementById('tm-minimize-btn').addEventListener('click', () => this.toggleMinimize());
        document.getElementById('tm-connect-btn').addEventListener('click', () => this.onConnectClick());
        document.getElementById('tm-click-btn').addEventListener('click', () => this.onElementClick());
        document.getElementById('tm-intercept-btn').addEventListener('click', () => this.onInterceptToggle());
        document.getElementById('tm-export-btn').addEventListener('click', () => this.onExportClick());
        document.getElementById('tm-clear-btn').addEventListener('click', () => this.onClearClick());
        document.getElementById('tm-settings-btn').addEventListener('click', () => this.onSettingsClick());
    }
    
    startDrag(e) {
        if (e.target.id === 'tm-minimize-btn') return;
        this.isDragging = true;
        const rect = this.panel.getBoundingClientRect();
        this.dragOffset = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }
    
    drag(e) {
        if (!this.isDragging) return;
        const x = e.clientX - this.dragOffset.x;
        const y = e.clientY - this.dragOffset.y;
        this.panel.style.left = `${Math.max(0, x)}px`;
        this.panel.style.top = `${Math.max(0, y)}px`;
    }
    
    endDrag() {
        if (this.isDragging) {
            this.savePosition();
        }
        this.isDragging = false;
    }
    
    toggleMinimize() {
        this.isMinimized = !this.isMinimized;
        this.panel.classList.toggle('minimized', this.isMinimized);
        document.getElementById('tm-minimize-btn').textContent = this.isMinimized ? '+' : '−';
    }
    
    updateServerStatus(connected) {
        const indicator = document.getElementById('tm-status-indicator');
        const status = document.getElementById('tm-server-status');
        indicator.className = `status-indicator ${connected ? 'connected' : 'disconnected'}`;
        status.textContent = connected ? '已连接' : '未连接';
    }
    
    updateInterceptCount(count) {
        document.getElementById('tm-intercept-count').textContent = `${count} 条`;
    }
    
    updateLastUpdate() {
        const now = new Date();
        const time = now.toTimeString().split(' ')[0];
        document.getElementById('tm-last-update').textContent = time;
    }
    
    addLog(message, type = 'info') {
        const logArea = document.getElementById('tm-log-area');
        const now = new Date();
        const time = now.toTimeString().split(' ')[0];
        
        const logItem = document.createElement('div');
        logItem.className = `log-item ${type}`;
        logItem.innerHTML = `<span class="time">[${time}]</span>${message}`;
        
        logArea.appendChild(logItem);
        logArea.scrollTop = logArea.scrollHeight;
        
        if (logArea.children.length > 100) {
            logArea.removeChild(logArea.firstChild);
        }
    }
    
    savePosition() {
        const rect = this.panel.getBoundingClientRect();
        GM_setValue('tm_panel_position', JSON.stringify({
            x: rect.left,
            y: rect.top
        }));
    }
    
    loadPosition() {
        const saved = GM_getValue('tm_panel_position');
        if (saved) {
            const pos = JSON.parse(saved);
            this.panel.style.left = `${pos.x}px`;
            this.panel.style.top = `${pos.y}px`;
        } else {
            this.panel.style.left = `${this.config.ui.position.x}px`;
            this.panel.style.top = `${this.config.ui.position.y}px`;
        }
    }
    
    onConnectClick() {
        if (this.onConnect) this.onConnect();
    }
    
    onElementClick() {
        if (this.onElementClickCallback) this.onElementClickCallback();
    }
    
    onInterceptToggle() {
        if (this.onInterceptToggleCallback) this.onInterceptToggleCallback();
    }
    
    onExportClick() {
        if (this.onExport) this.onExport();
    }
    
    onClearClick() {
        if (this.onClear) this.onClear();
    }
    
    onSettingsClick() {
        if (this.onSettings) this.onSettings();
    }
}
```

## 5. 通信模块设计

### 5.1 HTTP 请求封装

```javascript
class HttpClient {
    constructor(config) {
        this.config = config;
        this.baseUrl = `http://${config.server.host}:${config.server.port}`;
    }
    
    async request(method, path, data = null) {
        return new Promise((resolve, reject) => {
            const options = {
                method: method,
                url: `${this.baseUrl}${path}`,
                headers: {
                    'Content-Type': 'application/json'
                },
                timeout: this.config.server.timeout,
                onload: (response) => {
                    try {
                        const result = JSON.parse(response.responseText);
                        resolve(result);
                    } catch (e) {
                        reject(new Error('响应解析失败'));
                    }
                },
                onerror: (error) => {
                    reject(new Error('网络请求失败'));
                },
                ontimeout: () => {
                    reject(new Error('请求超时'));
                }
            };
            
            if (data) {
                options.data = JSON.stringify(data);
            }
            
            GM_xmlhttpRequest(options);
        });
    }
    
    async get(path) {
        return this.request('GET', path);
    }
    
    async post(path, data) {
        return this.request('POST', path, data);
    }
    
    async put(path, data) {
        return this.request('PUT', path, data);
    }
    
    async delete(path) {
        return this.request('DELETE', path);
    }
    
    updateBaseUrl(host, port) {
        this.baseUrl = `http://${host}:${port}`;
    }
}
```

### 5.2 服务器连接管理

```javascript
class ServerConnection {
    constructor(httpClient, uiManager, config) {
        this.httpClient = httpClient;
        this.uiManager = uiManager;
        this.config = config;
        this.isConnected = false;
        this.checkInterval = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }
    
    async checkConnection() {
        try {
            const response = await this.httpClient.get('/api/health/ping');
            if (response.success) {
                this.setConnected(true);
                this.reconnectAttempts = 0;
                return true;
            }
        } catch (e) {
            this.setConnected(false);
        }
        return false;
    }
    
    async connect() {
        this.uiManager.addLog('正在连接服务器...', 'info');
        const connected = await this.checkConnection();
        if (connected) {
            this.uiManager.addLog('服务器连接成功', 'success');
            this.startAutoCheck();
        } else {
            this.uiManager.addLog('服务器连接失败', 'error');
        }
        return connected;
    }
    
    startAutoCheck() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }
        this.checkInterval = setInterval(() => {
            this.checkConnection();
        }, this.config.action.autoCheckInterval);
    }
    
    stopAutoCheck() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
    }
    
    setConnected(connected) {
        if (this.isConnected !== connected) {
            this.isConnected = connected;
            this.uiManager.updateServerStatus(connected);
            if (!connected) {
                this.uiManager.addLog('服务器连接断开', 'error');
            }
        }
    }
    
    async autoConnect() {
        setTimeout(async () => {
            this.uiManager.addLog('自动检测服务器状态...', 'info');
            await this.checkConnection();
        }, 3000);
    }
}
```

## 6. 拦截模块设计

### 6.1 XHR 拦截器

```javascript
class XHRInterceptor {
    constructor(config, onIntercept) {
        this.config = config;
        this.onIntercept = onIntercept;
        this.originalXHR = window.XMLHttpRequest;
        this.enabled = false;
    }
    
    enable() {
        if (this.enabled) return;
        
        const self = this;
        window.XMLHttpRequest = function() {
            const xhr = new self.originalXHR();
            const originalOpen = xhr.open;
            const originalSend = xhr.send;
            
            let requestInfo = {};
            
            xhr.open = function(method, url, ...args) {
                requestInfo = { method, url };
                return originalOpen.apply(this, [method, url, ...args]);
            };
            
            xhr.send = function(body) {
                if (self.enabled && self.shouldIntercept(requestInfo.url, requestInfo.method)) {
                    xhr.addEventListener('load', function() {
                        const responseInfo = {
                            source: {
                                url: requestInfo.url,
                                method: requestInfo.method,
                                timestamp: new Date().toISOString()
                            },
                            response: {
                                status: xhr.status,
                                headers: self.parseHeaders(xhr.getAllResponseHeaders()),
                                body: self.parseResponseBody(xhr.responseText)
                            },
                            metadata: {
                                page_url: window.location.href
                            }
                        };
                        self.onIntercept(responseInfo);
                    });
                }
                return originalSend.apply(this, [body]);
            };
            
            return xhr;
        };
        
        this.enabled = true;
    }
    
    disable() {
        if (!this.enabled) return;
        window.XMLHttpRequest = this.originalXHR;
        this.enabled = false;
    }
    
    shouldIntercept(url, method) {
        if (!this.config.interceptor.enabled) return false;
        if (!this.config.interceptor.methods.includes(method)) return false;
        
        const urlPath = new URL(url, window.location.origin).pathname;
        return this.config.interceptor.patterns.some(pattern => {
            if (pattern instanceof RegExp) {
                return pattern.test(urlPath);
            }
            return urlPath.includes(pattern);
        });
    }
    
    parseHeaders(headersString) {
        const headers = {};
        if (headersString) {
            headersString.split('\r\n').forEach(line => {
                const [key, value] = line.split(': ');
                if (key && value) {
                    headers[key] = value;
                }
            });
        }
        return headers;
    }
    
    parseResponseBody(responseText) {
        try {
            return JSON.parse(responseText);
        } catch (e) {
            return responseText;
        }
    }
}
```

### 6.2 Fetch 拦截器

```javascript
class FetchInterceptor {
    constructor(config, onIntercept) {
        this.config = config;
        this.onIntercept = onIntercept;
        this.originalFetch = window.fetch;
        this.enabled = false;
    }
    
    enable() {
        if (this.enabled) return;
        
        const self = this;
        window.fetch = async function(input, init = {}) {
            const url = typeof input === 'string' ? input : input.url;
            const method = init.method || 'GET';
            
            const response = await self.originalFetch.apply(this, [input, init]);
            
            if (self.enabled && self.shouldIntercept(url, method)) {
                const clonedResponse = response.clone();
                clonedResponse.json().then(body => {
                    const responseInfo = {
                        source: {
                            url: url,
                            method: method,
                            timestamp: new Date().toISOString()
                        },
                        response: {
                            status: response.status,
                            headers: self.headersToObject(response.headers),
                            body: body
                        },
                        metadata: {
                            page_url: window.location.href
                        }
                    };
                    self.onIntercept(responseInfo);
                }).catch(() => {});
            }
            
            return response;
        };
        
        this.enabled = true;
    }
    
    disable() {
        if (!this.enabled) return;
        window.fetch = this.originalFetch;
        this.enabled = false;
    }
    
    shouldIntercept(url, method) {
        if (!this.config.interceptor.enabled) return false;
        if (!this.config.interceptor.methods.includes(method)) return false;
        
        try {
            const urlPath = new URL(url, window.location.origin).pathname;
            return this.config.interceptor.patterns.some(pattern => {
                if (pattern instanceof RegExp) {
                    return pattern.test(urlPath);
                }
                return urlPath.includes(pattern);
            });
        } catch (e) {
            return false;
        }
    }
    
    headersToObject(headers) {
        const obj = {};
        headers.forEach((value, key) => {
            obj[key] = value;
        });
        return obj;
    }
}
```

## 7. 操作模块设计

### 7.1 元素点击器

```javascript
class ElementClicker {
    constructor(uiManager) {
        this.uiManager = uiManager;
        this.isSelecting = false;
        this.highlightOverlay = null;
        this.currentTarget = null;
    }
    
    startSelection() {
        this.isSelecting = true;
        this.createOverlay();
        document.addEventListener('mouseover', this.onMouseOver.bind(this));
        document.addEventListener('mouseout', this.onMouseOut.bind(this));
        document.addEventListener('click', this.onElementSelect.bind(this), true);
        document.addEventListener('keydown', this.onKeyDown.bind(this));
        this.uiManager.addLog('请点击要操作的元素', 'info');
    }
    
    stopSelection() {
        this.isSelecting = false;
        this.removeOverlay();
        document.removeEventListener('mouseover', this.onMouseOver);
        document.removeEventListener('mouseout', this.onMouseOut);
        document.removeEventListener('click', this.onElementSelect, true);
        document.removeEventListener('keydown', this.onKeyDown);
        this.currentTarget = null;
    }
    
    createOverlay() {
        this.highlightOverlay = document.createElement('div');
        this.highlightOverlay.style.cssText = `
            position: fixed;
            z-index: 999998;
            pointer-events: none;
            border: 2px solid #00ff88;
            background: rgba(0, 255, 136, 0.1);
            transition: all 0.1s ease;
        `;
        document.body.appendChild(this.highlightOverlay);
    }
    
    removeOverlay() {
        if (this.highlightOverlay) {
            this.highlightOverlay.remove();
            this.highlightOverlay = null;
        }
    }
    
    updateOverlay(element) {
        if (!this.highlightOverlay || !element) return;
        
        const rect = element.getBoundingClientRect();
        this.highlightOverlay.style.left = `${rect.left}px`;
        this.highlightOverlay.style.top = `${rect.top}px`;
        this.highlightOverlay.style.width = `${rect.width}px`;
        this.highlightOverlay.style.height = `${rect.height}px`;
    }
    
    onMouseOver(e) {
        if (!this.isSelecting) return;
        this.currentTarget = e.target;
        this.updateOverlay(e.target);
    }
    
    onMouseOut(e) {
        if (!this.isSelecting) return;
        this.updateOverlay(null);
    }
    
    onElementSelect(e) {
        if (!this.isSelecting) return;
        e.preventDefault();
        e.stopPropagation();
        
        const element = e.target;
        const selector = this.generateSelector(element);
        
        this.stopSelection();
        this.clickElement(selector);
    }
    
    onKeyDown(e) {
        if (e.key === 'Escape') {
            this.stopSelection();
            this.uiManager.addLog('已取消元素选择', 'info');
        }
    }
    
    generateSelector(element) {
        if (element.id) {
            return `#${element.id}`;
        }
        
        const path = [];
        let current = element;
        
        while (current && current !== document.body) {
            let selector = current.tagName.toLowerCase();
            if (current.className) {
                selector += `.${current.className.trim().split(/\s+/).join('.')}`;
            }
            path.unshift(selector);
            current = current.parentElement;
        }
        
        return path.join(' > ');
    }
    
    clickElement(selector) {
        try {
            const element = document.querySelector(selector);
            if (element) {
                element.click();
                this.uiManager.addLog(`已点击元素: ${selector}`, 'success');
                return true;
            } else {
                this.uiManager.addLog(`未找到元素: ${selector}`, 'error');
                return false;
            }
        } catch (e) {
            this.uiManager.addLog(`点击失败: ${e.message}`, 'error');
            return false;
        }
    }
}
```

### 7.2 操作队列管理

```javascript
class ActionQueue {
    constructor(httpClient, uiManager) {
        this.httpClient = httpClient;
        this.uiManager = uiManager;
        this.pendingActions = [];
        this.pollInterval = null;
    }
    
    startPolling(interval = 5000) {
        this.pollInterval = setInterval(() => {
            this.fetchPendingActions();
        }, interval);
    }
    
    stopPolling() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }
    
    async fetchPendingActions() {
        try {
            const response = await this.httpClient.get('/api/action/pending');
            if (response.success && response.data.actions.length > 0) {
                for (const action of response.data.actions) {
                    await this.executeAction(action);
                }
            }
        } catch (e) {
            this.uiManager.addLog('获取待执行操作失败', 'error');
        }
    }
    
    async executeAction(action) {
        let success = false;
        let message = '';
        
        try {
            switch (action.action) {
                case 'click':
                    const element = document.querySelector(action.selector);
                    if (element) {
                        element.click();
                        success = true;
                        message = '点击成功';
                    } else {
                        message = '元素未找到';
                    }
                    break;
                default:
                    message = '未知操作类型';
            }
        } catch (e) {
            message = e.message;
        }
        
        await this.reportResult(action.action_id, success, message);
    }
    
    async reportResult(actionId, success, message) {
        try {
            await this.httpClient.post('/api/action/result', {
                action_id: actionId,
                success: success,
                message: message
            });
        } catch (e) {
            this.uiManager.addLog('上报操作结果失败', 'error');
        }
    }
}
```

## 8. 主程序入口

```javascript
(function() {
    'use strict';
    
    const config = ConfigManager.loadConfig();
    
    const uiManager = new UIManager(config);
    const httpClient = new HttpClient(config);
    const serverConnection = new ServerConnection(httpClient, uiManager, config);
    const xhrInterceptor = new XHRInterceptor(config, handleIntercept);
    const fetchInterceptor = new FetchInterceptor(config, handleIntercept);
    const elementClicker = new ElementClicker(uiManager);
    const actionQueue = new ActionQueue(httpClient, uiManager);
    
    let interceptCount = 0;
    let interceptEnabled = false;
    
    function handleIntercept(data) {
        interceptCount++;
        uiManager.updateInterceptCount(interceptCount);
        uiManager.updateLastUpdate();
        
        httpClient.post('/api/data/intercept', data)
            .then(response => {
                if (response.success) {
                    uiManager.addLog(`数据已发送: ${data.source.url}`, 'success');
                } else {
                    uiManager.addLog(`数据发送失败: ${response.error.message}`, 'error');
                }
            })
            .catch(e => {
                uiManager.addLog(`数据发送错误: ${e.message}`, 'error');
            });
    }
    
    uiManager.onConnect = async () => {
        await serverConnection.connect();
    };
    
    uiManager.onElementClickCallback = () => {
        elementClicker.startSelection();
    };
    
    uiManager.onInterceptToggleCallback = () => {
        interceptEnabled = !interceptEnabled;
        if (interceptEnabled) {
            xhrInterceptor.enable();
            fetchInterceptor.enable();
            uiManager.addLog('拦截已启用', 'success');
        } else {
            xhrInterceptor.disable();
            fetchInterceptor.disable();
            uiManager.addLog('拦截已禁用', 'info');
        }
    };
    
    uiManager.onExport = async () => {
        try {
            const response = await httpClient.post('/api/export/excel', {});
            if (response.success) {
                uiManager.addLog(`导出成功: ${response.data.file_path}`, 'success');
            }
        } catch (e) {
            uiManager.addLog(`导出失败: ${e.message}`, 'error');
        }
    };
    
    uiManager.onClear = async () => {
        try {
            const response = await httpClient.delete('/api/data/cache');
            if (response.success) {
                interceptCount = 0;
                uiManager.updateInterceptCount(0);
                uiManager.addLog(`已清空 ${response.data.cleared_count} 条数据`, 'success');
            }
        } catch (e) {
            uiManager.addLog(`清空失败: ${e.message}`, 'error');
        }
    };
    
    uiManager.onSettings = () => {
        uiManager.addLog('设置功能开发中...', 'info');
    };
    
    uiManager.init();
    serverConnection.autoConnect();
    
    GM_registerMenuCommand('显示/隐藏面板', () => {
        uiManager.panel.style.display = uiManager.panel.style.display === 'none' ? 'block' : 'none';
    });
    
    GM_registerMenuCommand('重置配置', () => {
        ConfigManager.resetConfig();
        location.reload();
    });
})();
```

## 9. 扩展指南

### 9.1 添加新的拦截规则

```javascript
GlobalConfig.interceptor.patterns.push('/api/new-endpoint');
```

### 9.2 添加新的操作类型

```javascript
case 'input':
    const inputElement = document.querySelector(action.selector);
    if (inputElement) {
        inputElement.value = action.options.value;
        inputElement.dispatchEvent(new Event('input', { bubbles: true }));
        success = true;
        message = '输入成功';
    }
    break;
```

### 9.3 自定义数据处理

```javascript
function handleIntercept(data) {
    const processedData = customProcess(data);
    httpClient.post('/api/data/intercept', processedData);
}
```
