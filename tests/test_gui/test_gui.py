
import pytest


class TestGUIModule:
    def test_import_gui(self):
        from src.gui import MainWindow
        assert MainWindow is not None

    def test_main_import(self):
        import main
        assert main is not None

