import subprocess
import os

def is_valid_rscript(path):
        path = os.path.normpath(path.replace('\\', '/'))
        path = os.path.realpath(path)

        if not os.path.isfile(path):
            return False
        
        kwargs = {}
        if os.name == 'nt':
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW

        try:
            result = subprocess.run(
                [path, '-e', 'R.version.string'],
                capture_output=True,
                text=True,
                timeout=5,
                **kwargs
            )
            output = result.stdout + result.stderr
            return 'R version' in output
        except Exception:
            return False

def root_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class RPathRequiredError(RuntimeError):
    pass    

class MissingDependencyError(RuntimeError):
    pass