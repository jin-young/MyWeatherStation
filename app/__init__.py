import cherrypy
import time
import board
import busio
import math

from adafruit_bme680 import Adafruit_BME680


class Adafruit_BME680_PYFTDI(Adafruit_BME680):
    """Driver for I2C connected BME680 via FT232H. Powered by PyFtdi.
        :param i2c pyftdi I2cController
        :param int address: I2C device address
        :param bool debug: Print debug statements when True.
        :param int refresh_rate: Maximum number of readings per second. Faster property reads
          will be from the previous reading."""
    def __init__(self, i2c, address=0x77, debug=False, *, refresh_rate=10):
        self._i2c = i2c.get_port(address)
        self._debug = debug
        self._addr = address
        super().__init__(refresh_rate=refresh_rate)

    def _read(self, register, length):
        """Returns an array of 'length' bytes from the 'register'"""
        value = self._i2c.read_from(register, length)
        if self._debug:
            print("\t$%02X => %s" % (register, value))
        return value

    def _write(self, register, values):
        """Writes an array of 'length' bytes to the 'register'"""
        self._i2c.write_to(register, values)


class Root(object):
    def __init__(self, sensor, sensor2):
        self._sensor = sensor
        self._sensor2 = sensor2

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {
            "temperature": (self._sensor.temperature + self._sensor2.temperature)/2,
            "pressure": self._sensor.pressure,
            "humidity": (self._sensor.humidity + self._sensor2.relative_humidity)/2,
            "wind": {
                "speed": 1.06,
                "deg": 17.0003
            },
            "dt": int(time.time())
        }

