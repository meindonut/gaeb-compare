import os
import unicodedata
import re
from gaeb_parser import XmlGaebParser
from pathlib import Path
import pandas as pd

from file_manager import load_pickle, write_file_abs_path

pickle = load_pickle()

def slugify(value, allow_unicode=False) -> str:
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.

    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

    
def extractInteger(text: str) -> list:
    # extracts all integers from a text
    if type(text) == str and text != '':
        res = []
        for s in re.findall(r'\d+', text):
            res.append(int(s))
        return res
    else:
        return []


def startsWithNumber(text: str) -> bool:
    # checks if a text starts with a number
    if type(text) == str and text != '':
        return text[0].isdigit()
    else:
        return False


def textContainsStringTuple(text: str, stringTuple: tuple) -> bool:
    # checks a text if it contains any string of stringTuple
    if type(text) == str and text != '':
        if any(subStr in text for subStr in stringTuple):
            return True
        else:
            return False
    else:
        return False
    

def iTwoTextFormatter(text: str) -> str:
    # formats text imported from RIB iTwo nicely
    formattedText = ""
    text += "\n"
    
    listBulletPoints = ('-', ' -',' ·', '·') # identified bullet points get new lines
    listSingleLineIncludes = ('...', '(vom Bieter auszufüllen)', 'Angebotenes Fabrikat','Angebotener Typ','vom Bieter einzutragen') # identified passages get new lines
    
    # temporary variables for next iteration
    lineBefore = ' '
    putNewLineAfterBlock = False

    # first: split all lines apart
    lines = text.split('\n')

    # second: put them together rule based
    for line, nextLine in zip(lines, lines[1:]):
        # keep empty lines
        if line == '': 
            formattedText += '\n\n'

        # keep lists with bullet points
        elif (line.startswith(listBulletPoints) and nextLine.startswith(listBulletPoints)) or (line.startswith(listBulletPoints) and lineBefore.startswith(listBulletPoints)):
            formattedText += '\n' + line
            putNewLineAfterBlock = True

        # keep list with ':' inside
        elif (':' in line and ':' in nextLine) or (':' in line and ':' in lineBefore):
            formattedText += '\n' + line
            putNewLineAfterBlock = True

        # keep enumerations
        elif startsWithNumber(line) and startsWithNumber(nextLine) :
            if extractInteger(line)[0] == extractInteger(nextLine)[0] - 1:
                formattedText += '\n' + line
                putNewLineAfterBlock = True
            else:
                formattedText += line + ' '
        elif (startsWithNumber(line) and startsWithNumber(lineBefore)):
            if extractInteger(lineBefore)[0] == extractInteger(line)[0] - 1:
                formattedText += '\n' + line
                putNewLineAfterBlock = True
            else:
                formattedText += ' ' + line

        # special texts for single lines
        elif textContainsStringTuple(line, listSingleLineIncludes):
            formattedText += '\n' + line
            putNewLineAfterBlock = True

        # put new line after block:
        elif putNewLineAfterBlock:
            formattedText += '\n' + line
            putNewLineAfterBlock = False
        
        else:
            formattedText += ' ' + line

        lineBefore = line

    return formattedText
    

def lvSentTokenizer(langtext: str) -> str:
    # tokenize sentences and put on sentence into on line
    add_abbrev = ["dgl", "pol", "einschl", "max", "fa", "incl", "min", "pos", "ca", "cu", "gm", "cm"]   # additional abbreviations to NOT end a sentence
    # sentence_tokenizer = nltk.data.load("tokenizers/punkt/german.pickle")                   # load german words
    

    sentence_tokenizer = pickle

    sentence_tokenizer._params.abbrev_types.update(add_abbrev)                              # add abreviations
    langtextParagraphs = langtext.split('\n\n')                                             # split into paragraphs to keep them
    langtextSentences = ""
    for langtextParagraph in langtextParagraphs:
        # join different senteces with newlines and add double newlines to keep paragraphs
        langtextSentences += "\n".join(sentence_tokenizer.tokenize(langtextParagraph)).strip() + "\n\n"
    return langtextSentences


