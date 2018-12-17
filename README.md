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
}
```

Note that temperature is read from MCP9808 because my BME280 showed a bit higher than actual temperature.
