import RPi.GPIO as GPIO
from datetime import datetime
import time
import argparse

pin = int()
log_file = str()
name = str()

parser = argparse.ArgumentParser()
parser.add_argument('pin', help="pin number to activate", type=int)
parser.add_argument('logpath', help="path to actuator log file", type=str)
parser.add_argument('name', help="name to be stored in the log file", type=str)
args = parser.parse_args()

pin = args.pin
log_file = args.logpath
name = args.name

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)


with open(log_file, "a") as log:
    log.write(f"{name},{pin},{int(0)},{str(datetime.now())}\n")