import time
import board
import busio
import adafruit_mcp9808
from Adafruit_LED_Backpack import SevenSegment

i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c_bus)


segment = SevenSegment.SevenSegment(address=0x70)

# Initialize the display. Must be called once before using the display.
segment.begin()

while(True):
  segment.clear()

  temp = mcp.temperature

  segment.print_float(temp, 1, False)
  segment.set_digit(3, 'C', False)        # Ones

  # Write the display buffer to the hardware.  This must be called to
  # update the actual display LEDs.
  segment.write_display()

  # Wait a quarter second (less than 1 second to prevent colon blinking getting$
  time.sleep(10)
