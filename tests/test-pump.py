#!/usr/bin/env python3
"""Test pompy - dla przekaźnika Active LOW na GPIO17"""

from gpiozero import OutputDevice
from time import sleep
import sys

relay = OutputDevice(17, active_high=False, initial_value=False)

confirm = input("Czy pompa jest w wodzie? (tak/nie): ").strip().lower()

if confirm not in ['tak', 't', 'yes', 'y']:
    relay.close()
    sys.exit(0)

try:
    relay.on()
    sleep(1)
    relay.off()

except KeyboardInterrupt:
    relay.off()

except Exception as e:
    relay.off()

finally:
    relay.close()
