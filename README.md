# GAEB Compare
opens GAEB files, finds similaritites and compares them visually

![Screenshot of the example import.](example_screenshot.jpg)

## Use it:
download *.exe file

## Change it:

### Install required modules in venv

`python -m venv .venv`

`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force`

`.venv/Scripts/activate.ps1`

`pip install -r requirements.txt`


### run tests

`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force`

`.venv/Scripts/activate.ps1`

`pytest -v -m unit           # unit tests`

`pytest -v -m integration    # integration tests`

### build:

`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force`

`.venv/Scripts/activate.ps1`

`pyinstaller --noconsole --clean --name LV_Pruefer --add-data "data/german.pickle:data" lv_explorer/main.py`

### create ui code:

`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force`

`.venv/Scripts/activate.ps1`

`pyside6-uic ui/project_window.ui -o lv_explorer/ui_project_window.py`

## To-Dos:
- ...