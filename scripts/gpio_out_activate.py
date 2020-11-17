import RPi.GPIO as GPIO
from datetime import datetime
import argparse
import os

# For Raspberry Pi A+, B+ and Pi2 models
valid_pins = [4, 17, 18, 27, 22, 23, 24, 9, 25, 8, 7, 5, 6, 13, 12, 19, 16, 20, 21, 26]

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

if pin in valid_pins:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

    with open(log_file, "a") as log:
        log.write(f"{name},{pin},{int(1)},{str(datetime.now())}\n")
