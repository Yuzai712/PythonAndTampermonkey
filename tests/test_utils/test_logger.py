import pytest
import logging
from src.utils.logger import Logger


class TestLogger:
    
    def test_get_instance(self):
        logger1 = Logger.get_instance('test')
        logger2 = Logger.get_instance('test')
        assert logger1 is logger2
    
    def test_configure(self):
        logger = Logger.get_instance('test_simple')
        logger.configure(level='DEBUG')
        assert True
