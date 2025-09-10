# pytest ini import source folder lv_explorer
# vscode settings includes folder lv_explorer for type hinting

# ----- for direct debugging ------
def debugger_is_active() -> bool:
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None

if debugger_is_active:
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\lv_explorer')))
# ----- for direct debugging ------


test_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.\\test_project'))

from file_manager import FileManager
import pytest

test_fm = FileManager(test_project_dir)
test_file_rel_path = "test_dir\\empty_file.txt"
test_file_abs_path = u"\\\\?\\" + os.path.abspath(os.path.join(os.path.dirname(__file__), '.\\test_project\\test_dir\\empty_file.txt'))

@pytest.mark.unit
def test_get_rel_path_of():
    rel_path = test_fm.get_rel_path_of(test_file_abs_path)
    assert rel_path == test_file_rel_path

@pytest.mark.unit
def test_get_abs_path_of():
    abs_path = test_fm.get_abs_path_of(test_file_rel_path)
    assert abs_path == test_file_abs_path


# ----- for direct debugging ------
if debugger_is_active:
    test_get_rel_path_of()
    test_get_abs_path_of()