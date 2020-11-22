import Script

class Sensor:
    """Defines a physical sensor of the system"""

    def __init__(self, name, pin, read: Script):
        self.name = name
        self.pin = pin
        self.read = read
