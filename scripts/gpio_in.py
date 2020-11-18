from datetime import datetime
import board
import adafruit_dht
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

dhtDevice = adafruit_dht.DHT11(board.D22)

read_attempts = 0
 
while True:
    try:
        temp = dhtDevice.temperature
        humidity = dhtDevice.humidity
        with open(log_file, "a") as log:
            log.write(f"{name},{pin},{temp},{humidity},{str(datetime.now())}\n")
        break
 
    except RuntimeError as error:
        read_attempts += 1
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error