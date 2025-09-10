import pandas as pd
import numpy as np
import os
from file_manager import FileManager, read_files, read_file, keep_highest_order_subfolder
from window_helper_dialogs import show_error_message

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import difflib

def find_most_similar(target, candidates):
    best_match = None
    best_index = -1
    highest_similarity = 0

    for i, candidate in enumerate(candidates):
        similarity = difflib.SequenceMatcher(None, target, candidate).ratio()
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = candidate
            best_index = i

    return best_index, best_match, highest_similarity

def cosine_comparison_single(text1: str, text2: str) -> float:
    # Wrap single strings in lists to match expected input format
    contents0 = [text1]
    contents1 = [text2]

    # Use the original function
    return cosine_comparison(contents0, contents1)[0, 0]  # Extract single similarity score

def cosine_comparison(contents0: list, contents1: list):
    assert not (None in contents0 or None in contents1) # None contents will result in error of comparison
    # Combine all text to fit the vectorizer correctly
    combined_files_content = contents0 + contents1

    # Fit the vectorizer on the combined content
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(combined_files_content)

    # Split the TF-IDF matrix back into base and comparison parts
    c0_tfidf_matrix = tfidf_matrix[:len(contents0)]
    c1_tfidf_matrix = tfidf_matrix[len(contents0):]

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(c0_tfidf_matrix, c1_tfidf_matrix)

    return similarity_matrix

