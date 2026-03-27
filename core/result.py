"""Defines the RResult class for parsing messages from the R process."""
from .utils import MissingDependencyError

class RResult(dict):
    """
    A dictionary-like object that parses and represents a JSON message from R.

    It categorizes the message (e.g., chunk of output, error, request for data)
    and provides convenient properties to access its contents.
    """

    def __init__(self, msg):
        """
        Initializes and parses the message from R.

        Args:
            msg (dict): The raw JSON message received from the R subprocess.
        """
        super().__init__()
        self.stdout = ""
        self.error = None
        self.wd = None
        self.expression = None
        self.is_done = False
        self.is_request = False
        self.is_pkg = False
        self.is_help = False
        self.method = None
        self.args = None
        self.signatures = None
        self.path = None
        self._parse(msg)

    def _parse(self, msg):
        """
        Parses the raw message dictionary and sets the object's properties.

        Args:
            msg (dict): The raw JSON message.

        Raises:
            MissingDependencyError: If R reports a missing package.
        """
        match msg["type"]:
            case "expression":
                self.expression = msg["data"]
            case "chunk":
                self.stdout = msg["data"]
                self.wd = msg.get("wd")
                self.update(stdout=self.stdout, error=None, wd=self.wd)
            case "done":
                self.error = msg.get("error")
                self.wd = msg.get("wd")
                self.is_done = True
                self.update(stdout="", error=self.error, wd=self.wd)
            case "request":
                self.method = msg["method"]
                self.args = msg.get("args")
                self.is_request = True
                self.is_done = False
            case "pkg":
                self.signatures = msg['data']
                self.is_pkg = True
            case "help":
                self.is_help = True
                self.path = msg['path']
            case "question":
                self.method = "question"
                self.args = msg
                self.is_request = True
                self.is_done = False
            case "missing":
                raise MissingDependencyError(f"The following R packages are required but are not installed: {msg['data']}")

    def __bool__(self):
        """
        Returns False if the message indicates the end of an execution block.

        This is used to control the loop in RBridge.run_code.
        """
        return not self.is_done
