import Script

class Actuator:
    """Defines a physical actuator of the system"""

    def __init__(self, name: str, pin: int, activate: Script, deactivate: Script):
        self.name = name
        self.pin = pin
        self.activate = activate
        self.deactivate = deactivate

    def toString(self):
        return f"Name: {self.name}; \n Pin: {self.pin}; \n Activate Script: {self.activate.path}; \n Deactivate Script: {self.deactivate.path};\n"