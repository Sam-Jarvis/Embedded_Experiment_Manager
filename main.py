import Scheduler
import Config

c = Config.Config("config.cfg")
c.parse()

actuators = c.getActuators()

#c.generateScript(act_name = "test", script_tpe = True, pin = 27, log_file = "actuator.csv")

#c.print_sensors()
#c.print_actuators()
s = Scheduler.Scheduler()
s.scheduleActuators(actuators)
#s.deleteAllJobs()
s.listAllJobs()
