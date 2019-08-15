#!/usr/bin/env python
import time
import board
import busio
import sqlite3
from os import path
import contextlib

from Adafruit_LED_Backpack import SevenSegment

root_dir = path.dirname(path.dirname(path.abspath(__file__)))

segment = SevenSegment.SevenSegment(address=0x70)
# Initialize the display. Must be called once before using the display.
segment.begin()

while(True):
  segment.clear()
  
  with contextlib.closing(sqlite3.connect(root_dir + '/db/weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)) as conn:
    cur = conn.cursor()
    cur.execute('SELECT temperature FROM weather ORDER BY id DESC limit 1')
    record = cur.fetchone()
    
    temp = record[0]

    segment.print_float(temp, 1, False)
    segment.set_digit(3, 'C', False)        # Ones

    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    segment.write_display()

  # Wait a quarter second (less than 1 second to prevent colon blinking getting$
  time.sleep(10)
