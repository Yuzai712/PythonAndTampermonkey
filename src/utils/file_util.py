import os
import shutil
from typing import List


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
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def exists(path: str) -> bool:
        """
        检查文件或目录是否存在。
        
        参数：
            path: 路径
        
        返回：
            是否存在
        """
        return os.path.exists(path)
    
    @staticmethod
    def delete(path: str) -> bool:
        """
        删除文件或目录。
        
        参数：
            path: 路径
        
        返回：
            是否删除成功
        """
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_filename(path: str) -> str:
        """
        获取文件名（含扩展名）。
        
        参数：
            path: 文件路径
        
        返回：
            文件名
        """
        return os.path.basename(path)
    
    @staticmethod
    def get_extension(path: str) -> str:
        """
        获取文件扩展名。
        
        参数：
            path: 文件路径
        
        返回：
            扩展名（不含点）
        """
        _, ext = os.path.splitext(path)
        return ext[1:] if ext else ''
    
    @staticmethod
    def join(*paths) -> str:
        """
        连接路径。
        
        参数：
            *paths: 路径片段
        
        返回：
            连接后的路径
        """
        return os.path.join(*paths)
    
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
        import glob
        pattern_path = FileUtil.join(dir_path, pattern)
        return glob.glob(pattern_path)
    
    @staticmethod
    def get_size(path: str) -> int:
        """
        获取文件大小。
        
        参数：
            path: 文件路径
        
        返回：
            文件大小（字节）
        """
        return os.path.getsize(path)
    
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
        try:
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src):
                shutil.copytree(src, dst)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_size(path: str) -> int:
        """
        获取文件大小。
        
        参数：
            path: 文件路径
        
        返回：
            文件大小（字节）
        """
        if os.path.exists(path):
            return os.path.getsize(path)
        return 0
