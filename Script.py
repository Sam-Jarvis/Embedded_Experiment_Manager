import os

class Script:
    """Represents a pyhton script in storage"""

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def deleteScript(self):
        """Removes the script associated with this script object"""
        if os.path.exists(self.path):
            os.remove(self.path)

    def execute(self):
        """Executes the script associated with with script object"""
        bash_location = "/bin/bash"
        command = f"sudo {bash_location} {self.path}"
        os.system(command)