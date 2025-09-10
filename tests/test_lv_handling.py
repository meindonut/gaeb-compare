# pytest ini import source folder lv_explorer
# vscode settings includes folder lv_explorer for type hinting
from lv_handling import extractInteger, startsWithNumber, textContainsStringTuple
import pytest

@pytest.mark.unit
def test_extractInteger():
    assert extractInteger("4Bla")[0] == 4

@pytest.mark.unit
def test_startsWithNumber():
    assert startsWithNumber("bla") == False
    assert startsWithNumber("2adasd") == True
    assert startsWithNumber("23") == True

@pytest.mark.unit
def test_textContainsStringTuple():
    stringTuple = ("-", "+")
    stringTrue = "-Bla2"
    stringFalse = "sjdf98ada"

    assert textContainsStringTuple(stringTrue, stringTuple) == True
    assert textContainsStringTuple(stringFalse, stringTuple) == False