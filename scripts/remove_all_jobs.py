from crontab import CronTab

cron = CronTab(user='root')

with open("/home/ubuntu/all_jobs_removed.txt", "a") as removed:
    for job in cron:
        removed.write(f"REMOVED: {job}")

cron.remove_all()
cron.write()
