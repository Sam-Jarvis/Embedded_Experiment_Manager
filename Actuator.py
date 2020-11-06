import Script

class Actuator:
    """Defines a physical actuator of the system"""

    def __init__(self, name: str, pin: int, duty_cycle: int, activate: Script, deactivate: Script):
        self.name = name
        self.pin = pin
        self.duty_cycle = duty_cycle
        self.activate = activate
        self.deactivate

    def getName():
        return self.name

    def getPin():
        return self.pin

    def getDuty_cycle():
        return self.duty_cycle

    def getActivate():
        return self.activate

    def getDeactivate():
        return self.deactivate