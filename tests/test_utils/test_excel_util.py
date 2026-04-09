import pytest
import tempfile
import os
from src.utils.excel_util import ExcelUtil


class TestExcelUtil:
    
    def test_create_workbook(self):
        wb = ExcelUtil.create_workbook()
        assert wb is not None
        assert 'Sheet' in wb.sheetnames
    
    def test_create_sheet(self):
        wb = ExcelUtil.create_workbook()
        sheet = ExcelUtil.create_sheet(wb, 'TestSheet')
        assert sheet.title == 'TestSheet'
        assert 'TestSheet' in wb.sheetnames
        assert 'Sheet' not in wb.sheetnames
    
    def test_write_headers(self):
        wb = ExcelUtil.create_workbook()
        sheet = ExcelUtil.create_sheet(wb, 'Test')
        headers = ['ID', 'Name', 'Value']
        ExcelUtil.write_headers(sheet, headers)
        assert sheet.cell(1, 1).value == 'ID'
        assert sheet.cell(1, 2).value == 'Name'
        assert sheet.cell(1, 3).value == 'Value'
    
    def test_write_data(self):
        wb = ExcelUtil.create_workbook()
        sheet = ExcelUtil.create_sheet(wb, 'Test')
        data = [
            ['1', 'Item1', 100],
            ['2', 'Item2', 200]
        ]
        ExcelUtil.write_data(sheet, data, start_row=2)
        assert sheet.cell(2, 1).value == '1'
        assert sheet.cell(2, 2).value == 'Item1'
        assert sheet.cell(2, 3).value == 100
        assert sheet.cell(3, 1).value == '2'
        assert sheet.cell(3, 2).value == 'Item2'
        assert sheet.cell(3, 3).value == 200
    
    def test_save(self):
        wb = ExcelUtil.create_workbook()
        sheet = ExcelUtil.create_sheet(wb, 'Test')
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        try:
            ExcelUtil.save(wb, temp_path)
            assert os.path.exists(temp_path)
            assert os.path.getsize(temp_path) > 0
        finally:
            os.unlink(temp_path)
