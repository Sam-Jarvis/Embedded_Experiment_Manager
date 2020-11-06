import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

pwm18 = GPIO.PWM(18, 0.8)
pwm18.start(90)
time.sleep(3)
pwm18.stop()
GPIO.cleanup()