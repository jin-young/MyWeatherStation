#!/usr/bin/env python
import board
import busio
from Adafruit_LED_Backpack import SevenSegment

i2c_bus = busio.I2C(board.SCL, board.SDA)

segment = SevenSegment.SevenSegment(address=0x70)
segment.begin()
segment.clear()
segment.write_display()
