from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox
import os

class HelpDialog(QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("R Help")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setSearchPaths([os.path.dirname(path)])

        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        self.browser.setHtml(html)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.close)

        layout.addWidget(self.browser)
        layout.addWidget(buttons)