from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel

from database import LvDatabase # for type hinting

class AddLinkDialog(QDialog):
    def __init__(self, base_item_id, database: LvDatabase, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Link hinzufügen")
        self.selected_link_id = None
        self.database = database
        self.base_item_id = base_item_id

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Label
        label = QLabel(f"Position verknüpfen mit Basis Position: {self.database.get_category_of_index(self.base_item_id)} -> {self.database.get_position_of_index(self.base_item_id)}")
        layout.addWidget(label)

        # ComboBox
        self.combo_box = QComboBox()
        layout.addWidget(self.combo_box)
        self.fill_combobox()

        # Buttons
        button_layout = QHBoxLayout()
        btn_add = QPushButton("Hinzufügen")
        btn_cancel = QPushButton("Abbrechen")
        button_layout.addWidget(btn_add)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)

        # Connect buttons
        btn_add.clicked.connect(self.handle_add)
        btn_cancel.clicked.connect(self.reject)

    def fill_combobox(self):
        texts_array = self.database.get_all_non_base_positions_as_text()
        similarities = self.database.compare_all_to_single_base(self.base_item_id).flatten().tolist()

        combo_items = list(zip(similarities, texts_array, self.database.get_non_base_ui().index))
        combo_items.sort(key=lambda x: x[0], reverse=True)

        for sim, text, idx in combo_items:
            self.combo_box.addItem(f"({sim * 100:.1f} %) {text}", userData=idx)

    def handle_add(self):
        selected_id = self.combo_box.currentData()
        if selected_id != -1:
            self.selected_link_id = selected_id
        self.accept()
