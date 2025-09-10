import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox

import os
import sys
import pickle
import nltk # needed for dist

def get_long_abs_path(abs_path):
    if not abs_path.startswith(u"\\\\?\\"):     # convert to UNC path for extended length > 260 characters
            abs_path = u"\\\\?\\" + abs_path
    return abs_path

def get_short_abs_path(abs_path):
    if abs_path.startswith(u"\\\\?\\"): # convert back to normal paths
            abs_path = os.path.normpath(abs_path.removeprefix(u"\\\\?\\"))
    return abs_path

def write_file_abs_path(content: str, abs_path: str, createDir: bool = True):
    abs_path = get_long_abs_path(abs_path)

    if createDir:
        try:
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        except:
            print("Folder could not be created")
    try:
        f = open(abs_path, "w", encoding='utf-8')
        f.write(content)  
        f.close()
    except:
        print("File not written")
        return False

    return True

def load_pickle():
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS  # PyInstaller sets this for bundled apps
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        pickle_file_path = os.path.join(base_dir, "data", "german.pickle")

        with open(pickle_file_path, 'rb') as f:                                                  # Load the pickle file manually
            sentence_tokenizer = pickle.load(f)

        return sentence_tokenizer

def keep_n_lowest_order_subfolders(paths, n):
    new_paths = []
    for path in paths:
        new_paths.append(keep_n_lowest_order_subfolder(path, n))
    return new_paths

def keep_n_lowest_order_subfolder(path, n):
    norm_path = os.path.normpath(path)
    parts = norm_path.split(os.sep)
    
    if n > len(parts):
        n = len(parts)

    selected_parts = parts[-n:]
    return os.path.join(*selected_parts)

def keep_n_highest_order_subfolder(path, n):
    norm_path = os.path.normpath(path)
    parts = norm_path.split(os.sep)
    
    if n > len(parts):
        n = len(parts)

    selected_parts = parts[0:n]
    return os.path.join(*selected_parts)

def keep_highest_order_subfolder(path):
    return keep_n_highest_order_subfolder(path, 1)


def read_files(file_paths):
    data = []
    for file_path in file_paths:
        data.append(read_file(file_path))
    return data

def read_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
def read_txt_files_from_folder(folder_path):
    files_content = []
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".txt"):  # Ensure only .txt files are read
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        files_content.append(file.read())
                        file_paths.append(file_path)
    return files_content, file_paths

# Helper function to get the relative subfolder path
def get_subfolder_path(full_path, base_folder):
    return os.path.relpath(full_path, base_folder)

# Helper function to get the file name from a path
def get_file_name(file_path, with_extension = True):
    file_name = os.path.basename(file_path)
    if with_extension:
        return file_name
    else:
        return os.path.splitext(file_name)[0]

def get_file_names(file_paths):
    if file_paths is None:
        return None
    
    file_names = []
    for file_path in file_paths:
        file_names.append(get_file_name(file_path))
    return file_names


def get_lowest_folder(path):
    if os.path.isdir(path):
        folder = path
    else:
        folder = os.path.dirname(path)
    return os.path.basename(os.path.normpath(folder))

def get_lowest_folders(paths):
    folders = []
    for path in paths:
        folders.append(get_lowest_folder(path))
    return folders

def list_files_in_folder(folder_path):
    # Return None if the input is None
    if folder_path is None:
        return None
    
    try:
        # Check if the provided path is a file
        if os.path.isfile(folder_path):
            # Use the directory containing the file
            folder_path = os.path.dirname(folder_path)

        # Check if the folder path exists and is a directory
        if not os.path.isdir(folder_path):
            raise ValueError(f"The path '{folder_path}' is not a valid directory.")

        # List all files in the folder
        files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        return files

    except Exception as e:
        print(f"Error: {e}")
        return []


class FileManager:
    def __init__(self, project_path):
        self.base_folder_name = 'Base'
        self.classification_filename = "zuordnung.xlsx"
        self.project_path = project_path
    
    def get_abs_paths_of(self, rel_file_paths_in_project):
        abs_paths = []
        for rfp in rel_file_paths_in_project:
            abs_paths.append(self.get_abs_path_of(rfp))
        return abs_paths
        
    def get_abs_path_of(self, rel_file_path_in_project: str):
        abs_path = os.path.join(self.project_path, rel_file_path_in_project)
        abs_path = get_long_abs_path(abs_path)
        return os.path.normpath(abs_path)

    def get_rel_path_of(self, abs_file_path_in_project: str):
        abs_file_path_in_project = get_short_abs_path(abs_file_path_in_project)
        return os.path.relpath(abs_file_path_in_project, start=self.project_path)

    def get_rel_paths_of(self, abs_file_path_in_project):
        rel_paths = []
        for rfp in abs_file_path_in_project:
            rel_paths.append(self.get_rel_path_of(rfp))
        return rel_paths
    
    def write_file_rel_path(self, content: str, rel_path: str, createDir: bool = True):
        abs_path = self.get_abs_path_of(rel_path)
        return write_file_abs_path(content, abs_path, createDir)


    def get_path_ui(self, extensions):
        file = QFileDialog.getOpenFileName(None, 'Datei auswählen', self.project_path, extensions)
        path = file[0]
        if not os.path.exists(path):
            QMessageBox.warning(self, "Warning", f"The assignment file {path} does not exist.")
            return None
        else:
            return path
        
    def load_text_file(self, rel_path):
        abs_path = self.get_abs_path_of(rel_path)
        with open(abs_path, 'r', encoding='utf-8') as file:  # Setze das encoding auf 'utf-8'
            file_content = file.read()
        return file_content
        

    def get_base_folder_path(self):
        base_path = os.path.join(self.project_path, self.base_folder_name)
        os.path.normpath(base_path)
        if os.path.exists(base_path) and os.path.isdir(base_path):
            return base_path
        else:
            return None
        
    def list_comparison_folders(self):
        try:
            subfolders = [f.name for f in os.scandir(self.project_path) if f.is_dir()]
            subfolders.remove(self.base_folder_name)
            paths = [os.path.join(self.project_path, subfolder) for subfolder in subfolders]
            return paths
        except FileNotFoundError:
            return f"Error: The directory {self.project_path} was not found."
        except PermissionError:
            return f"Error: You do not have permission to access {self.project_path}"
        
    def load_classification(self):
        excel_path = self.project_path + "\\" + self.classification_filename
        try:
            classification_df = pd.read_excel(io = excel_path, sheet_name = "tKategorien", index_col=0)
            classification_df = classification_df.sort_index()
        except Exception as e:
            print("Fehler beim Laden der Zuordnungs-Datei")
            return None

        return classification_df
    

