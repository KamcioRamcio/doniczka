#!/usr/bin/env python3
import serial
import time
import sys

BAUD_RATE = 9600
TIMEOUT = 1


def find_arduino_port():
    import os
    for p in ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyUSB0', '/dev/ttyUSB1']:
        if os.path.exists(p):
            return p
    return None


def main():
    port = find_arduino_port()

    if not port:
        sys.exit(1)

    try:
        ser = serial.Serial(
            port=port,
            baudrate=BAUD_RATE,
            timeout=TIMEOUT,
            dsrdtr=True
        )

        time.sleep(3)

        ser.reset_input_buffer()

        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()

            if line:
                print(f"RAW: {line}")
            else:
                print(".", end="", flush=True)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()


if __name__ == "__main__":
    main()
