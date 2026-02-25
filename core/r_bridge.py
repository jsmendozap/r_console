from qgis.PyQt.QtCore import QSettings
from shutil import which
from subprocess import Popen, PIPE, TimeoutExpired
import json
import os

class RPathRequiredError(RuntimeError):
    pass

class RBridge:
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.settings = QSettings("r_console", "RConsole")
        self.r = self._find_rscript()
        self.process = self._start()
        self.r_version = self._get_r_version()
        self._set_home()
        
    def run_code(self, code, width=None):
        data = {"code": code}
        if width:
            data["width"] = int(width)
        request = json.dumps(data) + "\n"

        self.process.stdin.write(request)
        self.process.stdin.flush()

        response = self.process.stdout.readline().strip()
        
        if not response:
            raise RuntimeError("R process returned empty response (process might have crashed or path is invalid).")
            
        return json.loads(response.strip())
    
    def stop(self):
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=2)
        except TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=2)

    def restart(self):
        self.stop()
        self.process = self._start()
        self.r_version = self._get_r_version()
        self._set_home()
            
    def _start(self):
        base = os.path.basename(self.r).lower()
        args = [self.r, "--vanilla"]
        
        if "rscript" not in base:
            args.extend(["--slave", "-f", "r_worker.R"])
        else:
            args.append("r_worker.R")

        process = Popen(
            args,
            stdin=PIPE, 
            stdout=PIPE, 
            text=True,
            bufsize=1,
            cwd=self.plugin_dir
        )

        ready = process.stdout.readline().strip()

        if ready != "READY":
            raise RuntimeError("Failed to start R worker process.")
        
        return process     

    def _get_r_version(self):
        code = "cat(paste0(R.Version()$major, '.', R.Version()$minor))"
        response = self.run_code(code)
        return response["stdout"].strip()
    
    def _find_rscript(self):
        path = which('Rscript')
        if path:
            return path
        
        saved = self.settings.value('r_path')
        if saved:
            return saved
        
        raise RPathRequiredError("Rscript not found in PATH.")

    def _set_home(self):
        home = os.path.expanduser('~').replace('\\', '/')
        self.run_code(f"setwd('{home}')")
