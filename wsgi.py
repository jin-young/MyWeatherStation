import cherrypy
import time
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController
from app import Root
from app import Adafruit_BME680_PYFTDI
from lib.sht31d import SHT31D_FTDI

cherrypy.config.update({'engine.autoreload.on': False})
cherrypy.server.unsubscribe()
cherrypy.engine.start()

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
        raise "could not acquire device"


wsgiapp = cherrypy.tree.mount(Root(bme680, sht31d))
