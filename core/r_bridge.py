from . import plugin_settings
from shutil import which
import subprocess
import json
import os

class RPathRequiredError(RuntimeError):
    pass

class RBridge:
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.process = None
        self.r_version = None
        self.r = self._find_rscript()

    def initialize(self):
        self.process = self._start()
        self.r_version = self._get_r_version()
        self._set_wd()
        
    def run_code(self, code, width=None):
        data = {"code": code}
        if width:
            data["width"] = int(width)
        request = json.dumps(data) + "\n"

        self.process.stdin.write(request)
        self.process.stdin.flush()

        response = self.process.stdout.readline().strip()
        
        if not response:
            raise RuntimeError("R process returned empty response (process might have crashed).")
            
        return json.loads(response.strip())
    
    def stop(self):
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=2)

    def restart(self):
        self.stop()
        self.process = self._start()
        self._set_wd()
            
    def _start(self):
        base = os.path.basename(self.r).lower()
        args = [self.r, "--vanilla"]
        
        if "rscript" not in base:
            args.extend(["--slave", "-f", "r_worker.R"])
        else:
            args.append("r_worker.R")

        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) if os.name == "nt" else 0

        process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=self.plugin_dir, 
            creationflags=creationflags
        )

        ready = process.stdout.readline().strip()

        if ready != "READY":
            stderr_output = process.stderr.read().strip()
            detail = f"\nR stderr: {stderr_output}" if stderr_output else ""
            process.kill()
            raise RuntimeError("Failed to start R worker process. {detail}")
        
        return process     

    def _get_r_version(self):
        code = "cat(paste0(R.Version()$major, '.', R.Version()$minor))"
        response = self.run_code(code)
        return response["stdout"].strip()
    
    def _find_rscript(self):
        saved = plugin_settings.get_r_path()
        if saved:
            return saved
        
        path = which('Rscript')
        if path:
            return path
        
        raise RPathRequiredError("R/Rscript not found. Plase set the path in settings.")

    def _set_wd(self):
        wd = plugin_settings.get_initial_wd()
        wd = wd.replace('\\', '/').replace('"', '\\"')
        self.run_code(f'setwd("{wd}")')
