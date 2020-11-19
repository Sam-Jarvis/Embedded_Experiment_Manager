from datetime import datetime
import board
import adafruit_dht
import argparse 

pin = int()
log_file = str()
name = str()

parser = argparse.ArgumentParser()
parser.add_argument('pin', type=int)
parser.add_argument('logpath', type=str)
parser.add_argument('name', type=str)
args = parser.parse_args()

pin = args.pin
log_file = args.logpath
name = args.name

dhtDevice = adafruit_dht.DHT11(board.D22)

read_attempts = 1
 
while True:
    try:
        temp = dhtDevice.temperature
        humidity = dhtDevice.humidity
        with open(log_file, "a") as log:
            log.write(f"{name},{pin},{temp},{humidity},{str(datetime.now())},{read_attempts}\n")
        break
 
    except RuntimeError as error:
        read_attempts += 1
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error