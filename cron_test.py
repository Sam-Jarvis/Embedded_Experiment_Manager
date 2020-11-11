from crontab import CronTab

cron = CronTab(user='root')
job = cron.new(command='python3 /home/ubuntu/example1.py')
job.setall(10, '*/2', None, None, None)

cron.write()