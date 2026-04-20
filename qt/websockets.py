"""QtWebSockets compatibility imports."""

try:
    from qgis.PyQt.QtWebSockets import QWebSocket
except ModuleNotFoundError:
    try:
        from PyQt5.QtWebSockets import QWebSocket
    except ModuleNotFoundError:
        from PyQt6.QtWebSockets import QWebSocket
