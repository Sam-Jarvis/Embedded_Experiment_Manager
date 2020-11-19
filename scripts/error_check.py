#!/usr/bin python3
import shutil
import smtplib

send_flag = False

server = "smtp.mailtrap.io"
port = 2525
login = "eec33d5833f9cf"
password = "99cdcbca36a5b9"
sender = "Private Person <from@example.com>"                    
receiver = "A Test User <to@example.com>"

storage_limit = 85.0
temperature_limit = 75.0

disk_space = shutil.disk_usage("/")
disk_space_percent = (disk_space[1]/disk_space[2]) * 100
temperature = 0.0

print(f"Storage: {disk_space_percent}")

with open('/sys/class/thermal/thermal_zone0/temp') as f:
    line = f.readline().strip()
    if line.isdigit():
        temperature = float(line) / 1000

print(f"temperature: {temperature}")

temperature_warning = f"""\
Subject: Experiment Temperature Warning!
To: {receiver}
From: {sender}

The temperature limit of the Raspberry pi is {temperature_limit} degrees celcius.
The temperature of the Raspberry Pi is {temperature}
Consider moving the system out of direct sunlight or to a cooler location."""

storage_warning = f"""\
Subject: Experiment Storage Warning!
To: {receiver}
From: {sender}

The storage limit (used storage space as a percentage) is {storage_limit}%.
The Raspberry Pi is currently using {disk_space_percent}% of it's storage.
Consider exporting the log files to free up space."""

both = f"""\
Subject: Experiment Storage and Temperature Warning!
To: {receiver}
From: {sender}

The temperature limit of the Raspberry pi is {temperature_limit} degrees celcius.
The temperature of the Raspberry Pi is {temperature}
Consider moving the system out of direct sunlight or to a cooler location.

The storage limit (used storage space as a percentage) is {storage_limit}%.
The Raspberry Pi is currently using {disk_space_percent}% of it's storage.
Consider exporting the log files to free up space."""

if temperature >= temperature_limit and disk_space_percent >= storage_limit:
    send_flag = True
    message = both

elif temperature >= temperature_limit:
    send_flag = True
    message = temperature_warning

elif disk_space_percent >= storage_limit:
    send_flag = True
    message = storage_warning

if send_flag:
    with smtplib.SMTP(server, port) as server:
        server.login(login, password)
        server.sendmail(sender, receiver, message)
        print(message)