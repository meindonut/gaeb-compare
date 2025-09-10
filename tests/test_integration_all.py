# pytest ini import source folder lv_explorer
# vscode settings includes folder lv_explorer for type hinting

# ----- for direct debugging ------
def debugger_is_active() -> bool:
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None

if debugger_is_active:
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\lv_explorer')))
# ----- for direct debugging -

# imports
import pytest
from file_manager import FileManager, get_file_name
from database import LvDatabase
from lv_handling import load_lv, save_lv

# globals
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.\\test_project'))
lv_file_name = "Pruefdatei GAEB DA XML 3.3 - Bauausfuehrung - V 04 04 2024.x83"
lv_file = os.path.abspath(os.path.join(os.path.dirname(__file__), f".\\pruefung_gaeb_da_xml_3_3\\bauausfuehrung\\{lv_file_name}"))

fm = FileManager(project_dir)
db = LvDatabase(project_dir,fm)

@pytest.mark.integration
def test_integration():
    export_path = fm.project_path + "\\" + get_file_name(lv_file, with_extension=False)

    # load and save lv
    df = load_lv(lv_file)
    lv_paths_import = save_lv(df, export_path)

    # import lv into database
    df_prep = db.prepare_for_database(df, lv_paths_import)
    df_prep["Link"] = [""] * df_prep.shape[0]
    df_prep["Basis"] = [False] * df_prep.shape[0]
    db.add_lv_df(df_prep)

    # save database
    db.save()

    # load again and test
    db.load()
#    assert db._df.equals(df_prep)

# ----- for direct debugging ------
if debugger_is_active:
    test_integration()