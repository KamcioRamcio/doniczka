#!/usr/bin/env python3
"""
Test pompy - dla przekaźnika Active LOW
GPIO17 (Pin 11)
"""

from gpiozero import OutputDevice
from time import sleep
import sys

print("=" * 60)
print("💧 TEST POMPY - Active LOW")
print("=" * 60)

# active_high=False - dla przekaźnika Active LOW
# initial_value=False - start z przekaźnikiem OFF (GPIO HIGH)
relay = OutputDevice(17, active_high=False, initial_value=False)

print("\n✅ Przekaźnik zainicjalizowany (Active LOW)")
print("✅ Stan początkowy: OFF (GPIO HIGH)")
print("⚠️  Sprawdź czy pompa jest w wodzie!")
print("\n" + "=" * 60)

confirm = input("\nCzy pompa jest w wodzie? (tak/nie): ").strip().lower()

if confirm not in ['tak', 't', 'yes', 'y']:
    print("\n❌ Test anulowany.")
    relay.close()
    sys.exit(0)

print("\n🚀 Test za 3 sekundy...")
for i in range(3, 0, -1):
    print(f"   {i}...")
    sleep(1)

try:
    print("\n" + "=" * 60)
    print("✅ PRZEKAŹNIK ON (GPIO LOW) - POMPA WŁĄCZONA!")
    print("=" * 60)

    relay.on()  # GPIO LOW → Przekaźnik ON
    print("   Pompowanie przez 1 sekundę...")
    sleep(1)

    relay.off()  # GPIO HIGH → Przekaźnik OFF

    print("\n" + "=" * 60)
    print("❌ PRZEKAŹNIK OFF (GPIO HIGH) - POMPA WYŁĄCZONA")
    print("=" * 60)

    print("\n✅ Test zakończony pomyślnie!")

except KeyboardInterrupt:
    print("\n\n⚠️  Przerwano (Ctrl+C)")
    relay.off()  # Wyłącz pompę

except Exception as e:
    print(f"\n❌ Błąd: {e}")
    relay.off()

finally:
    relay.close()
    print("\n👋 Program zakończony - GPIO zwolniony")
