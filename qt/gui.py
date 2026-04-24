"""QtGui compatibility shims that preserve PyQt5-style enum names on Qt6."""

from qgis.PyQt.QtGui import QFont as _QFont, QTextCursor as _QTextCursor
from .utils import resolve_enum


class _QTextCursorCompat:
    End = resolve_enum(_QTextCursor, "MoveOperation", "End")
    StartOfBlock = resolve_enum(_QTextCursor, "MoveOperation", "StartOfBlock")
    KeepAnchor = resolve_enum(_QTextCursor, "MoveMode", "KeepAnchor")

    def __call__(self, *args, **kwargs):
        return _QTextCursor(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(_QTextCursor, name)


class _QFontCompat:
    TypeWriter = resolve_enum(_QFont, "StyleHint", "TypeWriter")
    Monospace = resolve_enum(_QFont, "StyleHint", "Monospace")

    def __call__(self, *args, **kwargs):
        return _QFont(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(_QFont, name)


QTextCursor = _QTextCursorCompat()
QFont = _QFontCompat()
