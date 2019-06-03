import sys
import time
import sqlite3
import contextlib
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController

from os import path
root_dir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(root_dir)

from lib.sht31d import SHT31D_FTDI
from lib.bme680 import Adafruit_BME680_PYFTDI

bme680 = None
sht31d = None

for i in range(0,3):
    try:
        i2c = I2cController()
        i2c.configure('ftdi://ftdi:232h/1')

        bme680 = Adafruit_BME680_PYFTDI(i2c)
        sht31d = SHT31D_FTDI(i2c)
        break
    except Exception:
        if i < 3:
            print("could not acquire device. Retry")
            time.sleep(1)
            continue
        raise "could not acquire device due to error"

if bme680 is None or sht31d is None:
    raise "could not acquire device"
    
insert_sql = "INSERT INTO weather (temperature, humidity, pressure) VALUES (?, ?, ?);"

while True:
    temp = (bme680.temperature + sht31d.temperature)/2
    humi = (bme680.humidity + sht31d.relative_humidity)/2
    press = bme680.pressure
    print("============================================")
    print("Temperature: %0.2f C" % temp)
    print("Humidity: %0.2f %%" % humi)
    print("Pressure: %0.2f hPa\n" % press)

    with contextlib.closing(sqlite3.connect(root_dir + '/db/weather.db')) as conn:
        with conn as cur:
            cur.execute(insert_sql, (temp, humi, press))
            
    time.sleep(30)