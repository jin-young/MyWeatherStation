#!/usr/bin/env python
import time
import board
import busio
import adafruit_mcp9808
import adafruit_bme280
from Adafruit_LED_Backpack import SevenSegment

i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c_bus)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c_bus, 0x77)

while(True):
  print("MCP9808: ", mcp.temperature)
  print("BME280:  ", bme280.temperature)

  time.sleep(10)