class LvDatabase:

    @staticmethod
    def combine_columns_as_list(df: pd.DataFrame, *col_names):
        if df.empty:
            return []
        
        # Filter only existing columns
        existing_cols = [col for col in col_names if col in df.columns]
        
        if not existing_cols:
            return []

        # Convert each existing column to string and combine with ' -> '
        combined_series = df[existing_cols].astype(str).agg(" -> ".join, axis=1)
        
        return combined_series.tolist()
    
    @staticmethod
    def string_to_int_list(x: str):
        if isinstance(x, str) and x:  # Ensure x is a non-empty string
            if x.lower() == 'nan' or x.strip() == '':
                return []
            else:
                return list(map(int, x.split('; ')))  # Split by ", " and convert to integers
        else:
            return []  # Return an empty list if x is not a valid string
        
    @staticmethod
    def string_to_float_list(x: str):
        if isinstance(x, str) and x:  # Ensure x is a non-empty string
            if x.lower() == 'nan' or x.strip() == '':
                return []
            else:
                try:
                    return list(map(float, x.split('; ')))  # Split by ", " and convert to floats
                except ValueError:
                    return []  # Return empty list if conversion fails
        else:
            return []  # Return an empty list if x is not a valid string
        
    
    @staticmethod
    def get_unique_gewerke(lv_df: pd.DataFrame) -> list:
        return lv_df['Gewerk'].unique().tolist()

    def __init__(self, project_path: str, file_manager: FileManager):
        self._df = pd.DataFrame()
        self._df_abbreviations = pd.DataFrame()
        self.db_path = project_path + "\\" + "database.xlsx"
        self.file_manager = file_manager
        self.header_excel = ['Projekt', 'OZ', 'Gewerk', 'Untergewerk', 'Kurztext', 'Qty', 'QU', 'TLK', 'Pfad', 'Basis', 'Link']
        self.header_intern = self.header_excel.copy().extend(['calc_links', 'calc_similarity','Langtext'])

    @property
    def df_ui(self):
        return self.replace_abbreviations(self._df)
        
    def exists(self):
        return os.path.exists(self.db_path) and os.path.isfile(self.db_path)
    
    def loaded(self):
        return not self._df.empty
    
    def replace_abbreviations(self, df: pd.DataFrame):
        if df.empty or self._df_abbreviations.empty:
            return df.copy()

        df_processed = df.copy()

        for _, abbr_row in self._df_abbreviations.iterrows():
            name = abbr_row["name"]
            path = abbr_row["path"]
            abbreviation = abbr_row["abbreviation"]

            if pd.isna(abbreviation) or str(abbreviation).strip() == "":
                continue

            mask = (df_processed["Gewerk"] == name) & (
                df_processed["Pfad"].astype(str).str.contains(str(path), na=False)
            )

            df_processed.loc[mask, "Gewerk"] = abbreviation

        return df_processed

    def load(self):
        # load abbreviations
        self._df_abbreviations = pd.read_excel(io=self.db_path, sheet_name="abbreviation", index_col=None)   
        # load database
        self._df = pd.read_excel(io=self.db_path, sheet_name="database", index_col=0)
        # filter replace abbreviations
        # self.replace_abbreviations()
        print("database: load")

    def refresh_calculated_values(self):
        self.load_reverse_links()
        self.load_similiarities()
        self.load_textfiles()
        print("database: refreshed")

    def save(self):
        if not self.loaded():
            return
        try:
            with pd.ExcelWriter(self.db_path) as writer:
                self._df.to_excel(writer, sheet_name="database", columns=self.header_excel, index=True) 
                self._df_abbreviations.to_excel(writer, sheet_name="abbreviation", index=False)
        except PermissionError:
            print("Error: Permission denied to open the file.")
            show_error_message("Die Datenbank konnte nicht gespeichert werden, da der Zugriff verweigert wurde.")

        print("database: saved")

    
    def load_reverse_links(self):
        column_name = 'calc_links'

        # check if calling function makes sense
        if self._get_base().__len__() == 0:
            return
        
        # prepare list of lists
        links_from_base = [[] for i in range(self._df.__len__())]

        # go through non base position sort links of non base into lists above
        for id, row in self._get_non_base().iterrows():
            linked_id = row["Link"]
            if not pd.isna(linked_id): # if not empty in excel
                linked_id_int = int(linked_id)
                assert self._df.loc[linked_id_int, "Basis"] # shall be base position (==True)
                links_from_base[linked_id_int].append(id)

        # Convert each NumPy array in links_from_base to a comma-separated string
        links_from_base_str = ['; '.join(map(str, linklist)) for linklist in links_from_base]

        # save into database
        self._df[column_name]= links_from_base_str

    def load_similiarities(self):
        column_name = 'calc_similarity'

        # check if calling function makes sense
        if self._get_base().__len__() == 0:
            return

        # prepare list of lists
        similarities = [[] for i in range(self._df.__len__())]
        
        # get info from base
        lv_files_content_base = self.get_lv_file_contents(self._get_base())

        for [id, links], base_content in zip(self.get_base_links().items(), lv_files_content_base):
            df_linked = self.get_rows_of_index(links)
            lv_file_content = self.get_lv_file_contents(df_linked)
            if lv_file_content:
                sm = cosine_comparison(lv_file_content, [base_content])
                similarities[id] = sm.flatten()

        # Convert each NumPy array in links_from_base to a comma-separated string
        similarities_str = ['; '.join(map(str, linklist)) for linklist in similarities]

        # save into database
        self._df[column_name] = similarities_str

    def load_textfiles(self):
        column_name = 'Langtext'
        long_texts = []
        for rowidx, _ in self._df.iterrows():
            rel_path = self.get_path_of_index(rowidx)
            text = self.file_manager.load_text_file(rel_path)
            long_texts.append(text)

        self._df[column_name] = long_texts

    def prepare_for_database(self, lv_df: pd.DataFrame, paths: list, is_base_lv = False):
        lv_df_s = lv_df[['Projekt', 'OZ', 'Gewerk', 'Untergewerk', 'Kurztext', 'Qty', 'QU', 'TLK']]
        lv_df_s['Pfad'] = self.file_manager.get_rel_paths_of(paths)  # <- should be changed to substract project path
        lv_df_s['Basis'] = is_base_lv
        lv_df_s['Link'] = None
        lv_df_s.sort_values(by=['Gewerk'])
        lv_df_s = lv_df_s.reset_index(drop=True)

        return lv_df_s


    def add_lv_df(self, df_new: pd.DataFrame):
        # add to database
        self._df = pd.concat([self._df, df_new], ignore_index=True)

        # add abbreviations
        df_new['Pfad'] = df_new['Pfad'].apply(keep_highest_order_subfolder)
        df_filtered = df_new[['Gewerk','Pfad']].drop_duplicates()

        for _, row in df_filtered.iterrows():
            self.add_abbreviation(row['Gewerk'],row['Pfad'], "")

        print("database: lv added")
        # refresh database
        self.refresh_calculated_values()

    def add_abbreviation(self, long_name: str, path :str, abbreviation = ""):
        df_add = pd.DataFrame({"name": [long_name], "path": [path], "abbreviation": [abbreviation]})
        self._df_abbreviations =  pd.concat([self._df_abbreviations, df_add])
        self._df_abbreviations.reset_index()

    def set_abbreviation(self, long_name: str, path :str, abbreviation: str):
        pass

    def get_base_ui(self):
        if not self._df.empty:
            return self.df_ui[self._df['Basis'] == True]
        else:
            return pd.DataFrame()
        
    def _get_base(self):
        if not self._df.empty:
            return self._df[self._df['Basis'] == True]
        else:
            return pd.DataFrame()
    
    def get_base_links(self) -> pd.Series:
        filtered_df = self._get_base()
        if filtered_df.empty:
            return pd.Series()
        return filtered_df['calc_links'].apply(LvDatabase.string_to_int_list)
    
    def get_base_links_of_index(self, index: int):
        filtered_df = self._get_base()
        if filtered_df.empty:
            return []
        return LvDatabase.string_to_int_list(filtered_df.loc[index, 'calc_links'])
    
    def get_base_similiarities(self) -> pd.Series:
        filtered_df = self._get_base()
        if filtered_df.empty:
            return pd.Series()
        return filtered_df['calc_similarity'].apply(LvDatabase.string_to_float_list)
    
    def get_base_similiarities_of_index(self, index: int):
        filtered_df = self._get_base()
        if filtered_df.empty:
            return []
        return LvDatabase.string_to_float_list(filtered_df.loc[index, 'calc_similarity'])

    def _get_non_base(self):
        return self._df[self._df['Basis'] == False]

    def get_non_base_ui(self):
        return self.df_ui[self._df['Basis'] == False]

    def get_classification(self):
        filtered_df = self.get_base_ui()
        if filtered_df.empty:
            return np.empty(0)
        return filtered_df['Untergewerk'].unique()
    
    def find_linked_position_of_id(self, id: int):
        index_value = self._df[self._df['Link'] == id].index
        return index_value
         
    def find_linked_rows_of_id(self, id: int):
        index = self.find_linked_position_of_id(id)
        return self.get_rows_of_index(index)

    def get_positions_of_classification(self, classification: str):
        classes = self.get_classification()
        if classification in classes:
            base_df = self.get_base_ui()
            filtered_df = base_df[base_df['Untergewerk'] == classification]
            return filtered_df['Kurztext'].values[:]
        else:
            return None

    def get_all_base_positions_as_text(self):
        filtered_df = self.get_base_ui()
        if filtered_df.empty:
            return ""
        return LvDatabase.combine_columns_as_list(filtered_df,"Untergewerk", "Kurztext")
    
    def get_all_non_base_positions_as_text(self):
        filtered_df = self._get_non_base()
        if filtered_df.empty:
            return ""
        return LvDatabase.combine_columns_as_list(filtered_df,"Gewerk", "Untergewerk", "Kurztext")
        
    def set_to_base(self, index: int):
        self._df.loc[index, "Basis"] = True
        self._df.loc[index, "Link"] = None

        self.refresh_calculated_values()

    def set_to_not_base(self, index: int):
        self._df.loc[index, "Basis"] = False

    def set_link(self, non_base_index: int, id_of_base: int):
        # check if link is for non-base
        if self._df.loc[non_base_index, "Basis"]:
            print("Warning: Cannot set link for base positions")
            return
        self._df.loc[non_base_index, "Link"] = id_of_base
        self.refresh_calculated_values()

    def find_matching_tlk_indexes_of_base(self, lv_df_imported: pd.DataFrame) -> list[pd.Index]:
        index_value_list = []
        base_df = self._get_base()
        if base_df.empty:
            return [pd.Index([])] * lv_df_imported.__len__()
        
        for row_idx, row in lv_df_imported.iterrows():
            tlk = row["TLK"]
            if tlk == '': # dont search if empty string
                index_value = pd.Index([])
            else:
                index_value = base_df[base_df['TLK'] == tlk].index
                if index_value.size > 1: # not well defined
                    print(f"TLK Matcher: TLK {tlk} not uniquely defined") 
                    index_value = pd.Index([]) # -> set empty
            index_value_list.append(index_value)

        return index_value_list
    
    def _get_value_of_index(self, index: int, column_name: str):
        if column_name in self.df_ui.columns:
            cat_df = self.df_ui.loc[index, column_name]
            if type(cat_df) == str:
                return cat_df
            if cat_df.empty:
                return None
            else:
                return cat_df.values[:]
        else:
            return None
        
    def get_rows_of_index(self, id: int):
        return self.df_ui.loc[id]
    
    def get_gewerk_of_index(self, index: int):
        return self._get_value_of_index(index, 'Gewerk')
    
    def get_category_of_index(self, index: int):
        return self._get_value_of_index(index, 'Untergewerk')

    def get_position_of_index(self, index: int):
        return self._get_value_of_index(index, 'Kurztext')
    
    def get_path_of_index(self, index: int) -> str:
        return self._df.loc[index, 'Pfad']
    
    def id_is_base(self, index: int) -> bool:
        return self._df.loc[index, 'Basis']
    
    def get_link_of_index(self, index: int):
        return self._df.loc[index, 'Link']
    
    def get_long_text(self, index: int):
        return self._df.loc[index, 'Langtext']
    
    def get_similarity_factor(self, index_base, index_other):
        base_text = self.get_long_text(index_base)
        other_text = self.get_long_text(index_other)
        sm = cosine_comparison_single(base_text, other_text)
        return sm    

    def find_matching_tlk_categories_and_positions_of_base(self, lv_df_imported: pd.DataFrame):
        cats = []
        pos = []
        idxs = self.find_matching_tlk_indexes_of_base(lv_df_imported)
        for idx in idxs:
            cats.append(self.get_category_of_index(idx))
            pos.append(self.get_position_of_index(idx))
        return cats, pos, idxs
    
    def get_lv_file_contents(self, lv_df):
        rel_paths = lv_df["Pfad"].values[:]
        abs_paths = self.file_manager.get_abs_paths_of(rel_paths)
        lv_file_content = read_files(abs_paths)
        return lv_file_content
    
    def get_lv_file_content(self, lv_df):
        rel_path = lv_df["Pfad"]
        abs_path = self.file_manager.get_abs_path_of(rel_path)
        lv_file_content = read_file(abs_path)
        return lv_file_content


    def compare_to_base(self, new_lv_df):
        # get info from new lv
        lv_file_content = self.get_lv_file_contents(new_lv_df)

        # get info from base
        base_df = self._get_base()
        if base_df.empty:
            return np.zeros((new_lv_df.__len__(), 1))
        
        lv_file_content_base = self.get_lv_file_contents(base_df)

        sm = cosine_comparison(lv_file_content, lv_file_content_base)

        return sm
    
    def compare_all_to_single_base(self, base_item_id): # used for adding links
        content_non_base = self.get_lv_file_contents(self._get_non_base())
        df_base_single = self._get_base().loc[base_item_id]
        content_base_single = self.get_lv_file_content(df_base_single)
        sm = cosine_comparison(content_non_base, [content_base_single])
        return sm

    
    def find_similiar_categories_and_positions_of_base(self, lv_df_imported: pd.DataFrame):
        base_df = self._get_base()
        if base_df.empty:
            return [None] * lv_df_imported.__len__(), [None] * lv_df_imported.__len__(), [None] * lv_df_imported.__len__()
        
        sm = self.compare_to_base(lv_df_imported)

        matching_indices_matrix, similiarities = self.find_best_matching_indices(sm)
        base_idxs = self._get_base().index

        lv_df_imported.iterrows()
        
        matching_indices_db = []
        similiarities_new =[]
        for idxs, sim, [_, row] in zip(matching_indices_matrix, similiarities, lv_df_imported.iterrows()):
            idxs_db = base_idxs[idxs]
            if idxs_db.__len__() > 1: # choose the best index
                ug_imported = row["Untergewerk"]
                ug_base = self.get_category_of_index(idxs_db).tolist()
                loc_idx , _, _ = find_most_similar(ug_imported, ug_base)
                best_db_idx = idxs_db[loc_idx]
                best_sim = sim[loc_idx]

                matching_indices_db.append(pd.Index([best_db_idx]))
                similiarities_new.append(best_sim)
            else:
                matching_indices_db.append(idxs_db)
                similiarities_new.append(sim[0])
            

        threshold = 0.75
        idxs = []
        cats = []
        pos = []
        for idx, sim in zip(matching_indices_db, similiarities_new):
            if sim > threshold:
                idxs.append(idx) 
                cats.append(self.get_category_of_index(idx))
                pos.append(self.get_position_of_index(idx))
            else:
                idxs.append(None)
                cats.append(None)
                pos.append(None)

        # calculate right base file indices

        return cats, pos, idxs


    def isInitialized(self):
        if self._df is None:
            return False
        else:
            return True
        
    def find_best_matching_indices(self, sm: np.ndarray):
        # finds the index with the highest similarity
        matching_indices = []
        similiarities = []
        for i in range(sm.shape[0]):
            arr = sm[i,]
            max_val = np.max(arr)
            idxs = np.where(np.isclose(arr, max_val))[0]
            matching_indices.append(idxs)
            similiarities.append(sm[i,idxs])

        return matching_indices, similiarities
    
    def filter_with_langtext(self, search_term):
        found_rows = self._df['Langtext'].str.contains(search_term)
        return self.df_ui[found_rows]
    
    def get_ui_parameters(self, id):
        row = self.get_rows_of_index(id)
        row_filtered = row[['Kurztext', 'Qty', 'QU', 'TLK', 'OZ']]
        row_filtered = row_filtered.fillna('')
        return row_filtered.to_dict()