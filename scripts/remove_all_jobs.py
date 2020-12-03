from crontab import CronTab

cron = CronTab(user='root')

cron.remove_all()
cron.write()
