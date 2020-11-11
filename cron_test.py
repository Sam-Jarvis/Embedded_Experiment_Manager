from crontab import CronTab

cron = CronTab(user='root')
job1 = cron.new(command='sudo /bin/bash /home/ubuntu/.gpio_scripts/heater_activate.sh')
job1.setall('0-59/1', None, None, None, None)

job2 = cron.new(command='sudo /bin/bash /home/ubuntu/.gpio_scripts/heater_deactivate.sh')
job2.setall('1-59/1', None, None, None, None)

for item in cron:
    print(item)

cron.write()