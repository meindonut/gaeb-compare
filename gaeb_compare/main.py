from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from window_project import ProjectWindow
from window_startup import StartupWindow
from file_manager import FileManager
from database import LvDatabase

# Set the attribute before creating the QApplication instance
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

def main():
    app = QApplication([])
    # Launch Startup Window
    startup_window = StartupWindow()
    startup_window.show()
    print("start window: open")
    app.exec()
    print("start window: closed")
    # Get the selected project path
    project_path = startup_window.get_project_path()

    if project_path:
        print(f"project window: Open with path '{project_path}'")
        # Launch Main Window with the project path
        fm = FileManager(project_path)
        db = LvDatabase(project_path, fm)

        if db.exists():
            db.load()
            db.refresh_calculated_values()

        window = ProjectWindow(fm, db)
        window.show()
        app.exec()
        print(f"project window: closed")

if __name__ == "__main__":
    main()
