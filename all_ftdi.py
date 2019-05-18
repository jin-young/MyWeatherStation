import board
import busio
import time
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController
from lib.sht31d import SHT31D_FTDI
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

bme680 = None
sht31d = None

for i in range(0,3):
    try:
        i2c = I2cController()
        i2c.configure('ftdi://ftdi:232h/1')

        bme680 = Adafruit_BME680_PYFTDI(i2c)
        sht31d = SHT31D_FTDI(i2c)
        break
    except Exception as e:
        if i < 3:
            print("could not acquire device. Retry")
            print(e)
            time.sleep(1)
            continue
        raise "could not acquire device"
        
while True:
    print("SHT   : Temperature: %0.2f C" % sht31d.temperature)
    print("680   : Temperature: %0.2f C" % bme680.temperature)
    print("SHT   : Humidity: %0.2f %%" % sht31d.relative_humidity)
    print("680   : Humidity: %0.2f %%" % bme680.humidity)
    print("680   : Pressure: %0.2f hPascal" % bme680.pressure)

    time.sleep(5)
