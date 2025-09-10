# pytest ini import source folder lv_explorer
# vscode settings includes folder lv_explorer for type hinting

# ----- for direct debugging ------
def debugger_is_active() -> bool:
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None

if debugger_is_active:
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\lv_explorer')))
# ----- for direct debugging ------


from database import LvDatabase
import pandas as pd
from file_manager import FileManager
import pytest

#sample data
data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'Height': [175, 160, 185]
    }
df = pd.DataFrame(data)

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.\\test_project'))
fm = FileManager(project_dir)
database = LvDatabase(project_dir,fm)


@pytest.mark.unit
def test_combine_columns_as_list():
    df_input = df
    outputTrue1 = ["Alice -> 25", "Bob -> 30", "Charlie -> 35"]
    output1 = LvDatabase.combine_columns_as_list(df_input, "Name", "Age")
    assert output1 == outputTrue1

    output2 = LvDatabase.combine_columns_as_list(df_input, "Name", "Age", "Height")
    outputTrue2 = ["Alice -> 25 -> 175", "Bob -> 30 -> 160", "Charlie -> 35 -> 185"]
    assert output2 == outputTrue2

    output3 = LvDatabase.combine_columns_as_list(df_input, "Age")
    outputTrue3 = ["25", "30", "35"]
    assert output3 == outputTrue3

if debugger_is_active:
 test_combine_columns_as_list()