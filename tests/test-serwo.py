#!/usr/bin/env python3
"""Test serwa z biblioteką pigpio na GPIO18"""

import pigpio
from time import sleep

pi = pigpio.pi()

if not pi.connected:
    exit(1)

SERVO_PIN = 18

pi.set_mode(SERVO_PIN, pigpio.OUTPUT)


def set_servo_angle(angle):
    """Ustaw kąt serwa (-90 do +90 stopni)"""
    pulse_width = 1500 + (angle * 1000 / 90)
    pulse_width = int(max(500, min(2500, pulse_width)))

    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
    return pulse_width


try:
    set_servo_angle(0)
    sleep(2)

    set_servo_angle(90)
    sleep(2)

    set_servo_angle(0)
    sleep(2)

    set_servo_angle(-90)
    sleep(2)

    set_servo_angle(0)
    sleep(2)

    for angle in [-90, -45, 0, 45, 90]:
        set_servo_angle(angle)
        sleep(1)

    for angle in range(-90, 91, 5):
        set_servo_angle(angle)
        sleep(0.05)

    for angle in range(90, -91, -5):
        set_servo_angle(angle)
        sleep(0.05)

    set_servo_angle(0)
    sleep(1)

    pi.set_servo_pulsewidth(SERVO_PIN, 0)


except KeyboardInterrupt:
    print("\n⚠️  Test przerwany")

finally:
    # Wyłącz PWM
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    # Rozłącz pigpio
    pi.stop()
    print("\n👋 Program zakończony")
