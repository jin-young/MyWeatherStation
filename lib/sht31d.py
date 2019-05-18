import time

try:
    import struct
except ImportError:
    import ustruct as struct
    
from micropython import const

SHT31_DEFAULT_ADDR = const(0x44)
SHT31_MEAS_HIGHREP_STRETCH = const(0x2C06)
SHT31_MEAS_MEDREP_STRETCH = const(0x2C0D)
SHT31_MEAS_LOWREP_STRETCH = const(0x2C10)
SHT31_MEAS_HIGHREP = const(0x2400)
SHT31_MEAS_MEDREP = const(0x240B)
SHT31_MEAS_LOWREP = const(0x2416)
SHT31_READSTATUS = const(0xF32D)
SHT31_CLEARSTATUS = const(0x3041)
SHT31_SOFTRESET = const(0x30A2)
SHT31_HEATEREN = const(0x306D)
SHT31_HEATERDIS = const(0x3066)

def _crc(data):
    crc = 0xff
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc <<= 1
                crc ^= 0x131
            else:
                crc <<= 1
    return crc


class SHT31D_FTDI:
    """
    A driver for the SHT31-D temperature and humidity sensor.
    :param i2c_bus: The `busio.I2C` object to use. This is the only required parameter.
    :param int address: (optional) The I2C address of the device.
    """
    def __init__(self, i2c_bus, address=SHT31_DEFAULT_ADDR):
        self._i2c = i2c_bus.get_port(address)
        self._command(SHT31_SOFTRESET)
        time.sleep(.010)

    def _command(self, command):
        self._i2c.write(struct.pack('>H', command))

    def _data(self):
        #data = bytearray(6)
        #data[0] = 0xff
        self._command(SHT31_MEAS_HIGHREP)
        time.sleep(.5)
        
        data = self._i2c.read(6)
        temperature, tcheck, humidity, hcheck = struct.unpack('>HBHB', data)
        if tcheck != _crc(data[:2]):
            raise RuntimeError("temperature CRC mismatch")
        if hcheck != _crc(data[3:5]):
            raise RuntimeError("humidity CRC mismatch")
        return temperature, humidity

    @property
    def temperature(self):
        """The measured relative humidity in percent."""
        raw_temperature, _ = self._data()
        return -45 + (175 * (raw_temperature / 65535))

    @property
    def relative_humidity(self):
        """The measured relative humidity in percent."""
        _, raw_humidity = self._data()
        return 100 * (raw_humidity / 65523)

    def reset(self):
        """Execute a Soft RESET of the sensor."""
        self._command(SHT31_SOFTRESET)
        time.sleep(.010)

    @property
    def heater(self):
        """Control the sensor internal heater."""
        return (self.status & 0x2000) != 0

    @heater.setter
    def heater(self, value=False):
        if value:
            self._command(SHT31_HEATEREN)
        else:
            self._command(SHT31_HEATERDIS)

    @property
    def status(self):
        """The Sensor status."""
        #data = bytearray(2)
        self._command(SHT31_READSTATUS)
        data = self._i2c.read(2)
        
        status = data[0] << 8 | data[1]
        return status
