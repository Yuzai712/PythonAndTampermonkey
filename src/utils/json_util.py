import json
from typing import Dict, Any


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
    def read(path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
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
        with open(path, 'r', encoding=encoding) as f:
            return json.load(f)
    
    @staticmethod
    def write(path: str, data: Dict[str, Any], encoding: str = 'utf-8', indent: int = 4):
        """
        写入 JSON 文件。
        
        参数：
            path: 文件路径
            data: 数据字典
            encoding: 编码格式
            indent: 缩进空格数
        """
        with open(path, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def dumps(data: Dict[str, Any], indent: int = 4) -> str:
        """
        将字典转换为 JSON 字符串。
        
        参数：
            data: 数据字典
            indent: 缩进空格数
        
        返回：
            JSON 字符串
        """
        return json.dumps(data, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def loads(json_str: str) -> Dict[str, Any]:
        """
        将 JSON 字符串解析为字典。
        
        参数：
            json_str: JSON 字符串
        
        返回：
            数据字典
        """
        return json.loads(json_str)
    
    @staticmethod
    def is_valid(json_str: str) -> bool:
        """
        验证 JSON 字符串是否有效。
        
        参数：
            json_str: JSON 字符串
        
        返回：
            是否有效
        """
        try:
            json.loads(json_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        深度合并两个字典。
        
        参数：
            base: 基础字典
            override: 覆盖字典
        
        返回：
            合并后的字典
        """
        result = base.copy()
        JsonUtil._deep_update(result, override)
        return result
    
    @staticmethod
    def _deep_update(target: Dict[str, Any], source: Dict[str, Any]):
        """
        深度更新字典。
        
        参数：
            target: 目标字典
            source: 源字典
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                JsonUtil._deep_update(target[key], value)
            else:
                target[key] = value
