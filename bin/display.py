#!/usr/bin/env python
import time
import board
import busio
import psycopg2
from os import path
import contextlib
import datetime

from Adafruit_LED_Backpack import SevenSegment

root_dir = path.dirname(path.dirname(path.abspath(__file__)))

segment = SevenSegment.SevenSegment(address=0x70)
# Initialize the display. Must be called once before using the display.
segment.begin()

while(True):
    segment.clear()
    segment.set_brightness(1)
    conn = None
    try:
        conn = psycopg2.connect(host="localhost",database="weather", user="pi", password="...")
        cur = conn.cursor()
        cur.execute('SELECT t_sht31d, created_at FROM weather ORDER BY id DESC limit 1')
        record = cur.fetchone()
        
        temp = record[0]
        record_time = record[1]
        t_diff = datetime.datetime.now().timestamp() - record_time.timestamp()

        if (t_diff > 30):
            segment.print_hex(0xFFFF)
        else:
            segment.print_float(temp, 1, False)
            segment.set_digit(3, 'C', False)        # Ones
        
        # Write the display buffer to the hardware.  This must be called to
        # update the actual display LEDs.
        segment.write_display()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    # Wait a quarter second (less than 1 second to prevent colon blinking getting$
    time.sleep(10)
  
