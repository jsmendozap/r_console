"""QtWebSockets compatibility imports."""
from qgis.PyQt.QtCore import QT_VERSION_STR

if QT_VERSION_STR.startswith("5."):
    from PyQt5.QtWebSockets import QWebSocket
elif QT_VERSION_STR.startswith("6."):
    from PyQt6.QtWebSockets import QWebSocket