from crontab import CronTab

class Scheduler:
    """Responsible for all cron job and time related tasks"""

    # All actuators that have cron jobs attached to them
    active_actuators = []

    def __init__(self):
        self.cron = CronTab(user='root')

    def minutesToHours(self, minutes):
        hours = int(minutes / 60)
        minutes = int(minutes % 60)
        return (hours, minutes)

    # TODO: frequency can be 0 or -1. Handle. 
    def scheduleActuator(self, actuator, frequency, length):
        if frequency <= 0:
            return
        print(f"Frequency: {frequency}")
        bash_location = '/bin/bash'

        # keep track of this actuator (it will have a cron job attached to it)
        if actuator not in self.active_actuators:
            self.active_actuators.append(actuator)

        # How often to activate (in minutes)
        activate_every_x_minutes = 1440 / frequency
        print(f"Every: {activate_every_x_minutes} minutes")

        # Hours and minutes section of the crontab file
        a_cron_hours = '*'
        a_cron_minutes = '*'

        # How often to activate in terms of hours and minutes
        a_hour, a_minute = self.minutesToHours(activate_every_x_minutes)
        print(f"{a_hour} hours; {a_minute} minutes")

        # Set crontab hour and minute sections 
        if a_hour > 0:
            a_cron_hours = f'0-23/{a_hour}'
        a_cron_minutes = f'{a_minute}'

        print(a_cron_hours)
        print(a_cron_minutes)

        # Command for cron to execute
        a_cron_command = f'sudo {bash_location} {actuator.activate.path}'

        # The cron job
        activate = self.cron.new(command=a_cron_command)
        activate.setall(a_cron_minutes, a_cron_hours, None, None, None)

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
        for act in actuators:
            self.scheduleActuator(act[0], act[1], act[2])
        

    def deleteAllJobs(self):
        for job in self.cron:
            print(job)
        self.cron.remove_all()
        self.cron.write()

        for act in self.active_actuators:
            act.deactivate.execute()
            self.active_actuators.remove(act)

    def listAllJobs(self):
        for job in self.cron:
            print(job)