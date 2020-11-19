import configparser
import string
import re
import os, stat

import Actuator
import Script
import Sensor

act = "^(actuator)\d+$"     # Actuator regex detection pattern 
sen = "^(sensor)\d{1,}$"    # Sensor regex detection pattern
gen = "^(general)$"         # General settings regex detection pattern

parser = configparser.ConfigParser()

sensor_log_freq = int()         # Stores the log frequency of sensors from the config file
experiment_duration = int()     # Stores the experiment from the config file
error_check_frequency = int()   # Stores the frequency of error checks from the config file

actuators = []  # List of all actuators created from the config file
sensors = []    # List of all sensors created from the config file

class Config:
    """Responsible for parsing the config file and other such tasks"""

    def __init__(self, cfg: str):
        parser.read(cfg)

    def limitIntensity(self, intensity: int) -> int: 
    """Ensures that the intensity value passed to it is not more than 100%"""
        if intensity > 100:
            return 100
        return intensity

    def parse(self):
    """Reads the config file, creates actuators and sensors adding them to the relevant lists and parses the general experiment options"""
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

                activate_name, activate_path = self.generateScript(dev_name = name, script_tpe = 1, pin = pin, log_file = "actuator_log.csv")
                activate = Script.Script(activate_name, activate_path)

                deactivate_name, deactivate_path = self.generateScript(dev_name = name, script_tpe = 0, pin = pin, log_file = "actuator_log.csv")
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

                read_name, read_path = self.generateScript(dev_name = name, script_tpe = 2, pin = 22, log_file = "sensor_log.csv")
                read = Script.Script(read_name, read_path)

                s = Sensor.Sensor(name, pin, read)
                sensors.append(s)

            elif re.match(gen, sec):
                self.sensor_log_freq = int(section["sensor_log_frequency"])
                self.experiment_duration = int(section["experiment_duration"])
                self.error_check_frequency = int(section["error_check_frequency"])


    def generateScript(self, dev_name: str, script_tpe: int, pin: int, log_file: str, root="home": str, user="ubuntu": str, folder="gpio_scripts": str) -> str:
    """Creates a bash script that can be executed by cron. The script wraps a python script with the necessary command line arguments"""
        path = f"/{root}/{user}/.{folder}"
        script_type = str()
        act_name = dev_name.replace(" ", "_").replace("\"", "")
        name = act_name
        full_path = str()

        if script_tpe == 1:
            script_type = f"{os.getcwd()}/scripts/gpio_out_activate.py"
            name += "_activate"
        elif script_tpe == 0:
            script_type = f"{os.getcwd()}/scripts/gpio_out_deactivate.py"
            name += "_deactivate"
        elif script_tpe == 2:
            script_type = f"{os.getcwd()}/scripts/gpio_in.py"

        script = f"sudo python3 {script_type} {pin} {path}/{log_file} {dev_name}"

        if not os.path.exists(path):
            os.mkdir(path)
        elif os.path.exists(path):
            full_path = f"{path}/{name}.sh"
            if not os.path.exists(full_path):
                with open(full_path, "w") as bash_script:
                    bash_script.write(script)
                os.chmod(full_path, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

        return name, full_path


    def getActuators(self) -> list:
    """Returns the list of actuators to caller"""
        return actuators

    def getSensors(self) -> list:
    """Returns the list of sensors to caller"""
        return sensors

    def getSensorLogFrequency(self) -> int:
    """Returns the sensor log frequency to caller"""
        return self.sensor_log_freq

    def getExperimentDuration(self) -> int:
    """Returns the experiment duration to caller"""
        return self.experiment_duration

    def getErrorCheckFrequency(self) -> int:
    """Returns the error checking frequency to caller"""
        return self.error_check_frequency

    # DEBUG METHODS
    def print_config_file(self):
    """Prints each section of the config file. For each section it prints the options"""
        for sec in parser.sections():
            print(sec)
            for opt in parser.options(sec):
                print(f"\t {opt}")

    def print_actuators(self):
    """Prints the list of actuators"""
        for i in actuators:
            print(i)

    def print_sensors(self):
    """Prints the list of sensors"""
        for i in sensors:
            print(i.name)