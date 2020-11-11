import Scheduler
import Config

c = Config.Config("config.cfg")
c.parse()

print(c.getActuators()[0][0].toString())
# c.print_actuators()
# c.print_sensors()

# print(c.minutesToHours(576))

