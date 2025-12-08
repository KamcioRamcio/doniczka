#!/usr/bin/env python3
"""
Raspberry Pi - Odczyt z Arduino UNO (czujnik wilgotności)
Komunikacja przez Serial USB
"""

import serial
import time

# Konfiguracja portu Serial
# Port może być /dev/ttyACM0 lub /dev/ttyUSB0
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
TIMEOUT = 1


def find_arduino_port():
    """Znajdź port Arduino automatycznie"""
    import os
    for port in ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyUSB0', '/dev/ttyUSB1']:
        if os.path.exists(port):
            return port
    return None


def parse_soil_data(line):
    """
    Parsuj dane z Arduino
    Format: SOIL:raw_value:percent
    Przykład: SOIL:654:45
    """
    try:
        if line.startswith('SOIL:'):
            parts = line.split(':')
            raw_value = int(parts[1])
            moisture_percent = int(parts[2])
            return {
                'raw': raw_value,
                'moisture': moisture_percent
            }
    except (IndexError, ValueError) as e:
        print(f"⚠️  Błąd parsowania: {line} - {e}")
    return None


def main():
    """Główna funkcja programu"""

    print("🔌 Łączenie z Arduino UNO...")

    # Znajdź port Arduino
    port = find_arduino_port()
    if not port:
        print("❌ Nie znaleziono Arduino!")
        print("Sprawdź:")
        print("  1. Czy Arduino jest podłączone przez USB")
        print("  2. ls /dev/tty*")
        return

    print(f"✅ Znaleziono Arduino na porcie: {port}")

    try:
        # Otwórz połączenie Serial
        ser = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Czekaj na inicjalizację Arduino

        # Wyczyść bufor
        ser.flushInput()

        print("\n📊 Odczyt danych z czujnika wilgotności")
        print("=" * 50)
        print("Naciśnij Ctrl+C aby zakończyć\n")

        while True:
            # Odczytaj linię z Serial
            if ser.in_waiting > 0:
                line = ser.readline()
                message = line[:-2]
                print(message)
                # Debug - pokaż surową linię
                # print(f"DEBUG: {line}")

                # Parsuj dane
                # data = parse_soil_data(line)
                #
                # if data:
                #     raw = data['raw']
                #     moisture = data['moisture']
                #
                #     # Wizualizacja wilgotności
                #     bar_length = int(moisture / 2)  # 50 znaków max
                #     bar = '█' * bar_length + '░' * (50 - bar_length)
                #
                #     # Ocena stanu
                #     if moisture < 30:
                #         status = "🔴 SUCHO - Podlej!"
                #     elif moisture < 60:
                #         status = "🟡 OK"
                #     else:
                #         status = "🟢 MOKRO"
                #
                #     # Wyświetl
                #     print(f"Raw: {raw:4d} | Wilgotność: {moisture:3d}% [{bar}] {status}")
                # else:
                #     # Inne wiadomości z Arduino
                #     if line and not line.startswith('SOIL:'):
                #         print(f"ℹ️  Arduino: {line}")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\n👋 Program zakończony")
        ser.close()

    except serial.SerialException as e:
        print(f"❌ Błąd Serial: {e}")

    except Exception as e:
        print(f"❌ Błąd: {e}")


if __name__ == "__main__":
    main()
