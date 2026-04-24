"""QtWidgets compatibility shims that preserve PyQt5-style enum names on Qt6."""

from qgis.PyQt.QtWidgets import (
    QDialogButtonBox as _QDialogButtonBox,
    QFrame as _QFrame,
    QHeaderView as _QHeaderView,
    QGraphicsView as _QGraphicsView,
    QListView as _QListView,
    QMessageBox as _QMessageBox,
    QStyle as _QStyle,
    QTabBar as _QTabBar,
    QTextEdit as _QTextEdit,
    QAbstractItemView as _QAbstractItemView
)

from .utils import resolve_enum


class _QStyleCompat:
    SP_DialogSaveButton = resolve_enum(_QStyle, "StandardPixmap", "SP_DialogSaveButton")
    SP_FileDialogStart = resolve_enum(_QStyle, "StandardPixmap", "SP_FileDialogStart")
    SP_MediaPlay = resolve_enum(_QStyle, "StandardPixmap", "SP_MediaPlay")
    SP_FileDialogDetailedView = (
        resolve_enum(_QStyle, "StandardPixmap", "SP_FileDialogDetailedView")
    )
    SP_DialogResetButton = resolve_enum(_QStyle, "StandardPixmap", "SP_DialogResetButton")
    SP_BrowserReload = resolve_enum(_QStyle, "StandardPixmap", "SP_BrowserReload")
    SP_BrowserStop = resolve_enum(_QStyle, "StandardPixmap", "SP_BrowserStop")
    SP_DirOpenIcon = resolve_enum(_QStyle, "StandardPixmap", "SP_DirOpenIcon")
    SP_DialogNoButton = resolve_enum(_QStyle, "StandardPixmap", "SP_DialogNoButton")
    SP_DialogYesButton = resolve_enum(_QStyle, "StandardPixmap", "SP_DialogYesButton")

    def __getattr__(self, name):
        return getattr(_QStyle, name)


class _QFrameCompat:
    NoFrame = resolve_enum(_QFrame, "Shape", "NoFrame")

    def __call__(self, *args, **kwargs):
        return _QFrame(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(_QFrame, name)


class _QDialogButtonBoxCompat:
    Ok = resolve_enum(_QDialogButtonBox, "StandardButton", "Ok")
    Cancel = resolve_enum(_QDialogButtonBox, "StandardButton", "Cancel")
    Close = resolve_enum(_QDialogButtonBox, "StandardButton", "Close")
    Save = resolve_enum(_QDialogButtonBox, "StandardButton", "Save")

    def __call__(self, *args, **kwargs):
        return _QDialogButtonBox(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(_QDialogButtonBox, name)


class _QMessageBoxCompat:
    Save = resolve_enum(_QMessageBox, "StandardButton", "Save")
    Discard = resolve_enum(_QMessageBox, "StandardButton", "Discard")
    Cancel = resolve_enum(_QMessageBox, "StandardButton", "Cancel")
    Yes = resolve_enum(_QMessageBox, "StandardButton", "Yes")
    No = resolve_enum(_QMessageBox, "StandardButton", "No")

    def __getattr__(self, name):
        return getattr(_QMessageBox, name)


class _QTabBarCompat:
    RightSide = resolve_enum(_QTabBar, "ButtonPosition", "RightSide")

    def __getattr__(self, name):
        return getattr(_QTabBar, name)


class _QGraphicsViewCompat:
    ScrollHandDrag = resolve_enum(_QGraphicsView, "DragMode", "ScrollHandDrag")

    def __call__(self, *args, **kwargs):
        return _QGraphicsView(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(_QGraphicsView, name)


class _QListViewCompat:
    IconMode = resolve_enum(_QListView, "ViewMode", "IconMode")
    LeftToRight = resolve_enum(_QListView, "Flow", "LeftToRight")
    Adjust = resolve_enum(_QListView, "ResizeMode", "Adjust")

    def __getattr__(self, name):
        return getattr(_QListView, name)


class _QTextEditCompat:
    NoWrap = resolve_enum(_QTextEdit, "LineWrapMode", "NoWrap")

    def __call__(self, *args, **kwargs):
        return _QTextEdit(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(_QTextEdit, name)


class _QHeaderViewCompat:
    Stretch = resolve_enum(_QHeaderView, "ResizeMode", "Stretch")

    def __call__(self, *args, **kwargs):
        return _QHeaderView(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(_QHeaderView, name)


class _QAbstractItemViewCompat():
    NoEditTriggers = resolve_enum(_QAbstractItemView, "EditTrigger", "NoEditTriggers")

    def __getattr__(self, name):
        return getattr(_QAbstractItemView, name)


QStyle = _QStyleCompat()
QFrame = _QFrameCompat()
QDialogButtonBox = _QDialogButtonBoxCompat()
QMessageBox = _QMessageBoxCompat()
QTabBar = _QTabBarCompat()
QGraphicsView = _QGraphicsViewCompat()
QListView = _QListViewCompat()
QTextEdit = _QTextEditCompat()
QHeaderView = _QHeaderViewCompat()
QAbstractItemView = _QAbstractItemViewCompat()