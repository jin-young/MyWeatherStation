import sys
import time
import psycopg2
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
    
insert_sql = "INSERT INTO weather (t_bme680, t_sht31d, h_bme680, h_sht31d, pressure) VALUES (%s, %s, %s, %s, %s);"

bme680.humidity_oversample = 16

while True:
    t_680 = bme680.temperature
    t_31d = sht31d.temperature
    delta = t_680 - t_31d
    temp = (t_680 + t_31d)/2
    h_680 = bme680.humidity
    h_31d = sht31d.relative_humidity
    humi = (h_680 + h_31d)/2
    press = bme680.pressure
    print("============================================")
    print("Temperature BEM680: %0.2f C" % t_680)
    print("Temperature STD31H: %0.2f C" % t_31d)
    print("Temperature: %0.2f C" % temp)
    print("Humidity BME680: %0.2f %%" % h_680)
    print("Humidity STD31H: %0.2f %%" % h_31d)
    print("Humidity: %0.2f %%" % humi)
    print("Pressure: %0.2f hPa" % press)
    print("Delta: %0.2f C\n" % delta)

    try:
        conn = psycopg2.connect(host="localhost",database="weather", user="pi", password="...")
        cur = conn.cursor()
        cur.execute(insert_sql, (t_680, t_31d, h_680, h_31d, press))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
    sht31d.heater = True
    time.sleep(1)
    sht31d.heater = False
    time.sleep(9)
