"""Qsci compatibility shims that preserve PyQt5-style enum names on Qt6."""

from qgis.PyQt.Qsci import QsciScintilla as _QsciScintilla, QsciAPIs

from .utils import resolve_enum


class _QsciScintillaCompat:
    AcsAPIs = resolve_enum(_QsciScintilla, "AutoCompletionSource", "AcsAPIs")
    AcsNone = resolve_enum(_QsciScintilla, "AutoCompletionSource", "AcsNone")
    AcusNever = (
        resolve_enum(_QsciScintilla, "AutoCompletionUseSingle", "AcusNever")
    )
    CallTipsAboveText = (
        resolve_enum(_QsciScintilla, "CallTipsPosition", "CallTipsAboveText")
    )
    NoFoldStyle = resolve_enum(_QsciScintilla, "FoldStyle", "NoFoldStyle")

    def __getattr__(self, name):
        return getattr(_QsciScintilla, name)


QsciScintilla = _QsciScintillaCompat()
