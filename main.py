import Scheduler
import Config

c = Config.Config("config.cfg")
s = Scheduler.Scheduler()

c.parse()

log_frequency = c.getSensorLogFrequency()
error_check_frequency = c.getErrorCheckFrequency()

actuators = c.getActuators()
sensors = c.getSensors()

# s.scheduleActuators(actuators)
# s.scheduleSensors(sensors, log_frequency)
s.scheduleErrorChecks(error_check_frequency)
s.listAllJobs()
