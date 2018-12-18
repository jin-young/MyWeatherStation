# MyWeatherStation

Simple Python web service which provides temperature/humidity/pressure from BME280 and MCP9808 sensors.

This is very very personal project using 
* Raspberry Pi 3 powered by Ubuntu Mate
* BME280 Temperature/Humidity/Pressure sensor
* MCP9808 Temperature sensor
* (optional) Adafruit 0.56" 4-Digit 7-Segment Display w/I2C Backpack - Red
* Python3 and CherryPy

The service provides environment data as JSON format
```
{
    temperature: 22.375,  # Celsius (°C)
    dt: 1545021923,       # Unix Epoch timestamp  
    wind: {               # Hardcoded value. Just for future improvement
        speed: 1.06,
        deg: 17.0003,
    },
    pressure: 1015.4940735556579,  # Hectopascal (hPa)
    humidity: 53.36025163466593,   # percentage (%)
    delta: 0.78999   # temp from bme280 - temp from mcp9808
}
```

Note:
* temperature is read from MCP9808 because my BME280 showed a bit higher than actual temperature
* Code assumes that I2C address of BME280 is 0x77
* Code assumes that all sensors are connected via I2C
* To display current temperature on 7-segment display, the LED and controller should be connected via I2C
  * run ```bin/display.py```
  * temperature is updated every 15 seconds
