from crontab import CronTab

cron = CronTab(user='root')
job = cron.new(command='python3 /home/ubuntu/gpio_cron.py')
job.minute.every(1)

cron.write()