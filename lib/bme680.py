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