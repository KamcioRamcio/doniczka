# LCD jest pod adresem 0x27

# !/usr/bin/env python3
"""
Prosty test wyświetlacza LCD 1602 I2C
Wyświetla napis "sigma"
"""

from RPLCD.i2c import CharLCD
import time

# Inicjalizacja LCD
# Zmień adres na 0x3F jeśli 0x27 nie działa
lcd = CharLCD('PCF8574', 0x27, port=1, charmap='A00',
              cols=16, rows=2, dotsize=8,
              auto_linebreaks=True,
              backlight_enabled=True)

try:
    # Wyczyść wyświetlacz
    lcd.clear()

    # Wyświetl "sigma" w pierwszej linii
    lcd.write_string('sigma')

    print("✅ Napis 'sigma' wyświetlony na LCD!")
    print("Naciśnij Ctrl+C aby zakończyć")

    # Pozostaw napis na 10 sekund
    time.sleep(10)

    # Wyczyść wyświetlacz
    lcd.clear()
    lcd.write_string('Test OK!')
    time.sleep(2)

except KeyboardInterrupt:
    print("\n👋 Program zakończony")
    lcd.clear()
    lcd.close()

except Exception as e:
    print(f"❌ Błąd: {e}")
    print("\nSprawdź:")
    print("  1. Czy LCD jest podłączony do I2C (Pin 3, 5)")
    print("  2. Czy adres to 0x27 lub 0x3F")
    print("  3. sudo i2cdetect -y 1")
