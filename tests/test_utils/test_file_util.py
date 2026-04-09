import pytest
import tempfile
import os
from src.utils.file_util import FileUtil


class TestFileUtil:
    
    def test_ensure_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = os.path.join(temp_dir, 'test', 'nested', 'dir')
            assert not os.path.exists(test_dir)
            FileUtil.ensure_dir(test_dir)
            assert os.path.exists(test_dir)
    
    def test_exists(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            assert FileUtil.exists(temp_path) is True
            assert FileUtil.exists(temp_path + '_not_exists') is False
        finally:
            os.unlink(temp_path)
    
    def test_get_filename(self):
        assert FileUtil.get_filename('/path/to/file.txt') == 'file.txt'
        assert FileUtil.get_filename('file.txt') == 'file.txt'
    
    def test_get_extension(self):
        assert FileUtil.get_extension('/path/to/file.txt') == 'txt'
        assert FileUtil.get_extension('file.jpg') == 'jpg'
        assert FileUtil.get_extension('file') == ''
    
    def test_join(self):
        assert FileUtil.join('path', 'to', 'file.txt').endswith('path/to/file.txt')
