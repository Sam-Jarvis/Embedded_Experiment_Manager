import Scheduler
import Config

def main(config_path):
    c = Config.Config(config_path)
    s = Scheduler.Scheduler()

    s.deleteAllJobs()
    c.parse()

    log_frequency = c.getSensorLogFrequency()
    error_check_frequency = c.getErrorCheckFrequency()
    experiment_duration = c.getExperimentDuration()

    actuators = c.getActuators()
    sensors = c.getSensors()

    s.scheduleActuators(actuators)
    s.scheduleSensors(sensors, log_frequency)
    s.scheduleErrorChecks(error_check_frequency)

    s.listAllJobs()
    s.scheduleDemise(experiment_duration)

if __name__ == "__main__":
    main("config.cfg")

