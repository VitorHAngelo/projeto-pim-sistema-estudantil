from os import path, mkdir

FILES_PATH = "./files/"

GUI_FONT = "Calibri"

if not path.exists(FILES_PATH):
    mkdir(FILES_PATH)
