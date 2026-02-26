from qgis.PyQt.QtCore import QSettings
import os

_settings = QSettings("r_console", "RConsole")

KEY_R_PATH    = "r_path"
KEY_INITIAL_WD = "initial_wd"


def get_r_path():
    return _settings.value(KEY_R_PATH, "", type=str)

def set_r_path(path: str):
    _settings.setValue(KEY_R_PATH, path)

def get_initial_wd():
    wd = _settings.value(KEY_INITIAL_WD, "", type=str)
    if not wd:
        wd = os.path.expanduser("~")
    return wd

def set_initial_wd(path: str):
    _settings.setValue(KEY_INITIAL_WD, path)