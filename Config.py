import configparser
import string
import re
import os, stat

import Actuator
import Sensor
# actuator re pattern: ^(actuator)\d+$
# sensor re pattern: ^(sensor)\d{1,}$

parser = configparser.ConfigParser()
actuators = []
sensors = []

class Config:
    """Responsible for parsing the config file and other such tasks"""

    def __init__(self, cfg: str):
        parser.read(cfg)

    def limitIntensity(self, intensity):
        if intensity > 100:
            return 100
        return intensity

    def limitFrequency(self, frequency):
        if frequency > 0:
            return int(round(24 / frequency))
        elif frequency == 0:
            return 0
        else:
            return -1

    # TODO: finish once generate script is done
    def parse(self):
        for sec in parser.sections():
            name = str()
            typ = bool()
            pin = int()
            frequency = int()
            length = int()
            intensity = int()
            for opt in parser.options(sec):
                if opt == "name":
                    name = parser.get(sec, opt)
                elif opt == "type":
                    typ = parser.getboolean(sec, opt)
                elif opt == "pin":
                    pin = parser.getint(sec, opt)
                elif opt == "frequency":
                    frequency = parser.getint(sec, opt)
                elif opt == "length":
                    length = parser.getint(sec, opt)
                elif opt == "intensity":
                    intensity = parser.getint(sec, opt)
            if typ:
                actuator = []
                a = Actuator.Actuator(name, pin)
                actuator.append(a)
                actuator.append(self.limitFrequency(frequency))
                actuator.append(length)
                actuator.append(self.limitIntensity(intensity))
                actuators.append(actuator)
            else:
                s = Sensor.Sensor(name, pin)
                sensors.append(s)

    def minutesToHours(self, minutes):
        hours = int(minutes / 60)
        minutes = minutes % 60
        return (hours, minutes)

    def generateScript(self, user, act_name, script_type, pin, root="home", folder="gpio_scripts"):

        path = f"/{root}/{user}/.{folder}"
        script_type = str()
        name = act_name.replace(" ", "_")
        full_path = str()

        if script_type:
            script_type = "gpio_out_activate.py"
            name += "_activate"
        else:
            script_type = "gpio_out_deactivate.py"
            name += "_deactivate"

        script = f"sudo python3 {script_type} {pin}"

        if not os.path.exists(path):
            os.mkdir(path)
        elif os.path.exists(path):
            full_path = f"{path}/{name}.sh"
            with open(full_path, "w") as bash_script:
                bash_script.write(script)
            os.chmod(full_path, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

        return full_path

    def getLogFrequency():
        return sensor_log_frequency

    def getSensors(self):
        return sensors

    # DEBUG
    def print_config_file(self):
        for sec in parser.sections():
            print(sec)
            for opt in parser.options(sec):
                print(f"\t {opt}")

    def print_actuators(self):
        for i in actuators:
            print(i)

    def print_sensors(self):
        for i in sensors:
            print(i.name)