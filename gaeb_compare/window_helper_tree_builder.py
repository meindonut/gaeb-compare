from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor
from PySide6.QtCore import Qt
import pandas as pd
from database import LvDatabase

# globals
color_tree_yellow_changed = QColor(200, 150, 0, 75)
color_tree_red_missing = QColor(255, 0, 0, 75)
color_tree_grey_identical = QColor(0, 0, 0, 25)

def build_three_level_tree_entry(tree_model: QStandardItemModel, three_str: list, data = None):
    if three_str.__len__() != 3:
        return
    
    name_lvl1, name_lvl2, name_lvl3 = three_str

    # Add level1 if not already in there
    item_lvl1 = None  # Default value
    for i in range(tree_model.rowCount()):
        item = tree_model.item(i)
        if item.text() == name_lvl1:
            item_lvl1 = item
            break  # Exit loop once a match is found

    if not item_lvl1:
        item_lvl1 = QStandardItem(name_lvl1)
        tree_model.appendRow(item_lvl1)

    # find level 2 name
    item_lvl2 = None  # Default value
    for i in range(item_lvl1.rowCount()):
        child = item_lvl1.child(i)
        if child.text() == name_lvl2:
            item_lvl2 = child
            break  # Exit loop once a match is found

    # add level 2 name if not found
    if not item_lvl2:
        item_lvl2 = QStandardItem(name_lvl2)
        item_lvl1.appendRow(item_lvl2)

    
    item_lvl3 = QStandardItem(name_lvl3)
    item_lvl3.setData(data, Qt.UserRole)         # Store data
    return [item_lvl1, item_lvl2, item_lvl3]

def build_simple_tree(tree_model: QStandardItemModel, lv_df: pd.DataFrame):
    #fill with data
    for idx, row in lv_df.iterrows():
        # Extract values
        three_str = [row["Gewerk"], row["Untergewerk"], row["Kurztext"]]

        three_items = build_three_level_tree_entry(tree_model, three_str, idx)
        three_items[1].appendRow(three_items[2])


def build_link_tree(tree_model: QStandardItemModel, lv_db: LvDatabase):       # populate_tree subfunction
    # Retrieve base items from the database    
    df_base = lv_db.get_base_ui()

    #fill with data
    for idx, row in df_base.iterrows():
        three_str = [row["Gewerk"], row["Untergewerk"], row["Kurztext"]]

        three_items = build_three_level_tree_entry(tree_model, three_str, idx)

        # build with extra links and columns
        kurztext_link_itemlist = [three_items[2]]
        columns_gewerke = LvDatabase.get_unique_gewerke(lv_db.get_non_base_ui())

        link_ids = lv_db.get_base_links_of_index(idx)
        similarities = lv_db.get_base_similiarities_of_index(idx)
        similarities_gewerke = lv_db.get_gewerk_of_index(link_ids)

        gewerk_stati = [""] * columns_gewerke.__len__()
        gewerk_last_links = [None] * columns_gewerke.__len__()

        # inteprete similarities to symbol and match to gewerke
        if similarities_gewerke is not None:
            for link_id, similarity, similarity_gewerk in zip(link_ids, similarities, similarities_gewerke):
                # find right column
                idx_sim = columns_gewerke.index(similarity_gewerk)
                if float(similarity) >= 0.99999:  # calculation is a bit unprecise somewhere, similarity sometimes single array
                    gewerk_stati[idx_sim] += "= "
                else:
                    gewerk_stati[idx_sim] += "~ "

                gewerk_last_links[idx_sim] = link_id
        gewerk_stati = ["- " if x == "" else x for x in gewerk_stati] # replace empty strings with '-'

        # Add additional columns for each gewerk
        for column, status, gewerk_last_link in zip(columns_gewerke, gewerk_stati, gewerk_last_links):
        
            link_item = QStandardItem(status)
            link_item.setData(idx, Qt.UserRole)
            link_item.setData(gewerk_last_link, Qt.UserRole + 1)

            # Set background color based on status -> order unimportant to important
            if "= " in status:
                link_item.setBackground(color_tree_grey_identical)
            if "~ " in status:
                link_item.setBackground(color_tree_yellow_changed)
            if "-" in status:
                link_item.setBackground(color_tree_red_missing)

            kurztext_link_itemlist.append(link_item)

        three_items[1].appendRow(kurztext_link_itemlist)