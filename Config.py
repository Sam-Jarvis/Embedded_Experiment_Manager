import configparser
import string
import re

# actuator re pattern: ^(actuator)\d+$
# sensor re pattern: ^(sensor)\d{1,}$

parser = configparser.ConfigParser()
actuators = []
sensors = []

class Config:
    """Responsible for parsing the config file and other such tasks"""

    def __init__(self, cfg: str):
        parser.read(cfg)

    # DEBUG
    def print_config_file(self):
        for sec in parser.sections():
            print(sec)
            for opt in parser.options(sec):
                print(f"\t {opt}")

    def parseActuators(self, section_header = "actuator"):
        pattern = re.compile(f"^({section_header})\d+$")

        for section in parser.sections():
            if re.match(pattern, section.lower()) is not None:
                

    def createSensor():
        pass

    def generateScripts():
        pass

    def getLogFrequency():
        return sensor_log_frequency