import configparser
import string
import re
import os, stat
import getpass

import Actuator
import Script
import Sensor

act = "^(actuator)\d+$"
sen = "^(sensor)\d{1,}$"
gen = "^(general)$"

# TODO: This is current not used, i.e. redundant
system_user = getpass.getuser()
parser = configparser.ConfigParser()
sensor_log_freq = int()
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

    # TODO: finish once generate script is done
    def parse(self):
        for sec in parser.sections():
            section = parser[sec]
            sec = sec.lower()
            if re.match(act, sec):
                name = str(section["name"])
                typ = bool(section["type"])
                pin = int(section["pin"])
                frequency = int(section["frequency"])
                length = int(section["length"])
                intensity = int(section["intensity"])

                actuator = []

                activate_name, activate_path = self.generateScript(act_name = name, script_tpe = True, pin = pin, log_file = "actuator_log.csv")
                activate = Script.Script(activate_name, activate_path)

                deactivate_name, deactivate_path = self.generateScript(act_name = name, script_tpe = False, pin = pin, log_file = "actuator_log.csv")
                deactivate = Script.Script(deactivate_name, deactivate_path)

                a = Actuator.Actuator(name, pin, activate, deactivate)
                actuator.append(a)
                actuator.append(frequency)
                actuator.append(length)
                actuator.append(self.limitIntensity(intensity))
                actuators.append(actuator)

            elif re.match(sen, sec):
                name = str(section["name"])
                typ = bool(section["type"])
                pin = int(section["pin"])

                s = Sensor.Sensor(name, pin)
                sensors.append(s)

            elif re.match(gen, sec):
                sensor_log_freq = int(section["sensor_log_frequency"])


    def generateScript(self, act_name, script_tpe, pin, log_file, root="home", user="ubuntu", folder="gpio_scripts"):

        path = f"/{root}/{user}/.{folder}"
        script_type = str()
        act_name = act_name.replace(" ", "_").replace("\"", "")
        name = act_name
        full_path = str()

        if script_tpe:
            script_type = f"{os.getcwd()}/scripts/gpio_out_activate.py"
            name += "_activate"
        else:
            script_type = f"{os.getcwd()}/scripts/gpio_out_deactivate.py"
            name += "_deactivate"

        script = f"sudo python3 {script_type} {pin} {path}/{log_file} {act_name}"

        if not os.path.exists(path):
            os.mkdir(path)
        elif os.path.exists(path):
            full_path = f"{path}/{name}.sh"
            if not os.path.exists(full_path):
                with open(full_path, "w") as bash_script:
                    bash_script.write(script)
                os.chmod(full_path, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

        return name, full_path

    def getActuators(self):
        return actuators

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