def createDir(pathRel: str):
    # create directiories of a relative path
    pathAbs = os.path.abspath(pathRel)
    os.makedirs(os.path.dirname(pathAbs), exist_ok=True)
    return 1


def getImportFiles(importDir: str) -> list:
    # get list of files to import with extentions below
    fileExtensions = ('.X81','.X82','.X83','.X84','.X85','.X86')

    res = []
    # Iterate directory
    for file in os.listdir(importDir):
        # check only text files
        if file.endswith(fileExtensions):
            res.append(file)
    return res


def getExportDirList(exportDir: str, names: list) -> list:
    # create list of export directories from names
    res = []
    for name in names:
        res.append(exportDir + '\\' + slugify(Path(name).stem))

    return res
    

def process_langtext(langtext: str):
    langtext = iTwoTextFormatter(langtext)  # Remove unnecessary newlines
    return lvSentTokenizer(langtext)        # Tokenize

def load_lv(path: str):
    # load lv with langtext processing
    parser = XmlGaebParser(path)
    df = parser.get_df()
    df['Langtext'] = df['Langtext'].apply(process_langtext)
    return df

def _save_lv_to_txt(lv_df: pd.DataFrame, exportDir: str, with_parameter = False):
    # go trough positions and save as separate txt files in directorys
    paths = []
    for idx in lv_df.index:

        # format content for text file
        content = ''
        if with_parameter:
            content +=  'Kurztext: ' + lv_df['Kurztext'][idx]
            content += '\nME: ' + lv_df['QU'][idx]
            content += '\nMenge: '+ lv_df['Qty'][idx]
            content += '\n\nLangtext:\n'
        
        content += lv_df['Langtext'][idx]

        # write
        fileName = slugify(lv_df['Kurztext'][idx])+'.txt'
        dir_path = exportDir + '\\' + slugify(lv_df['Gewerk'][idx]) + '\\' + slugify(lv_df['Untergewerk'][idx])
        dir_path = os.path.normpath(dir_path) # clean path, also for empty gewerk and untergewerk
        file_path = os.path.join(dir_path, fileName)

        write_file_abs_path(content, file_path)
        paths.append(file_path)
    
    return paths

def save_lv(lv_df: pd.DataFrame, exportDir: str):
    paths = _save_lv_to_txt(lv_df, exportDir)
    #_save_lv_database_into_import(lv_df, exportDir, paths)
    return paths

def pointToComma(text: str) -> str:
    return text.replace(".",",")
    
def export2itwoXls(lvFileName: str, importDir:str):
    # read Lv 
    fileNameImport = importDir + '\\' + lvFileName
    parser = XmlGaebParser(fileNameImport)
    df = parser.get_df()
    # filter
    dfOverviewUg = df[["OZ0","OZ1","Gewerk","Untergewerk"]]
    dfOverviewG = df[["OZ0","Gewerk"]]

    # drop
    dfOverviewUg = dfOverviewUg.drop_duplicates()
    dfOverviewG = dfOverviewG.drop_duplicates()

    # go trough positions and save as separate txt files in directorys
    dfWork = df
    for idx in dfOverviewUg.index:
        dfWork.loc[idx-0.5] = dfOverviewUg.loc[idx]                     # insert line
        dfWork['Kurztext'][idx-0.5] = dfOverviewUg["Untergewerk"][idx]  

    for idx in dfOverviewG.index:
        dfWork.loc[idx-0.8] = dfOverviewG.loc[idx]                  # insert line
        dfWork['Kurztext'][idx-0.8] = dfOverviewG["Gewerk"][idx]    # change Kurztext

    dfWork.sort_index(inplace=True)
    dfOutput = dfWork[["OZ0","OZ1","OZ3","Kurztext", "Qty","QU", "Langtext"]]   # output only important columns to iTwo
    
    # replace decimal sep 
    for index in dfOutput.index:
        if pd.notna(dfOutput.at[index, 'Qty']):
            dfOutput.at[index, 'Qty'] = dfOutput.at[index, 'Qty'].replace(".", ",")

    dfOutput.to_excel(Path(lvFileName).stem+".xlsx",index=False)

    return 0 




