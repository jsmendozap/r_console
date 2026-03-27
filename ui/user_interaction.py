from qgis.PyQt.QtWidgets import (
    QMessageBox, QInputDialog, QFileDialog, QDialog, 
    QVBoxLayout, QDialogButtonBox, QTableWidget, QTableWidgetItem
)
import os
import csv
from .editor import EditorTab

class QuestionDialog:

    def __init__(self, parent, method, args):
        self.parent = parent
        self.method = method
        self.args = args

    def dispatch(self):
        match self.method:
            case "ask_yes_no":
                return self._ask_yes_no()
            case "menu":
                return self._show_menu()
            case "file_choose":
                return self._file_choose()
            case "file_edit":
                return self._file_edit()
            case "readline":
                return self._readline()
            case "show_table":
                return self._show_table()

    def _ask_yes_no(self):
        question = self.args.get("question", "")
        default = self.args.get("default", True)

        default_btn = QMessageBox.Yes if default else QMessageBox.No
        ret = QMessageBox.question(self.parent, "R Question", question, QMessageBox.Yes | QMessageBox.No, default_btn)
        return {"type": "response", "data": ret == QMessageBox.Yes}
    
    def _show_menu(self):
        choices = self.args.get("choices", [])
        title = self.args.get("title") or "R Menu"
        item, ok = QInputDialog.getItem(self.parent, "R Input", title, choices, 0, False)
        if not ok:
            return {"type": "response", "data": 0}
        return {"type": "response", "data": choices.index(item) + 1}

    def _file_choose(self):
        new = self.args.get("new", False)
        if new:
            path, _ = QFileDialog.getSaveFileName(self.parent, "R File Choose")
        else:
            path, _ = QFileDialog.getOpenFileName(self.parent, "R File Choose")
        
        if not path:
            return {"type": "response", "data": ""}
        return {"type": "response", "data": path}

    def _file_edit(self):
        file_path = self.args.get("file", "")
        title = self.args.get("title") or "R Editor"

        dialog = QDialog(self.parent)
        dialog.setWindowTitle(title)
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        editor = EditorTab(dialog)
        if file_path and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                editor.setText(f.read())
            editor.mark_saved(file_path)
            
        layout.addWidget(editor)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Save).setText("Save and Close")
        
        def save_and_accept():
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(editor.text())
            dialog.accept()
            
        buttons.accepted.connect(save_and_accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.exec_()

        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
        return {"type": "response", "data": True}

    def _show_table(self):
        file_path = self.args.get("file", "")
        title = self.args.get("title") or "R View"

        dialog = QDialog(self.parent)
        dialog.setWindowTitle(title)
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        table = QTableWidget()
        if file_path and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                data = list(reader)
                if data:
                    table.setColumnCount(len(data[0]))
                    table.setHorizontalHeaderLabels(data[0])
                    table.setRowCount(len(data) - 1)
                    for row_idx, row_data in enumerate(data[1:]):
                        for col_idx, cell_data in enumerate(row_data):
                            table.setItem(row_idx, col_idx, QTableWidgetItem(cell_data))
                            
        layout.addWidget(table)
        
        dialog.exec_()
        
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
                
        return {"type": "response", "data": True}

    def _readline(self):
        prompt = self.args.get("prompt", "")
        text, ok = QInputDialog.getText(self.parent, "R Input", prompt)
        if not ok:
            return {"type": "response", "data": ""}
        return {"type": "response", "data": text}
