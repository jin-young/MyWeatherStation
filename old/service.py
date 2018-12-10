#!/usr/bin/python3
import cherrypy
import time
import board
import busio
import adafruit_mcp9808
import adafruit_bme280
import math

i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c_bus)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c_bus, 0x76)

class MyWStation(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def current(self, q="90404", APPID="APPID"):
        return {
            "temperature": mcp.temperature,
            "pressure": bme280.pressure,
            "humidity": bme280.humidity,
            "wind": {
                "speed": 1.06,
                "deg": 17.0003
            },
            "dt": int(time.time())
        }

if __name__ == '__main__': 
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        cherrypy.quickstart(MyWStation())
