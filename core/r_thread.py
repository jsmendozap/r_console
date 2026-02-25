from qgis.PyQt.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, QMetaObject, Qt
from .r_bridge import RBridge, RPathRequiredError

class RWorker(QObject):
    initialized = pyqtSignal(str)        
    line_result = pyqtSignal(str, dict)  
    run_finished = pyqtSignal()
    failed = pyqtSignal(str)
    busy_changed = pyqtSignal(bool)
    path_required = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._bridge = None

    @pyqtSlot(str)
    def initialize(self, plugin_dir):
        try:
            self._bridge = RBridge(plugin_dir)
            self.initialized.emit(self._bridge.r_version)
        except RPathRequiredError:
            self.path_required.emit()
        except Exception as e:
            self.failed.emit(f"Failed to initialize R Console: {e}")

    @pyqtSlot(str, int)
    def run_code_block(self, code, width):
        if self._bridge is None:
            self.failed.emit("R bridge is not initialized.")
            self.run_finished.emit()
            return

        self.busy_changed.emit(True)
        try:
            for line in code.splitlines():
                if not line.strip():
                    continue
                result = self._bridge.run_code(line, width=width)
                self.line_result.emit(line, result)
        except Exception as e:
            self.failed.emit(f"Execution error: {e}")
        finally:
            self.busy_changed.emit(False)
            self.run_finished.emit()

    @pyqtSlot()
    def shutdown(self):
        try:
            if self._bridge is not None:
                self._bridge.stop()
        except Exception:
            pass
        finally:
            self._bridge = None


class RRunner(QObject):
    initialized = pyqtSignal(str)
    line_result = pyqtSignal(str, dict)
    run_finished = pyqtSignal()
    failed = pyqtSignal(str)
    busy_changed = pyqtSignal(bool)
    path_required = pyqtSignal()
    request_initialize = pyqtSignal(str)
    request_run = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self._thread = QThread()
        self._worker = RWorker()
        self._worker.moveToThread(self._thread)

        self.request_initialize.connect(self._worker.initialize)
        self.request_run.connect(self._worker.run_code_block)
        
        self._worker.initialized.connect(self.initialized)
        self._worker.path_required.connect(self.path_required)
        self._worker.line_result.connect(self.line_result)
        self._worker.run_finished.connect(self.run_finished)
        self._worker.failed.connect(self.failed)
        self._worker.busy_changed.connect(self.busy_changed)

        self._thread.start()

    def initialize(self, plugin_dir):
        self.request_initialize.emit(plugin_dir)

    def run(self, code, width):
        self.request_run.emit(code, width)

    def stop(self):
        QMetaObject.invokeMethod(
            self._worker,
            "shutdown",
            Qt.BlockingQueuedConnection
        )
        self._thread.quit()
        self._thread.wait()
