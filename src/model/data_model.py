from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class InterceptData:
    """
    拦截数据模型。
    
    用于存储从 Tampermonkey 脚本拦截的 HTTP 响应数据。
    """
    
    id: str
    source_url: str
    source_method: str
    response_status: int
    response_body: Any
    source_timestamp: Optional[str] = None
    response_headers: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None
    received_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InterceptData':
        """
        从字典创建实例。
        
        参数：
            data: 数据字典
        
        返回：
            InterceptData 实例
        """
        source = data.get('source', {})
        response = data.get('response', {})
        metadata = data.get('metadata', {})
        
        return cls(
            id=data.get('id', ''),
            source_url=source.get('url', ''),
            source_method=source.get('method', 'GET'),
            source_timestamp=source.get('timestamp'),
            response_status=response.get('status', 0),
            response_headers=response.get('headers'),
            response_body=response.get('body'),
            metadata=metadata,
            received_at=datetime.now()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典。
        
        返回：
            数据字典
        """
        return {
            'id': self.id,
            'source': {
                'url': self.source_url,
                'method': self.source_method,
                'timestamp': self.source_timestamp
            },
            'response': {
                'status': self.response_status,
                'headers': self.response_headers,
                'body': self.response_body
            },
            'metadata': self.metadata,
            'received_at': self.received_at.isoformat() if self.received_at else None
        }


@dataclass
class ActionData:
    """
    操作数据模型。
    
    用于存储待执行的页面操作指令。
    """
    
    id: str
    action_type: str
    selector: str
    options: Optional[Dict[str, Any]] = None
    status: str = 'pending'
    result: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionData':
        """
        从字典创建实例。
        
        参数：
            data: 数据字典
        
        返回：
            ActionData 实例
        """
        return cls(
            id=data.get('id', ''),
            action_type=data.get('action', 'click'),
            selector=data.get('selector', ''),
            options=data.get('options'),
            status=data.get('status', 'pending'),
            result=data.get('result'),
            created_at=datetime.now()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典。
        
        返回：
            数据字典
        """
        return {
            'id': self.id,
            'action': self.action_type,
            'selector': self.selector,
            'options': self.options,
            'status': self.status,
            'result': self.result,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None
        }


@dataclass
class ExportRecord:
    """
    导出记录模型。
    
    用于存储 Excel 导出的历史记录。
    """
    
    id: str
    filename: str
    file_path: str
    file_size: int
    row_count: int
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExportRecord':
        """
        从字典创建实例。
        
        参数：
            data: 数据字典
        
        返回：
            ExportRecord 实例
        """
        return cls(
            id=data.get('id', ''),
            filename=data.get('filename', ''),
            file_path=data.get('file_path', ''),
            file_size=data.get('file_size', 0),
            row_count=data.get('row_count', 0),
            created_at=datetime.now()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典。
        
        返回：
            数据字典
        """
        return {
            'id': self.id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'row_count': self.row_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
