import RPi.GPIO as GPIO
import time
import argparse

# For Raspberry Pi A+, B+ and Pi2 models
valid_pins = [4, 17, 18, 27, 22, 23, 24, 9, 25, 8, 7, 5, 6, 13, 12, 19, 16, 20, 21, 26]

pin = int()

parser = argparse.ArgumentParser()
parser.add_argument('pin', help="pin number to activate", type=int)
args = parser.parse_args()
pin = args.pin

if pin in valid_pins:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()