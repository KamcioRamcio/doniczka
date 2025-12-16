#!/usr/bin/env python3
"""Test wyświetlacza LCD 1602 I2C"""

from RPLCD.i2c import CharLCD
import time

lcd = CharLCD('PCF8574', 0x27, port=1, charmap='A00',
              cols=16, rows=2, dotsize=8,
              auto_linebreaks=True,
              backlight_enabled=True)

try:
    lcd.clear()
    lcd.write_string('sigma')
    time.sleep(10)
    lcd.clear()
    lcd.write_string('Test OK!')
    time.sleep(2)

except KeyboardInterrupt:
    lcd.clear()
    lcd.close()

except Exception as e:
    pass
