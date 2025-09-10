from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QApplication
from PySide6.QtCore import Qt
import os

class StartupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.project_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("GAEB Compare: Start")
        self.setFixedSize(300, 100)  # Set fixed window size

        # Main Layout (Vertical)
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)  # Adjust margins for spacing

        # Example text (Wrapped with alignment)
        self.label = QLabel("Willkommen bei GAEB Compare \n\nBitte öffne einen Projektordner.")
        self.label.setWordWrap(True)  # Allow text wrapping
        self.label.setAlignment(Qt.AlignLeft)  # Center align text
        layout.addWidget(self.label)

        # Spacer to push buttons to the bottom
        layout.addStretch()

        # Button Layout (Horizontal)
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push buttons to the right

        # Select Directory Button
        self.select_button = QPushButton("Öffnen")
        self.select_button.setFixedSize(60, 25)  # Fixed size
        self.select_button.clicked.connect(self.select_project)
        button_layout.addWidget(self.select_button)
        
        # Exit Button
        self.exit_button = QPushButton("Beenden")
        self.exit_button.setFixedSize(60, 25)  # Fixed size
        self.exit_button.clicked.connect(self.exit_application)
        button_layout.addWidget(self.exit_button)

        # Add button layout to main layout
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def select_project(self):
        self.select_directory()

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Öffne Projekt Ordner")
        if directory:
            self.project_path = os.path.normpath(directory)
            self.close()

    def exit_application(self):
        QApplication.instance().quit()

    def get_project_path(self):
        return self.project_path
    
