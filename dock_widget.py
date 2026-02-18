from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QIcon, QFont, QTextCursor
from qgis.PyQt.Qsci import QsciScintilla, QsciLexerPython

try:
    from qgis.PyQt.Qsci import QsciLexerR
except ImportError:
    QsciLexerR = None

from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QToolButton,
    QTabWidget,
    QSplitter,
    QLabel,
    QStyle, 
    QFrame,
    QLineEdit
)



class RConsoleDockWidget(QDockWidget):
    runRequested = pyqtSignal(str)
    settingsRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.title_label = QLabel("R Console") 
        self.title_label.setStyleSheet("font-weight: 700; font-size: 16px;")

        self.editor_tabs = QTabWidget()
        self.editor = QsciScintilla()
        self.editor.setUtf8(True)
        
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self.editor.setFont(font)
        self.editor.setMarginsFont(font)

        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "00")
        self.editor.setMarginLineNumbers(0, True)
        self.editor.setMarginsForegroundColor(Qt.gray)
        self.editor.setFrameShape(QFrame.NoFrame)
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        if QsciLexerR:
            self.editor.setLexer(QsciLexerR(self.editor))
        else:
            self.editor.setLexer(QsciLexerPython(self.editor))
        self.editor_tabs.addTab(self.editor, "*Untitled1.R")

        self.output_tabs = QTabWidget()
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setFrameShape(QFrame.NoFrame)

        self.repl = QLineEdit()
        self.repl.setPlaceholderText("Type R code here and press Enter to execute...")
        self.repl.returnPressed.connect(self._emit_repl_run)

        console_tab = QWidget()
        console_layout = QVBoxLayout(console_tab)
        console_layout.addWidget(self.history)
        console_layout.addWidget(self.repl)
        self.output_tabs.addTab(console_tab, "Console")

        self.run_button = QToolButton()
        self.run_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.run_button.setToolTip("Run")
        self.run_button.clicked.connect(self._emit_run)

        self.settings_button = QToolButton()
        self.settings_button.setIcon(QIcon.fromTheme("preferences-system", self.style().standardIcon(QStyle.SP_FileDialogDetailedView)))
        self.settings_button.setToolTip("Settings")
        self.settings_button.clicked.connect(self.settingsRequested.emit)

        self.clear_button = QToolButton()
        self.clear_button.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        self.clear_button.setToolTip("Clear")
        self.clear_button.clicked.connect(self._clear_console)

        container = QWidget()
        self.setWidget(container)

        layout = QVBoxLayout(container)

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        top_bar.addWidget(self.run_button)
        top_bar.addWidget(self.settings_button)
        top_bar.addWidget(self.clear_button)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.editor_tabs)
        splitter.addWidget(self.output_tabs)
        splitter.setSizes([350, 250])

        layout.addLayout(top_bar)
        layout.addWidget(splitter)

        self._clear_console()

    def _emit_run(self):
        code = self.editor.text()
        self.runRequested.emit(code)

    def _emit_repl_run(self):
        code = self.repl.text()
        self.runRequested.emit(code)
        self.repl.clear()

    def _clear_console(self):
        self.history.document().setDocumentMargin(8)  
        self.history.setHtml(
            "<table width='100%' cellspacing='0' cellpadding='0'>"
            "<tr>"
            "<td><span style='font-weight:700;'>R 4.3.1</span></td>"
            "<td align='right'><span style='color:#8a8a8a;'>~/QGIS_R/</span></td>"
            "</tr>"
            "</table>"
            "<hr style='margin-top:2px; margin-bottom:4px;'>"
            "<div></div>"
        )

    def append_output(self, text):
        cursor = self.history.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.history.setTextCursor(cursor)
        self.history.insertPlainText(text + "\n")
        self.history.ensureCursorVisible()

