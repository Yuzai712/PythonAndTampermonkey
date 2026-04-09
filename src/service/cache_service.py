import threading
from collections import OrderedDict
from datetime import datetime
from typing import Dict, Any, Optional, List


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
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
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
                return self._cache[key].get('data')
            return None
    
    def set(self, key: str, value: Dict[str, Any]):
        """
        设置缓存值。
        
        参数：
            key: 缓存键
            value: 缓存值
        """
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = {
                'data': value,
                'timestamp': datetime.now()
            }
            
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
    
    def keys(self) -> List[str]:
        """
        获取所有缓存键。
        
        返回：
            缓存键列表
        """
        with self._lock:
            return list(self._cache.keys())
    
    def values(self) -> List[Dict[str, Any]]:
        """
        获取所有缓存值。
        
        返回：
            缓存值列表
        """
        with self._lock:
            return [item.get('data') for item in self._cache.values()]
    
    def get_all(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有缓存数据。
        
        返回：
            缓存字典
        """
        with self._lock:
            return {k: v.get('data') for k, v in self._cache.items()}
