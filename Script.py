import os

class Script:
    """Represents a pyhton script in storage"""

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def deleteScript(self):
       if os.path.exists(self.path):
           os.remove(self.path)