import time
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController
from adafruit_bme680 import Adafruit_BME680

class Adafruit_BME680_PYFTDI(Adafruit_BME680):
    """Driver for I2C connected BME680 via FT232H. Powered by PyFtdi.
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
        #with self._i2c as i2c:
        #    i2c.write(bytes([register & 0xFF]))
        #    result = bytearray(length)
        #    i2c.readinto(result)
        #    if self._debug:
        #        print("\t$%02X => %s" % (register, [hex(i) for i in result]))
        #    return result
			
        #self._i2c.write(register & 0xFF]))
        value = self._i2c.read_from(register, length)
        if self._debug:
            print("\t$%02X => %s" % (register, value))
        return value

    def _write(self, register, values):
        """Writes an array of 'length' bytes to the 'register'"""
        #with self._i2c as i2c:
        #    buffer = bytearray(2 * len(values))
        #    for i, value in enumerate(values):
        #        buffer[2 * i] = register + i
        #        buffer[2 * i + 1] = value
        #    i2c.write(buffer)
        #    if self._debug:
        #        print("\t$%02X <= %s" % (values[0], [hex(i) for i in values[1:]]))
        self._i2c.write_to(register, values)

sensor = None

for i in range(0,2):
    try:
        i2c = I2cController()
        i2c.configure('ftdi://ftdi:232h/1')

        sensor = Adafruit_BME680_PYFTDI(i2c)
        break
    except Exception:
        if i < 2:
            print("could not acquire device. Retry")
            time.sleep(1)
            continue
        raise "could not acquire device"
        
print('Temperature: {} degrees C'.format(sensor.temperature))
print('Humidity: {}%'.format(sensor.humidity))
print('Pressure: {}hPa'.format(sensor.pressure))