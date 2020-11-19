from crontab import CronTab
import os

class Scheduler:
"""Responsible for all cron job and time related tasks"""

    active_actuators = []   # All actuators that have cron jobs attached to them

    def __init__(self):
        self.cron = CronTab(user='root')

    def minutesToHours(self, minutes: int) -> tuple:
    """Converts time in minutes to time in hours and minutes (hours:minutes)"""
        hours = int(minutes / 60)
        minutes = int(minutes % 60)
        return (hours, minutes)

    def scheduleActuator(self, actuator: Actuator, frequency: int, length: int):
    """Schedules an activation and deactivation cron job for the given actuator based on the given frequency and length of operation"""
        print(f"Actuator: {actuator.name}\n")
        if frequency <= 0:
            return
        print(f"Frequency: {frequency}\n")
        bash_location = '/bin/bash'

        if actuator not in self.active_actuators:                           # Ensures actuator doesn't already have an active cron job
            self.active_actuators.append(actuator)

        activate_every_x_minutes = 1440 / frequency                         # Time in minutes between each activation
        print(f"Activates every: {activate_every_x_minutes} minute(s)\n")   

        a_cron_hours = '*'                                                  # Hours place in crontab format (activation)
        a_cron_minutes = '*'                                                # Minutes place in crontab format (activation)

        a_hour, a_minute = self.minutesToHours(activate_every_x_minutes)    # Time in hours:minutes between each activation
        print(f"{a_hour} hours and {a_minute} minute(s)\n\n")

        if a_hour > 0:                                                      # Adjust hours and minutes places in crontab accordingly
            a_cron_hours = f'0-23/{a_hour}'
        a_cron_minutes = f'{a_minute}'

        a_cron_command = f'sudo {bash_location} {actuator.activate.path}'   # Command for cron to execute

        activate = self.cron.new(command=a_cron_command)                    # The cronjob object
        activate.setall(a_cron_minutes, a_cron_hours, None, None, None)     # The cronjob schedule

        # Same for deactivate with different calculations
        deactivate_every_x_minutes = activate_every_x_minutes + length

        d_cron_hours = '*'
        d_cron_minutes = '*'

        d_hour, d_minute = self.minutesToHours(deactivate_every_x_minutes)

        d_cron_hours = f'{d_hour}-23/{d_hour}'
        d_cron_minutes = f'{d_minute}'

        d_cron_command = f'sudo {bash_location} {actuator.deactivate.path}'

        deactivate = self.cron.new(command=d_cron_command)
        deactivate.setall(d_cron_minutes, d_cron_hours, None, None, None)

        self.cron.write()


    def scheduleActuators(self, actuators: list):
    """Executes the 'scheduleActuator()' function for all actuators"""
        for act in actuators:
            self.scheduleActuator(act[0], act[1], act[2])
    

    def scheduleSensorLogging(self, sensor: Sensor, frequency: int):
    """Schedules a script that will log the information of the given sensor at the given frequency"""
        print(f"Sensor: {sensor.name}\n")
        if frequency <= 0:
            print("returning, frequency < = 0")
            return
        
        bash_location = '/bin/bash'
        log_every = 1440 / frequency
        print(f"Logs every: {log_every} minute(s)\n")
        cron_hours = '*'
        cron_minutes = '*'

        hours, minutes = self.minutesToHours(log_every)
        print(f"{hours} hours and {minutes} minute(s)\n\n")
        if hours > 0:
            cron_hours = f'0-23/{hours}'
        cron_minutes = f'{minutes}'

        cron_command = f'sudo {bash_location} {sensor.read.path}'
        read = self.cron.new(command=cron_command)
        read.setall(cron_minutes, cron_hours, None, None, None)

        self.cron.write()


    def scheduleSensors(self, sensors: list, frequency: int):
    """Executes the 'scheduleSensor()' function for all sensors"""
        for sen in sensors:
            self.scheduleSensorLogging(sen, frequency)


    def scheduleErrorChecks(self, frequency: int):
    """Schedules a script that will check for system errors at the given frequency"""
        check_every = 1440 / frequency
        cron_hours = '*'
        cron_minutes = '*'

        hours, minutes = self.minutesToHours(check_every)

        if hours > 0:
            cron_hours = f'0-23/{hours}'
        cron_minutes = f'{minutes}'

        cron_command = f'sudo python3 {os.getcwd()}/scripts/error_check.py'
        error_check = self.cron.new(command=cron_command)
        error_check.setall(cron_minutes, cron_hours, None, None, None)

        self.cron.write()


    def deleteAllJobs(self):
    """Removes all active cron jobs"""
        for job in self.cron:
            print(job)
        self.cron.remove_all()
        self.cron.write()

        for act in self.active_actuators:
            act.deactivate.execute()
            self.active_actuators.remove(act)

    def listAllJobs(self):
    """Lists (prints) all active cron jobs"""
        for job in self.cron:
            print(job)