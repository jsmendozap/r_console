from qgis.PyQt.QtCore import QRegularExpression
from qgis.PyQt.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont

class RHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []
        self._error_blocks = set()

        promptFormat = QTextCharFormat()
        promptFormat.setForeground(QColor("#0E0ED0"))
        promptFormat.setFontWeight(QFont.Bold)
        
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor("#2e7d32"))
        
        funcFormat = QTextCharFormat()
        funcFormat.setForeground(QColor("#0E0ED0"))
        
        self.errorFormat = QTextCharFormat()
        self.errorFormat.setForeground(QColor("red"))

        self.highlightingRules.append((QRegularExpression(r"^> "), promptFormat))
        self.highlightingRules.append((QRegularExpression(r'"[^"]*"'), stringFormat))
        self.highlightingRules.append((QRegularExpression(r"'[^']*'"), stringFormat))
        self.highlightingRules.append((QRegularExpression(r"\b[A-Za-z0-9_.]+(?=\()"), funcFormat))

    def highlightBlock(self, text):
        if self.currentBlock().blockNumber() in self._error_blocks:
            self.setFormat(0, len(text), self.errorFormat)
            return
        for pattern, fmt in self.highlightingRules:
            match = pattern.match(text)
            while match.hasMatch():
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
                match = pattern.match(text, match.capturedStart() + match.capturedLength())

    def mark_error_block(self, block):
        self._error_blocks.add(block.blockNumber())
        self.rehighlightBlock(block)

    def clear_errors(self):
        self._error_blocks.clear()
        self.rehighlight()

