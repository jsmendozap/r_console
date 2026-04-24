"""QtCore compatibility shims that preserve PyQt5-style enum names on Qt6."""

from qgis.PyQt.QtCore import Qt as _Qt
from .utils import resolve_enum


class _QtCompat:
    BlockingQueuedConnection = (
        resolve_enum(_Qt, "ConnectionType", "BlockingQueuedConnection")
    )
    RightDockWidgetArea = resolve_enum(_Qt, "DockWidgetArea", "RightDockWidgetArea")
    TopRightCorner = resolve_enum(_Qt, "Corner", "TopRightCorner")
    Vertical = resolve_enum(_Qt, "Orientation", "Vertical")
    NoModifier = resolve_enum(_Qt, "KeyboardModifier", "NoModifier")
    Key_Return = resolve_enum(_Qt, "Key", "Key_Return")
    Key_Enter = resolve_enum(_Qt, "Key", "Key_Enter")
    Key_Backspace = resolve_enum(_Qt, "Key", "Key_Backspace")
    Key_Delete = resolve_enum(_Qt, "Key", "Key_Delete")
    Key_Left = resolve_enum(_Qt, "Key", "Key_Left")
    Key_Up = resolve_enum(_Qt, "Key", "Key_Up")
    Key_Down = resolve_enum(_Qt, "Key", "Key_Down")
    CustomContextMenu = resolve_enum(_Qt, "ContextMenuPolicy", "CustomContextMenu")
    KeepAspectRatio = resolve_enum(_Qt, "AspectRatioMode", "KeepAspectRatio")
    SmoothTransformation = (
        resolve_enum(_Qt, "TransformationMode", "SmoothTransformation")
    )

    def __getattr__(self, name):
        return getattr(_Qt, name)


Qt = _QtCompat()
