from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QAbstractItemView,
    QDialog,
    QTreeView,
    QMenu,
    QHeaderView,
    QLabel,
)

from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QColor,
)

from CustomPlainTextEdit import PlainTextEditWithLineNumbers

from ui_project_window import Ui_MainWindow

# windows
from window_properties import PropertiesWindow
from window_import_lv import LvImportWindow
from window_add_link import AddLinkDialog
from window_search_textedits import SearchWindowTextedit
from window_search_database import SearchWindowDatabase
from window_helper_tree_builder import build_link_tree

# tools
from lv_handling import load_lv, save_lv
from file_manager import FileManager, get_file_name, write_file_abs_path
from database import LvDatabase
from diff_display import fill_text_google, fill_text_difflib, google_diff, difflib_diff


color_tree_yellow_changed = QColor(200, 150, 0, 75)

class ProjectWindow(QMainWindow):
    def __init__(self, file_manager: FileManager, database: LvDatabase):
        super(ProjectWindow, self).__init__()
        
        self.fm = file_manager
        self.lv_db = database
    
        self.loaded_left_base_id = None

        self.table_sorting_col = None
        self.table_sorting_ord = None
        self.tree_headers = []

        self.diff_method = "auto"

        # search
        self.search_textedit_dialog = None
        self.last_textedit_focused = None
        self.search_database_dialog = None

        self.load_ui()

        self.sortName()
        self.sortDsc()
        self.setup_connections()
        print("project window: opened")

    def load_ui(self):

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ------ further changes in the ui -> easier in code than in ui editor ------

        # Integrate TreeView of Database
        self.tree_view = QTreeView()
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Basis"])
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)  # Make items non-editable
        self.ui.verticalLayout_3.replaceWidget(self.ui.treeView, self.tree_view)
        self.ui.treeView.deleteLater()
        self.populate_tree()

        # replace textedits with advanced line number version
        layout = self.ui.verticalLayout
        self.text_edit_left = PlainTextEditWithLineNumbers()
        layout.replaceWidget(self.ui.textEdit_left, self.text_edit_left)
        self.ui.textEdit_left.deleteLater()
        layout = self.ui.verticalLayout_2
        self.text_edit_right = PlainTextEditWithLineNumbers()
        layout.replaceWidget(self.ui.textEdit_right, self.text_edit_right)
        self.ui.textEdit_right.deleteLater()

        # sync scrolling
        self.text_edit_left.set_synced_editor(self.text_edit_right)
        self.text_edit_right.set_synced_editor(self.text_edit_left)

        # Set read-only mode
        self.text_edit_right.setReadOnly(True)

        # Initialize TableView model
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(["Name", "Ähnlichkeit"])
        self.ui.tableView.setModel(self.table_model)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.setSortingEnabled(True)

        # intitialize table views above textedits
        self.table_model_left = QStandardItemModel()
        self.ui.tableView_left.setModel(self.table_model_left)
        self.ui.tableView_left.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView_left.verticalHeader().setVisible(False)

        self.table_model_right = QStandardItemModel()
        self.ui.tableView_right.setModel(self.table_model_right)        
        self.ui.tableView_right.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView_right.verticalHeader().setVisible(False)


    def setup_connections(self):
        self.ui.actionExit.triggered.connect(self.close_application)  # menu exit
        self.ui.tableView.clicked.connect(self.on_table_view_clicked)  # table click
        self.ui.actionSynchron.toggled.connect(self.toggle_sync_scroll)  # scrolling
        self.ui.pushButton_save.clicked.connect(self.save_and_reload)  # saving under textedit

        self.ui.actionLvImport.triggered.connect(self.importLv)  # import lv

        self.ui.actionName.triggered.connect(self.sortName)  # sorting
        self.ui.actionSim.triggered.connect(self.sortSimi)  # sorting

        self.ui.actionAsc.triggered.connect(self.sortAsc)  # sorting
        self.ui.actionDsc.triggered.connect(self.sortDsc)  # sorting

        self.ui.actionDifflib_2.triggered.connect(self.use_difflib)  # differ
        self.ui.actionGoogle_2.triggered.connect(self.use_google)  # differ
        self.ui.actionAutomatisch.triggered.connect(self.use_auto)  # differ

        self.ui.actionSuchen.triggered.connect(self.search)
        self.ui.actionSuchen_Alle.triggered.connect(self.search_all)

        self.ui.actionProperties.triggered.connect(self.open_properties_window)
        self.tree_view.clicked.connect(self.on_tree_item_clicked)

        self.ui.pushButtonAdd.clicked.connect(self.on_add_link_clicked)
        self.ui.pushButtonDelete.clicked.connect(self.on_delete_link_clicked)

        self.ui.actionAlles_ausklappen.triggered.connect(self.expand_tree)

        # connection for saving last focused text edit
        self.text_edit_left.focusInEvent = self._make_focus_handler(self.text_edit_left)
        self.text_edit_right.focusInEvent = self._make_focus_handler(self.text_edit_right)

    def _make_focus_handler(self, text_edit: PlainTextEditWithLineNumbers):
        def handler(event):
            self.search_window_set_textedit(text_edit)
            self.last_textedit_focused = text_edit
            PlainTextEditWithLineNumbers.focusInEvent(text_edit, event)
        return handler
    
    @staticmethod
    def fill_table_model_with_dict(table_model:  QStandardItemModel, dict_table: dict, mark_values: list[bool] = None):
        table_model.removeRows(0, table_model.rowCount())
        if not mark_values:
            mark_values = [False] * dict_table.__len__()
        
        for [key, value], mark in zip(dict_table.items(), mark_values):
            key_item = QStandardItem(key)
            value_item = QStandardItem(value)
            if mark:
                value_item.setBackground(color_tree_yellow_changed)
            key_item.setEditable(False)
            value_item.setEditable(False)
            table_model.appendRow([key_item, value_item])

    @staticmethod
    def compare_dicts(dict1, dict2):
        """
        Compare two dictionaries and return a list of booleans with the length of dict2.
        Each boolean indicates whether the corresponding key-value pair in dict2
        exists in dict1 with the same value.
        """
        return [dict1.get(key) == value for key, value in dict2.items()]

    def on_delete_link_clicked(self):
        selected = self.ui.tableView.selectionModel().selectedRows()
        if selected:
            row_index = selected[0].row()
            index_db = self.table_model.item(row_index, 0).data(Qt.UserRole)
            print(f"project window: delete link for database entry {index_db}")
            self.lv_db.set_link(index_db,None)

            # refresh view
            self.populate_tree()
            self.populate_table_view(None)

    def on_add_link_clicked(self):
        selected_indexes = self.tree_view.selectedIndexes()
        if not selected_indexes:
            return

        selected_index = selected_indexes[0]
        base_item_id = self.tree_model.itemFromIndex(selected_index).data(Qt.UserRole)
        if base_item_id is None:
            return

        dialog = AddLinkDialog(base_item_id, self.lv_db, self)
        if dialog.exec() == QDialog.Accepted and dialog.selected_link_id is not None:
            self.lv_db.set_link(dialog.selected_link_id, base_item_id)
            print(f"project window: add link for database entry {dialog.selected_link_id} to base entry {base_item_id}")
            self.populate_tree()
            self.populate_table_view(None)

    def expand_tree(self):
        self.tree_view.expandAll()

    def check_database(self):   # populate_tree subfunction
        if not self.lv_db.exists():
            self.tree_model.setHorizontalHeaderLabels(["Datenbank existiert nicht."])
            return False
        elif not self.lv_db.loaded():
            self.tree_model.setHorizontalHeaderLabels(["Datenbank nicht geladen."])
            return False
        else:
            return True
        
    def setup_header(self, with_links: bool):     # populate_tree subfunction
   
        # set column names
        if not with_links:
            self.tree_headers = ["Basis"]
        else:
            columns_gewerke = LvDatabase.get_unique_gewerke(self.lv_db.get_non_base_ui())
            self.tree_headers = ["Basis"] + columns_gewerke

        self.tree_model.setHorizontalHeaderLabels(self.tree_headers)
        self.tree_model.setColumnCount(self.tree_headers.__len__())

        # Add right-click context menu for column visibility toggle only on the header
        header = self.tree_view.header()
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.show_column_menu)

        # Enable word wrapping in headers
        header.setSectionResizeMode(QHeaderView.Interactive)

    def populate_tree(self):
        self.tree_model.clear()
        if not self.check_database():
            return
        self.setup_header(with_links=True)
        build_link_tree(self.tree_model, self.lv_db)

    def show_column_menu(self, pos):
        # Show right-click menu to toggle column visibility only on the header.
        print("project window: right click on menu bar")
        menu = QMenu(self.tree_view)
        header = self.tree_view.header()

        for i, header_name in enumerate(self.tree_headers):
            action = menu.addAction(header_name.replace("\n", " "))
            action.setCheckable(True)
            action.setChecked(not self.tree_view.isColumnHidden(i))
            action.triggered.connect(
                lambda checked, col=i: self.tree_view.setColumnHidden(col, not checked)
            )

        menu.exec_(header.mapToGlobal(pos))

    def on_tree_item_clicked(self, index):
        item = self.tree_model.itemFromIndex(index)
        
        base_item_id = item.data(Qt.UserRole)  # Retrieve base DataFrame index (ID)
        linked_item_id = item.data(Qt.UserRole + 1) 
        self.view_in_textedits(base_item_id, linked_item_id)        

    def view_in_textedits(self, base_id, linked_id):
        print(f"Load base item ID: {base_id} and linked item ID {linked_id}")  # Debugging output
        self.loaded_left_base_id = base_id
        self.clear_text_edits()
        self.clear_tables()

        if base_id is None:    # no information
            self.update_label_text(self.ui.label_title_left, "Basis: keine Auswahl")
            self.populate_table_view(base_id) # base_item_id = None
            return

        else:                       # base information or more
            base_path = self.lv_db.get_path_of_index(base_id)
            base_abs_path = self.fm.get_abs_paths_of([base_path])[0]

            # load new base file
            self.load_text_file(base_abs_path, self.text_edit_left)
            self.update_label_text(self.ui.label_title_left, f"Basis: {self.lv_db.get_gewerk_of_index(base_id)}")
            self.populate_table_view(base_id)
            base_parameter = self.lv_db.get_ui_parameters(base_id)
            self.fill_table_model_with_dict(self.table_model_left, base_parameter)
            self.table_model_left.setHorizontalHeaderLabels(["Eigenschaft", "Wert"])

            if linked_id is None:  # no further information
                self.update_label_text(self.ui.label_title_right, "Vergleich: keine Auswahl")
                return
            else:                       # also information about linked item
                linked_path = self.lv_db.get_path_of_index(linked_id)
                linked_abs_path = self.fm.get_abs_paths_of([linked_path])[0]

                #load new linked file
                self.load_text_file(linked_abs_path, self.text_edit_right)
                self.update_label_text(self.ui.label_title_right, f"Vergleich: {self.lv_db.get_gewerk_of_index(linked_id)}")
                linked_parameter = self.lv_db.get_ui_parameters(linked_id)
                different_in_dict = self.compare_dicts(base_parameter, linked_parameter)
                mark = [not elem for elem in different_in_dict]
                self.fill_table_model_with_dict(self.table_model_right, linked_parameter, mark)
                self.table_model_right.setHorizontalHeaderLabels(["Eigenschaft", "Wert"])
                self.compare_texts()

    def load_data_to_right_of_index(self, index):
        rel_path = self.lv_db.get_path_of_index(index)
        abs_path = self.fm.get_abs_path_of(rel_path)
        self.load_text_file(abs_path, self.text_edit_right)
        self.update_label_text(self.ui.label_title_right, f"Vergleich: {self.lv_db.get_gewerk_of_index(index)}")

        self.compare_texts()

    def open_properties_window(self):
        # Fenster anzeigen
        dialog = PropertiesWindow(name_value="Beispielname", parent=self)
        if dialog.exec() == QDialog.Accepted:
            # OK gedrückt, Pfad auslesen
            print("Pfad:", dialog.get_path())
        else:
            print("Abbrechen gedrückt")

    def show_confirmation_dialog(self, text: str):
        # Erstelle eine QMessageBox
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Bestätigung")
        dialog.setText(text)
        dialog.setIcon(QMessageBox.Question)

        # Buttons hinzufügen
        yes_button = dialog.addButton("Ja", QMessageBox.YesRole)
        no_button = dialog.addButton("Nein", QMessageBox.NoRole)

        # Dialog anzeigen und Benutzeraktion abfragen
        dialog.exec()

        # Rückgabe basierend auf der Auswahl
        if dialog.clickedButton() == yes_button:
            return True
        elif dialog.clickedButton() == no_button:
            return False

    def importLv(self):
        lv_path_import = self.fm.get_path_ui("LV XML (*.X81 *.X82 *.X83 *.X84 *.X85 *.X86)")
        if not lv_path_import:
            return
        print(f"project window: start lv import of {lv_path_import}")
        
        export_path = self.fm.project_path + "\\" + get_file_name(lv_path_import, with_extension=False)

        lv_df_import = load_lv(lv_path_import)
        lv_paths_import = save_lv(lv_df_import, export_path)
        lv_db_import = self.lv_db.prepare_for_database(lv_df_import, lv_paths_import)

        importDialog = LvImportWindow(
            self.fm.project_path, lv_db_import, self.lv_db, self
        )

        # refresh ui
        self.populate_tree()
        self.populate_table_view(None)

    def sortName(self):
        self.table_sorting_col = 0
        self.ui.actionName.setChecked(True)  # only needed for init
        self.ui.actionSim.setChecked(False)
        self.ui.actionLinked.setChecked(False)

    def sortSimi(self):
        self.table_sorting_col = 1
        self.ui.actionSim.setChecked(True)  # only needed for init
        self.ui.actionName.setChecked(False)
        self.ui.actionLinked.setChecked(False)

    def sortAsc(self):
        self.table_sorting_ord = Qt.AscendingOrder
        self.ui.actionAsc.setChecked(True)  # only needed for init
        self.ui.actionDsc.setChecked(False)

    def sortDsc(self):
        self.table_sorting_ord = Qt.DescendingOrder
        self.ui.actionDsc.setChecked(True)  # only needed for init
        self.ui.actionAsc.setChecked(False)

    def use_auto(self):
        self.diff_method = "auto"
        self.ui.actionGoogle_2.setChecked(False)
        self.ui.actionDifflib_2.setChecked(False)
        self.compare_texts()

    def use_difflib(self):
        self.diff_method = "difflib"
        self.ui.actionGoogle_2.setChecked(False)
        self.ui.actionAutomatisch.setChecked(False)
        self.compare_texts()

    def use_google(self):
        self.diff_method = "google"
        self.ui.actionDifflib_2.setChecked(False)
        self.ui.actionAutomatisch.setChecked(False)
        self.compare_texts()

    def search(self):
        # Check if already open
        if not self.search_textedit_dialog:
            self.search_textedit_dialog = SearchWindowTextedit(self, self.last_textedit_focused)
        else:
            print("Search: Dialog already opened")
            self.search_textedit_dialog.raise_()
            self.search_textedit_dialog.activateWindow()
    
    def search_window_set_textedit(self, text_edit: PlainTextEditWithLineNumbers):
        if self.search_textedit_dialog:
            self.search_textedit_dialog.set_text_edit(text_edit)
        
    def search_all(self):
        # Check if already open
        if not self.search_database_dialog:
            self.search_database_dialog = SearchWindowDatabase(self, self.lv_db)
        else:
            print("Search: Dialog already opened")
            self.search_database_dialog.raise_()
            self.search_database_dialog.activateWindow()

    def save_and_reload(self):
        # Save the current text to the respective files
        if self.loaded_left_base_id:
            base_path = self.lv_db.get_path_of_index(self.loaded_left_base_id)
        
            write_file_abs_path(self.text_edit_left.toPlainText(), base_path, createDir=False)
            # Reload the files to trigger the comparison
            self.load_text_file(base_path, self.text_edit_left)  

    def toggle_sync_scroll(self, checked: bool):
        if checked:
            self.text_edit_left.set_synced_editor(self.text_edit_right)
            self.text_edit_right.set_synced_editor(self.text_edit_left)
        else:
            self.text_edit_left.set_synced_editor(None)
            self.text_edit_right.set_synced_editor(None)

    def populate_table_view(self, id_clicked):
        self.table_model.removeRows(0, self.table_model.rowCount())
        self.text_edit_right.clear()

        df_linked = self.lv_db.find_linked_rows_of_id(id_clicked)
        if df_linked.empty:
            return

        for index, row in df_linked.iterrows():
            name = row["Gewerk"] + " -> " + row["Untergewerk"] + " -> " + row["Kurztext"]

            similarity_factor = self.lv_db.get_similarity_factor(id_clicked, index)
            similarity = f"{similarity_factor * 100:.1f} %"
            name_item = QStandardItem(name)
            similarity_item = QStandardItem(similarity)
            name_item.setData(index, Qt.UserRole)  # Stores the Excel index in the first column item

            name_item.setEditable(False)
            similarity_item.setEditable(False)

            self.table_model.appendRow([name_item, similarity_item])

        self.ui.tableView.sortByColumn(self.table_sorting_col, self.table_sorting_ord)

    def on_table_view_clicked(self, index):
        row = index.row()
        index = self.table_model.item(row, 0).data(
            Qt.UserRole
        )  # invisible data store in first column
        self.load_data_to_right_of_index(index)

    def update_label_text(self, label: QLabel, full_text: str):
        label.setText(full_text)
        label.setToolTip(full_text)

    def load_text_file(self, file_path: str, text_edit_widget: PlainTextEditWithLineNumbers):
        with open(file_path, "r", encoding="utf-8") as file:  # Setze das encoding auf 'utf-8'
            file_content = file.read()
            text_edit_widget.setPlainText(file_content)

    def compare_texts(self):
        # check if text edits are not empty
        if self.text_edit_left.toPlainText() == "" or self.text_edit_right.toPlainText() == "":
            print("Comparer: no meaningfull comparison with empty text_edit possible")
            return

        left_text = self.text_edit_left.toPlainText()
        right_text = self.text_edit_right.toPlainText()

        self.clear_text_edits()

        # set differ
        auto_threshhold = 5000
        if self.diff_method == "auto":
            if left_text.__len__() > auto_threshhold:
                use_diff_method = "difflib"
            else:
                use_diff_method = "google"
        else:
            use_diff_method = self.diff_method

        # diff
        if use_diff_method == "difflib":
            diff = difflib_diff(left_text, right_text)
            fill_text_difflib(diff, self.text_edit_left, self.text_edit_right)
        elif use_diff_method == "google":
            diff = google_diff(left_text, right_text)
            fill_text_google(diff, self.text_edit_left, self.text_edit_right)
        else:
            print(f"differ {use_diff_method} not found")

        print(f"Comparer: use method {use_diff_method} for left text length of {left_text.__len__()}")

    def clear_text_edits(self):
        self.text_edit_left.clear()
        self.text_edit_right.clear()

    def clear_tables(self):
        self.table_model_left.clear()
        self.table_model_right.clear()

    def closeEvent(self, event):
        # save database before closing
        self.lv_db.save()
        QApplication.quit()

    def close_application(self):
        self.close()
