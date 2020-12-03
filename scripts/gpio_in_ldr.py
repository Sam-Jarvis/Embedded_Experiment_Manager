import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin = 7

def read_light (pin):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1
        if count >= 100000:
            return 0

    return 1


#Catch when script is interrupted, cleanup correctly
try:
	print(read_light(pin))
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
