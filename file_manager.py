from os import getcwd, path, makedirs
from datetime import datetime
from pandas import DataFrame, read_excel, ExcelWriter, merge
from tkinter.filedialog import askopenfilename

COLOR_DICTIONARY = {
    "BACKGROUND": "#0076CF",
    "BUTTON_SUCCESS": "#00A29B",
    "BUTTON_NEUTRAL": "#F76800",
    "ERROR": "#C00000",
    "TEXT": "#333333"
}

class File_Initializer:
    def __init__(self):
        if not path.exists(path.join(getcwd(), r"Output")):
            makedirs(path.join(getcwd(), r"Output"))

def spreadsheetUploader(dict: dict,
                        dict_key: str,
                        button):
    dict[dict_key] = read_excel(askopenfilename(filetypes = [("Excel Files","*.xlsx")]))
    button.configure(bg = COLOR_DICTIONARY["BUTTON_SUCCESS"])