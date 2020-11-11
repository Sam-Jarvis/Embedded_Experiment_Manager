import getpass

import Config
#import configparser

c = Config.Config("config.cfg")
system_user = getpass.getuser()
c.parse()

# c.print_actuators()
# c.print_sensors()

print(c.minutesToHours(576))

test = c.generateScript(user=system_user, act_name="test", script_type=True, pin=18)
print(test)