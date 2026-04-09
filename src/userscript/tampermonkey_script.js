
// ==UserScript==
// @name         Tampermonkey 本地服务器助手
// @namespace    http://tampermonkey.net/
// @version      1.0.0
// @description  与本地Python服务器通信的Tampermonkey脚本
// @author       You
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @grant        GM_notification
// @connect      127.0.0.1
// @connect      localhost
// ==/UserScript==

(function() {
    'use strict';

    const CONFIG = {
        serverUrl: 'http://127.0.0.1:8080',
        pingInterval: 5000,
        retryCount: 3,
        retryDelay: 1000
    };

    let isServerConnected = false;
    let pingIntervalId = null;

    function init() {
        console.log('[Tampermonkey Helper] 初始化中...');
        createUI();
        startServerCheck();
        setupXHRInterceptor();
    }

    function createUI() {
        const container = document.createElement('div');
        container.id = 'tm-helper-container';
        container.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 999999;
            background: white;
            border: 2px solid #4CAF50;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            font-family: Arial, sans-serif;
            min-width: 200px;
        `;

        const title = document.createElement('h3');
        title.textContent = '本地服务器助手';
        title.style.cssText = 'margin: 0 0 10px 0; color: #333; font-size: 16px;';

        const statusDiv = document.createElement('div');
        statusDiv.id = 'tm-helper-status';
        statusDiv.style.cssText = 'margin-bottom: 10px; padding: 8px; border-radius: 4px; font-weight: bold;';

        const buttonContainer = document.createElement('div');
        buttonContainer.style.cssText = 'display: flex; gap: 8px; margin-bottom: 10px;';

        const checkBtn = document.createElement('button');
        checkBtn.textContent = '检查连接';
        checkBtn.style.cssText = 'flex: 1; padding: 6px 12px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer;';
        checkBtn.onclick = checkServerConnection;

        const clearBtn = document.createElement('button');
        clearBtn.textContent = '清空日志';
        clearBtn.style.cssText = 'flex: 1; padding: 6px 12px; background: #ff9800; color: white; border: none; border-radius: 4px; cursor: pointer;';
        clearBtn.onclick = clearLogs;

        const logContainer = document.createElement('div');
        logContainer.id = 'tm-helper-logs';
        logContainer.style.cssText = 'max-height: 200px; overflow-y: auto; background: #f5f5f5; border-radius: 4px; padding: 8px; font-size: 12px;';

        const toggleBtn = document.createElement('button');
        toggleBtn.textContent = '▼';
        toggleBtn.style.cssText = 'position: absolute; top: 5px; right: 5px; background: none; border: none; cursor: pointer; font-size: 14px;';
        toggleBtn.onclick = toggleContainer;

        container.appendChild(toggleBtn);
        container.appendChild(title);
        container.appendChild(statusDiv);
        container.appendChild(buttonContainer);
        container.appendChild(logContainer);

        document.body.appendChild(container);
        updateStatus(false);
    }

    function toggleContainer() {
        const container = document.getElementById('tm-helper-container');
        const elements = container.querySelectorAll('h3, #tm-helper-status, div, button:not(:first-child)');
        elements.forEach(el => {
            el.style.display = el.style.display === 'none' ? '' : 'none';
        });
    }

    function updateStatus(connected) {
        isServerConnected = connected;
        const statusDiv = document.getElementById('tm-helper-status');
        if (statusDiv) {
            if (connected) {
                statusDiv.textContent = '状态: 已连接 ✓';
                statusDiv.style.backgroundColor = '#d4edda';
                statusDiv.style.color = '#155724';
            } else {
                statusDiv.textContent = '状态: 未连接 ✗';
                statusDiv.style.backgroundColor = '#f8d7da';
                statusDiv.style.color = '#721c24';
            }
        }
    }

    function addLog(message, type = 'info') {
        const logContainer = document.getElementById('tm-helper-logs');
        if (logContainer) {
            const timestamp = new Date().toLocaleTimeString();
            const logEntry = document.createElement('div');
            logEntry.style.cssText = 'margin-bottom: 4px; padding: 2px 0;';
            
            let color = '#333';
            if (type === 'success') color = '#28a745';
            if (type === 'error') color = '#dc3545';
            if (type === 'warning') color = '#ffc107';
            
            logEntry.style.color = color;
            logEntry.textContent = `[${timestamp}] ${message}`;
            logContainer.appendChild(logEntry);
            logContainer.scrollTop = logContainer.scrollHeight;
        }
        console.log(`[Tampermonkey Helper] [${type.toUpperCase()}] ${message}`);
    }

    function clearLogs() {
        const logContainer = document.getElementById('tm-helper-logs');
        if (logContainer) {
            logContainer.innerHTML = '';
        }
    }

    function sendRequest(url, method, data, callback) {
        const fullUrl = CONFIG.serverUrl + url;
        
        GM_xmlhttpRequest({
            method: method,
            url: fullUrl,
            headers: {
                'Content-Type': 'application/json'
            },
            data: data ? JSON.stringify(data) : undefined,
            onload: function(response) {
                try {
                    const result = JSON.parse(response.responseText);
                    if (callback) callback(result);
                } catch (e) {
                    addLog('解析响应失败: ' + e.message, 'error');
                    if (callback) callback(null);
                }
            },
            onerror: function(error) {
                addLog('请求失败: ' + error, 'error');
                if (callback) callback(null);
            }
        });
    }

    function checkServerConnection() {
        addLog('检查服务器连接...', 'info');
        sendRequest('/api/health/ping', 'GET', null, function(result) {
            if (result && result.success) {
                addLog('服务器连接成功!', 'success');
                updateStatus(true);
            } else {
                addLog('服务器连接失败', 'error');
                updateStatus(false);
            }
        });
    }

    function startServerCheck() {
        checkServerConnection();
        pingIntervalId = setInterval(checkServerConnection, CONFIG.pingInterval);
    }

    function setupXHRInterceptor() {
        const originalOpen = XMLHttpRequest.prototype.open;
        const originalSend = XMLHttpRequest.prototype.send;

        XMLHttpRequest.prototype.open = function(method, url) {
            this._method = method;
            this._url = url;
            return originalOpen.apply(this, arguments);
        };

        XMLHttpRequest.prototype.send = function(body) {
            const self = this;
            const originalOnReadyStateChange = this.onreadystatechange;

            this.onreadystatechange = function() {
                if (self.readyState === 4) {
                    captureResponse(self);
                }
                if (originalOnReadyStateChange) {
                    originalOnReadyStateChange.apply(this, arguments);
                }
            };

            return originalSend.apply(this, arguments);
        };
    }

    function captureResponse(xhr) {
        if (!isServerConnected) return;

        try {
            const responseData = {
                source: {
                    url: xhr._url,
                    method: xhr._method,
                    timestamp: new Date().toISOString()
                },
                response: {
                    status: xhr.status,
                    statusText: xhr.statusText,
                    headers: {},
                    body: null
                },
                metadata: {
                    page_url: window.location.href,
                    user_agent: navigator.userAgent
                }
            };

            try {
                responseData.response.body = JSON.parse(xhr.responseText);
            } catch (e) {
                responseData.response.body = xhr.responseText;
            }

            sendRequest('/api/data/intercept', 'POST', responseData, function(result) {
                if (result && result.success) {
                    addLog('数据已发送到服务器: ' + xhr._url, 'success');
                }
            });
        } catch (e) {
            addLog('捕获响应失败: ' + e.message, 'error');
        }
    }

    window.addEventListener('load', init);
})();

