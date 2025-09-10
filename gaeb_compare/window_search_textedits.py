from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QLabel

from CustomPlainTextEdit import PlainTextEditWithLineNumbers # for type hinting


class SearchWindowTextedit(QDialog):
    def __init__(self, parent, text_edit: PlainTextEditWithLineNumbers):
        super().__init__(parent)
        self.search_dialog = QDialog(self)
        self.text_edit = text_edit

        self.setup_ui()
        self.setup_connections()

        self.last_search_term = ""
        self.last_search_cursor = None
        self.search_matches = []
        self.current_match_index = -1

        print("search text edit window: opened")

    def setup_ui(self):
        # UI

        #####################################
        ##  Suche                      [X] ##
        #####################################
        #   Suche nach: [___________]       #
        #   Treffer: 1 von 8                #
        #   [Suchen] [Weiter] [Abbrechen]   #
        #####################################

        self.search_dialog.setWindowTitle("Suche")
        
        layout = QVBoxLayout()
        # search
        search_layout = QHBoxLayout()
        label = QLabel("Suche nach:")
        search_layout.addWidget(label)
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # results
        self.search_status_label = QLabel("Keine Treffer")
        layout.addWidget(self.search_status_label)

        # buttons
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Suchen")
        self.next_button = QPushButton("Weiter")
        self.cancel_button = QPushButton("Abrechen")
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # set and show
        self.search_dialog.setLayout(layout)
        self.search_dialog.show()

    def setup_connections(self):
        self.search_dialog.destroyed.connect(self.clear_search_dialog_reference)
        self.search_dialog.rejected.connect(self.clear_search_dialog_reference)
        self.search_button.clicked.connect(self.perform_search)
        self.next_button.clicked.connect(self.jump_to_next_match)
        self.cancel_button.clicked.connect(self.search_dialog.reject)

    def perform_search(self):
        term = self.search_input.text()
        print(f"search text edit window: '{term}'")
        self.last_search_term = term
        self.find_all_matches(term)
           

    def set_text_edit(self, text_edit: PlainTextEditWithLineNumbers):
        self.text_edit = text_edit

    def clear_search_dialog_reference(self):
        self.parent().search_textedit_dialog = None # needs to match parent var name

    def find_all_matches(self, term: str):
        # reset
        self.search_matches.clear()
        self.current_match_index = -1

        if not self.text_edit:
            print("search text edit window: not possible without focus")
            return

        doc = self.text_edit.document()
        cursor = doc.find(term)
        while not cursor.isNull():
            self.search_matches.append(cursor)
            cursor = doc.find(term, cursor)

        self.update_search_status()
        self.jump_to_next_match()

    def jump_to_next_match(self):
        if not self.search_matches:
            return

        self.current_match_index = (self.current_match_index + 1) % len(self.search_matches)
        cursor = self.search_matches[self.current_match_index]

        # Set focus and move cursor
        self.text_edit.setFocus()
        self.text_edit.setTextCursor(cursor)

        self.update_search_status()

    def update_search_status(self):
        total = len(self.search_matches)
        index = self.current_match_index + 1 if self.current_match_index >= 0 else 0
        if total == 0:
            self.search_status_label.setText("Keine Treffer")
        else:
            self.search_status_label.setText(f"Treffer: {index} von {total}")
