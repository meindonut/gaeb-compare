from PySide6.QtWidgets import QAbstractItemView, QComboBox, QDialog, QVBoxLayout, QTableView, QPushButton, QHBoxLayout, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

import pandas as pd # only for type hinting
import numpy as np

from database import LvDatabase


class LvImportWindow(QDialog):
    def __init__(self, project_path: str, lv_df: pd.DataFrame, database: LvDatabase, parent=None):
        super().__init__(parent)
        self.table_dialog = None
        self.project_path = project_path
        self.lv_df = lv_df
        self.table_view = None
        self.lv_database = database
        self.new_links = []
        self.new_is_base = [False] * lv_df.shape[0]   # create list of false and change later to true if position shall be added to base
        self.cb_action_str = ["-> neue Basisposition", "-> Verknüpfen (TLK)", "-> Verknüpfen (Ähnlichkeit)", "-> keine Aktion"]
        self.cb_link_std = "(0.0 %) -"

        self.setup_ui()

    def setup_ui(self):

        # -------- setup window ------------

        # Create a new dialog to display the table
        self.table_dialog = QDialog(self)
        self.table_dialog.setWindowTitle("LV Import")
        self.table_dialog.resize(1200, 900)
        self.table_dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # Set up the layout for the dialog
        main_layout = QVBoxLayout(self.table_dialog)

        # Create a QTableView
        self.table_view = QTableView()
        main_layout.addWidget(self.table_view)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Add "Importieren" button
        import_button = QPushButton("Importieren")
        button_layout.addWidget(import_button)

        # Add button
        no_action_button = QPushButton("Neu -> keine Aktion")
        button_layout.addWidget(no_action_button)

        # Add button
        new_button = QPushButton("keine Aktion -> Neu")
        button_layout.addWidget(new_button)

        # Add "Abbrechen" button
        cancel_button = QPushButton("Abbrechen")
        button_layout.addWidget(cancel_button)

        # Connect button signals
        cancel_button.clicked.connect(self.cancelButtonClicked)  # Close dialog on cancel
        import_button.clicked.connect(self.importButtonClicked)  # Handle import
        no_action_button.clicked.connect(self.noActionButtonClicked)
        new_button.clicked.connect(self.newButtonClicked)

        # Align buttons to the bottom-right
        button_layout.setAlignment(Qt.AlignRight)
        main_layout.addLayout(button_layout)

        # -------- load data ------------

        lv_short_df = self.lv_df[["Gewerk", "Untergewerk", "Kurztext"]]
        # find category and position with tlk
        _, pos_with_tlk, idx_db_tlk = self.lv_database.find_matching_tlk_categories_and_positions_of_base(self.lv_df)
        _, pos_with_similiarity, idx_db_sim = self.lv_database.find_similiar_categories_and_positions_of_base(self.lv_df)
        is_first_import = not self.lv_database.exists()

        # -------- set up model and table view ------------

        # Set up the model for the QTableView
        model = QStandardItemModel()
        model.setRowCount(len(lv_short_df))
        model.setColumnCount(5)
        model.setHorizontalHeaderLabels(
            list(lv_short_df.columns) + ["Aktion", "Link"]
        )
        self.table_view.setModel(model)

        # Set up the QTableView
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)

        # Switch to Interactive mode after initial stretching
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_view.verticalHeader().setVisible(False)

        # Make the dialog scrollable
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # -------- precalculations for link ------------
        print("import windows: precalculations")

        base_ids = self.lv_database.get_base_ui().index
        base_ids = base_ids.append(pd.Index([-1]))

        # load texts
        texts_array = np.array(self.lv_database.get_all_base_positions_as_text())
        texts_array = np.append(texts_array,"-")
        # get similarites
        sm = self.lv_database.compare_to_base(self.lv_df).transpose()
        # add some zeros at the bottom
        sm = np.vstack((sm, np.full((1, sm.shape[1]), 0)))

        # Convert percentages to formatted strings
        percent_matrix = np.char.mod("(%.1f %%)", sm * 100)
        # Broadcast string_list and concatenate
        cb_link_str = percent_matrix + ' ' + texts_array[:, np.newaxis]

        # -------- fill table with data ------------
        print("import windows: fill table model")

        # Create the model with size of dataframe and set settings
        for row_idx, row in lv_short_df.iterrows():

            # preparation of size and set settings
            for column_idx, value in enumerate(row):
                item = QStandardItem(str(value))
                item.setEditable(False)  # Data columns are read-only
                model.setItem(row_idx, column_idx, item)
            for col_offset in range(2):
                combobox_item = QStandardItem("Default")
                combobox_item.setEditable(True)
                model.setItem(row_idx, len(lv_short_df.columns) + col_offset, combobox_item)

            
            # create cbs with options
            cb_action = QComboBox()
            cb_action.addItems(self.cb_action_str)

            cb_link = QComboBox()    
            similarities = sm[:, row_idx]   # Get similarity values for the current row   
            similarities[-1] = 2.0  # change the similiarity of the '-' value to sort it to the top           
            items = list(zip(similarities, cb_link_str[:, row_idx], base_ids))   # Pair (similarity, text, base_ids)
            sorted_items = sorted(items, key=lambda x: x[0], reverse=True)  # Sort by similarity descending
            for _, text, base_id in sorted_items:   # Add selections to combobox
                cb_link.addItem(text, userData=base_id)

            # set corresponding link
            if pos_with_tlk[row_idx]: # is in TLK
                cb_action.setCurrentText(self.cb_action_str[1]) # Verknüpfen TLK

                idx_db = idx_db_tlk[row_idx].values.astype(int)[0]
                idx_combo = base_ids.get_loc(idx_db)
                cb_link.setCurrentText(cb_link_str[idx_combo, row_idx])

            elif pos_with_similiarity[row_idx]: # found similiar
                cb_action.setCurrentText(self.cb_action_str[2]) # Verknüpfen

                idx_db = idx_db_sim[row_idx].values.astype(int)[0]
                idx_combo = base_ids.get_loc(idx_db)
                cb_link.setCurrentText(cb_link_str[idx_combo, row_idx])
            else:
                if is_first_import:
                    cb_action.setCurrentText(self.cb_action_str[0]) # Neu
                    self.new_is_base[row_idx] = True
                else:
                    cb_action.setCurrentText(self.cb_action_str[3]) # keine Aktion

                cb_link.setCurrentText(self.cb_link_std)
                idx_db = None

            # connect actions and insert combos
            cb_action.currentIndexChanged.connect(lambda idx, row=row_idx: self.on_action_changed(row))
            cb_link.currentIndexChanged.connect(lambda idx, row=row_idx: self.on_link_changed(row))
            self.table_view.setIndexWidget(model.index(row_idx, 3), cb_action)
            self.table_view.setIndexWidget(model.index(row_idx, 4), cb_link)

            self.new_links.append(idx_db)
            
        # Show the dialog
        print("import window: opened")
        self.table_dialog.exec()
        print("import window: closed")


    def on_action_changed(self, row_idx):
        # get comboBoxes
        cb_action = self.table_view.indexWidget(self.table_view.model().index(row_idx, 3))
        cb_link = self.table_view.indexWidget(self.table_view.model().index(row_idx, 4))

        if cb_action and cb_link:
            # get input
            selected_action = cb_action.currentText()
            print(f"import window: change action to '{selected_action}'")

            if selected_action == self.cb_action_str[3]: # keine Aktion
                cb_link.setCurrentText(self.cb_link_std)
                self.new_is_base[row_idx] = False
                self.new_links[row_idx] = None
            elif selected_action == self.cb_action_str[0]: # Neu
                cb_link.setCurrentText(self.cb_link_std)
                self.new_is_base[row_idx] = True
                self.new_links[row_idx] = None
            else: # Verknüpfen
                pass # possible to add a change of the linked item here

    
    def on_link_changed(self, row_idx):
        #get comboBoxes
        cb_link = self.table_view.indexWidget(self.table_view.model().index(row_idx, 4))
        cb_action = self.table_view.indexWidget(self.table_view.model().index(row_idx, 3))
        
        if cb_link:
            # get input
            base_id = cb_link.itemData(cb_link.currentIndex()) # -1 when '-' selected
            print(f"import window: change link to base id '{base_id}'")

            if base_id != -1: # user want to link
                cb_action.setCurrentText(self.cb_action_str[2]) # Verknüpfen
                self.new_is_base[row_idx] = False
                self.new_links[row_idx] = base_id
            else: # user want to unlink
                cb_action.setCurrentText(self.cb_action_str[3]) # keine Aktion
                self.new_is_base[row_idx] = False
                self.new_links[row_idx] = None


    def cancelButtonClicked(self):
        self.table_dialog.reject()
        self.table_dialog.close()
        self.reject()
        self.close()


    def importButtonClicked(self):
        self.lv_df["Link"] = self.new_links
        self.lv_df["Basis"] = self.new_is_base
        self.lv_database.add_lv_df(self.lv_df)
        self.lv_database.save()

        self.table_dialog.accept()
        self.table_dialog.close()
        self.accept()
        self.close()


    def noActionButtonClicked(self):
        print(f"import window: change all '{self.cb_action_str[0]}' to '{self.cb_action_str[3]}' ")
        col_idx = 3
        for row_idx in range(self.table_view.model().rowCount()):
            cb_action = self.table_view.indexWidget(self.table_view.model().index(row_idx, col_idx))
            if cb_action and cb_action.currentText() == self.cb_action_str[0]:  # "-> Neu"
                cb_action.setCurrentText(self.cb_action_str[3])  # "-> keine Aktion"
                self.on_action_changed(row_idx) # trigger as if user clicked


    def newButtonClicked(self):
        print(f"import window: change all '{self.cb_action_str[3]}' to '{self.cb_action_str[0]}' ")
        col_idx = 3
        for row_idx in range(self.table_view.model().rowCount()):
            cb_action = self.table_view.indexWidget(self.table_view.model().index(row_idx, col_idx))
            if cb_action and cb_action.currentText() == self.cb_action_str[3]:  # "-> keine Aktion"
                cb_action.setCurrentText(self.cb_action_str[0])  # "-> Neu"
                self.on_action_changed(row_idx) # trigger as if user clicked
