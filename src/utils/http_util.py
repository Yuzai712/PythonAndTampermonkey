from typing import Dict, Any, Optional
import requests


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
    def get(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> Dict[str, Any]:
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
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def post(url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> Dict[str, Any]:
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
        response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def put(url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> Dict[str, Any]:
        """
        发送 PUT 请求。
        
        参数：
            url: 请求 URL
            data: 表单数据
            json: JSON 数据
            headers: 请求头
            timeout: 超时时间（秒）
        
        返回：
            响应数据字典
        """
        response = requests.put(url, data=data, json=json, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def delete(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> Dict[str, Any]:
        """
        发送 DELETE 请求。
        
        参数：
            url: 请求 URL
            headers: 请求头
            timeout: 超时时间（秒）
        
        返回：
            响应数据字典
        """
        response = requests.delete(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def request(method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        发送通用 HTTP 请求。
        
        参数：
            method: 请求方法
            url: 请求 URL
            **kwargs: 其他参数
        
        返回：
            响应数据字典
        """
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
