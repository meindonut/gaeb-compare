from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QLabel, QTreeView
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel

from database import LvDatabase # fore type hinting

from window_helper_tree_builder import build_simple_tree





class SearchWindowDatabase(QDialog):
    def __init__(self, parent, lv_database: LvDatabase):
        super().__init__(parent)
        self.search_dialog = QDialog(self)
        self.lv_db = lv_database

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        # UI
        # 'Treffer' not implemented yet

        #####################################
        ##  Datenbank Suche                ##
        #####################################
        #    ___________________________    #
        #   |   Position      | Treffer |   #
        #   |---------------------------|   #
        #   |   - Gewerk      |         |   #
        #   |    - Untergewerk|         |   #
        #   |     - Position 1|    2    |   #
        #   |     - Position 2|    1    |   #
        #   |_________________|_________|   #
        #                                   #
        #   Suche nach: [___________]       #
        #   [Suchen]          [Abbrechen]   #
        #####################################


        self.search_dialog.setWindowTitle("Datenbank Suche")
        
        layout = QVBoxLayout()
        # tree
        self.tree = QTreeView()
        layout.addWidget(self.tree)
        self.tree_model = QStandardItemModel()
        self.tree.setModel(self.tree_model)
        self.tree.setEditTriggers(QTreeView.NoEditTriggers)  # Make items non-editable

        # search field
        search_layout = QHBoxLayout()
        label = QLabel("Suche nach:")
        search_layout.addWidget(label)
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # buttons
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Suchen")
        self.cancel_button = QPushButton("Abrechen")
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.search_dialog.setLayout(layout)

        self.search_dialog.show()
        print("search db window: opened")

    def setup_connections(self):
        self.search_dialog.destroyed.connect(self.clear_search_dialog_reference)
        self.search_dialog.rejected.connect(self.clear_search_dialog_reference)
        self.search_button.clicked.connect(self.perform_search)
        self.cancel_button.clicked.connect(self.search_dialog.reject)
        self.tree.clicked.connect(self.on_tree_item_clicked)

    def clear_search_dialog_reference(self):
        self.parent().search_database_dialog = None # needs to match parent var name

    def perform_search(self):
        term = self.search_input.text()
        print(f"search db window: search for '{term}'")
        filtered_df = self.lv_db.filter_with_langtext(term)
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(["Suchtreffer:"])
        build_simple_tree(self.tree_model, filtered_df)
        self.tree.expandAll()

    def on_tree_item_clicked(self, index):
        item = self.tree_model.itemFromIndex(index)
        item_id = item.data(Qt.UserRole)  # Retrieve base DataFrame index (ID)
        print(f"search db window: clicked on  item ID '{item_id}'")
        
        if self.lv_db.id_is_base(item_id):
            self.parent().view_in_textedits(item_id, None)
        else:
            base_id = self.lv_db.get_link_of_index(item_id)
            self.parent().view_in_textedits(base_id, item_id)