#!/usr/bin/env python3
"""
Test serwa z biblioteką pigpio
GPIO18 (Pin 12)
"""

import pigpio
from time import sleep

print("🔧 Test Serwa - pigpio")
print("=" * 50)

# Połącz z pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    print("❌ Nie można połączyć z pigpio daemon")
    print("Uruchom: sudo systemctl start pigpiod")
    exit(1)

print("✅ Połączono z pigpio daemon")

# GPIO18 (Pin 12)
SERVO_PIN = 18

# Ustaw GPIO18 jako wyjście PWM
pi.set_mode(SERVO_PIN, pigpio.OUTPUT)


def set_servo_angle(angle):
    """
    Ustaw kąt serwa (-90 do +90 stopni)
    """
    # Konwersja kąta na pulse width (500-2500 us)
    # -90° = 500us, 0° = 1500us, +90° = 2500us
    pulse_width = 1500 + (angle * 1000 / 90)
    pulse_width = int(max(500, min(2500, pulse_width)))

    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
    return pulse_width


try:
    print("\n🚀 Rozpoczynam test...\n")

    # Test 1: Środek (0°)
    print("📍 Test 1: Pozycja środkowa (0°)")
    set_servo_angle(0)
    sleep(2)

    # Test 2: Prawo (+90°)
    print("📍 Test 2: Pozycja prawa (+90°)")
    set_servo_angle(90)
    sleep(2)

    # Test 3: Środek
    print("📍 Test 3: Powrót do środka (0°)")
    set_servo_angle(0)
    sleep(2)

    # Test 4: Lewo (-90°)
    print("📍 Test 4: Pozycja lewa (-90°)")
    set_servo_angle(-90)
    sleep(2)

    # Test 5: Środek
    print("📍 Test 5: Powrót do środka (0°)")
    set_servo_angle(0)
    sleep(2)

    # Test 6: Pozycje pośrednie
    print("\n📍 Test 6: Pozycje pośrednie...")
    for angle in [-90, -45, 0, 45, 90]:
        print(f"   Kąt: {angle:+3d}°")
        set_servo_angle(angle)
        sleep(1)

    # Test 7: Płynny ruch
    print("\n📍 Test 7: Płynny ruch lewo → prawo")
    for angle in range(-90, 91, 5):
        set_servo_angle(angle)
        sleep(0.05)

    print("📍 Test 8: Płynny ruch prawo → lewo")
    for angle in range(90, -91, -5):
        set_servo_angle(angle)
        sleep(0.05)

    # Powrót do środka
    print("\n📍 Powrót do pozycji środkowej")
    set_servo_angle(0)
    sleep(1)

    # Wyłącz PWM (serwo przestanie trzymać)
    pi.set_servo_pulsewidth(SERVO_PIN, 0)

    print("\n" + "=" * 50)
    print("✅ Test zakończony pomyślnie!")
    print("=" * 50)

except KeyboardInterrupt:
    print("\n⚠️  Test przerwany")

finally:
    # Wyłącz PWM
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    # Rozłącz pigpio
    pi.stop()
    print("\n👋 Program zakończony")
