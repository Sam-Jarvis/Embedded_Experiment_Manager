from crontab import CronTab

cron = CronTab(user='root')
cron.remove_all()
cron.write()

with open("/home/ubuntu/all_jobs_removed.txt", "a") as removed:
    for job in cron:
        removed.write(job)