import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List

from src.service.cache_service import ThreadSafeCache
from src.model.data_model import InterceptData, ExportRecord
from src.utils.excel_util import ExcelUtil
from src.utils.file_util import FileUtil
from src.utils.logger import Logger


class DataService:
    """
    数据服务，处理数据的存储、查询和导出。
    
    职责：
    - 存储拦截数据
    - 查询缓存数据
    - 导出数据到 Excel
    - 管理数据缓存
    """
    
    def __init__(self, max_size: int = 1000, export_dir: str = './exports'):
        """
        初始化数据服务。
        
        参数：
            max_size: 缓存最大容量
            export_dir: 导出目录
        """
        self.cache = ThreadSafeCache(max_size)
        self.export_dir = export_dir
        self.export_history: List[ExportRecord] = []
        self.logger = Logger.get_instance('data_service')
        
        FileUtil.ensure_dir(export_dir)
    
    def store_data(self, data: Dict[str, Any]) -> str:
        """
        存储数据。
        
        参数：
            data: 数据字典
        
        返回：
            数据 ID
        """
        data_id = self._generate_data_id()
        data['id'] = data_id
        
        intercept_data = InterceptData.from_dict(data)
        self.cache.set(data_id, intercept_data.to_dict())
        
        self.logger.info(f"存储数据: {data_id}")
        return data_id
    
    def get_data(self, data_id: str) -> Optional[Dict[str, Any]]:
        """
        获取数据。
        
        参数：
            data_id: 数据 ID
        
        返回：
            数据字典
        """
        return self.cache.get(data_id)
    
    def get_data_list(self, page: int = 1, size: int = 20, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        获取数据列表。
        
        参数：
            page: 页码
            size: 每页数量
            filters: 过滤条件
        
        返回：
            分页数据字典
        """
        all_data = self.cache.values()
        
        if filters:
            all_data = [d for d in all_data if self._apply_filters(d, filters)]
        
        total = len(all_data)
        start = (page - 1) * size
        end = start + size
        
        items = all_data[start:end]
        
        return {
            'items': items,
            'pagination': {
                'page': page,
                'size': size,
                'total': total,
                'total_pages': (total + size - 1) // size
            }
        }
    
    def clear_all_data(self) -> int:
        """
        清空所有数据。
        
        返回：
            清空的数据数量
        """
        count = self.cache.clear()
        self.logger.info(f"清空数据: {count} 条")
        return count
    
    def export_to_excel(self, format_config: Optional[Dict[str, Any]] = None, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        导出数据到 Excel。
        
        参数：
            format_config: 格式配置
            filters: 过滤条件
        
        返回：
            导出文件路径
        """
        all_data = self.cache.values()
        
        if filters:
            all_data = [d for d in all_data if self._apply_filters(d, filters)]
        
        if not all_data:
            raise ValueError("没有数据可导出")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"export_{timestamp}.xlsx"
        file_path = os.path.join(self.export_dir, filename)
        
        wb = ExcelUtil.create_workbook()
        ws = ExcelUtil.create_sheet(wb, "数据")
        
        headers = ['ID', '来源URL', '请求方法', '状态码', '接收时间']
        ExcelUtil.write_headers(ws, headers)
        
        row_data = []
        for item in all_data:
            row_data.append([
                item.get('id', ''),
                item.get('source', {}).get('url', ''),
                item.get('source', {}).get('method', ''),
                item.get('response', {}).get('status', ''),
                item.get('received_at', '')
            ])
        
        ExcelUtil.write_data(ws, row_data, start_row=2)
        ExcelUtil.apply_header_style(ws)
        ExcelUtil.auto_fit_columns(ws)
        ExcelUtil.save(wb, file_path)
        
        export_record = ExportRecord(
            id=str(uuid.uuid4()),
            filename=filename,
            file_path=file_path,
            file_size=FileUtil.get_size(file_path),
            row_count=len(all_data),
            created_at=datetime.now()
        )
        self.export_history.append(export_record)
        
        self.logger.info(f"导出数据: {file_path}")
        return file_path
    
    def get_export_history(self) -> List[Dict[str, Any]]:
        """
        获取导出历史。
        
        返回：
            导出历史列表
        """
        return [record.to_dict() for record in self.export_history]
    
    def get_data_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        获取数据数量。
        
        参数：
            filters: 过滤条件
        
        返回：
            数据数量
        """
        all_data = self.cache.values()
        
        if filters:
            all_data = [d for d in all_data if self._apply_filters(d, filters)]
        
        return len(all_data)
    
    def _generate_data_id(self) -> str:
        """
        生成数据 ID。
        
        返回：
            唯一的数据 ID
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        short_uuid = str(uuid.uuid4())[:8]
        return f"data_{timestamp}_{short_uuid}"
    
    def _apply_filters(self, data: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """
        应用过滤条件。
        
        参数：
            data: 数据字典
            filters: 过滤条件
        
        返回：
            是否符合条件
        """
        if 'source_url' in filters:
            source_url = data.get('source', {}).get('url', '')
            if filters['source_url'] not in source_url:
                return False
        
        if 'start_time' in filters:
            received_at = data.get('received_at', '')
            if received_at and received_at < filters['start_time']:
                return False
        
        if 'end_time' in filters:
            received_at = data.get('received_at', '')
            if received_at and received_at > filters['end_time']:
                return False
        
        return True
