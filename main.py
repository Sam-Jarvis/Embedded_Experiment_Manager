import Scheduler
import Config

c = Config.Config("config.cfg")
c.parse()

s = Scheduler.Scheduler()
#for act in c.getActuators():
#    print(f"Name: {act[0].name}, freq: {act[1]}, Len: {act[2]}, Inte: {act[3]}")
#    s.scheduleActuator(act[0], act[1], act[2])
# c.getActuators()[0][0].deactivate.execute()
s.listAllJobs()
