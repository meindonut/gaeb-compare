from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout


class PropertiesWindow(QDialog):
    def __init__(self, name_value, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Eigenschaften")

        # Hauptlayout
        main_layout = QVBoxLayout(self)

        # Tabellarisches Layout für Eigenschaften
        grid_layout = QGridLayout()

        # Erste Zeile: Name
        name_label = QLabel("Name:")
        name_value_label = QLabel(name_value)
        name_label.setAlignment(Qt.AlignLeft)
        name_value_label.setAlignment(Qt.AlignLeft)
        grid_layout.addWidget(name_label, 0, 0)
        grid_layout.addWidget(name_value_label, 0, 1)

        # Zweite Zeile: Pfad
        path_label = QLabel("Pfad:")
        self.path_input = QLineEdit()
        self.path_input.setAlignment(Qt.AlignLeft)
        grid_layout.addWidget(path_label, 1, 0)
        grid_layout.addWidget(self.path_input, 1, 1)

        # Grid-Layout in das Hauptlayout einfügen
        main_layout.addLayout(grid_layout)

        # Button-Leiste
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Abbrechen")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        # Buttons mit Funktionen verknüpfen
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        # Buttons ins Hauptlayout einfügen
        main_layout.addStretch()  # Platz zwischen Tabelle und Buttons
        main_layout.addLayout(button_layout)

    def get_path(self):
        """Gibt den Wert aus dem Pfad-Eingabefeld zurück."""
        return self.path_input.text()