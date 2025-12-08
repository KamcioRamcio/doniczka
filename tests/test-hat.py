# 0x29 - TSL25911 (światło)
# 0x53 - LTR390 (UV)
# 0x68 - ICM20948 (akceleromet r /żyroskop)
# 0x76 - BME280 (tem p /wilgotnoś ć /ciśnienie)

# !/usr/bin/env python3
"""
Podstawowy program testowy dla Waveshare Environment Sensor HAT
Odczyt wszystkich czujników
"""

import time
import board
import busio

# Biblioteki czujników
try:
    import adafruit_bme280.advanced as adafruit_bme280

    bme280_available = True
except ImportError:
    print("⚠️  BME280 library not installed")
    bme280_available = False

try:
    from adafruit_tsl2591 import TSL2591

    tsl2591_available = True
except ImportError:
    print("⚠️  TSL2591 library not installed")
    tsl2591_available = False

try:
    from adafruit_icm20x import ICM20948

    icm20948_available = True
except ImportError:
    print("⚠️  ICM20948 library not installed")
    icm20948_available = False

try:
    import adafruit_ltr390

    ltr390_available = True
except ImportError:
    print("⚠️  LTR390 library not installed")
    ltr390_available = False


def init_sensors():
    """Inicjalizacja wszystkich czujników"""

    print("🔧 Inicjalizacja magistrali I2C...")
    i2c = board.I2C()  # uses board.SCL and board.SDA

    sensors = {}

    # BME280 - Temperatura, Wilgotność, Ciśnienie
    if bme280_available:
        try:
            sensors['bme280'] = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
            # Konfiguracja - tryb normalny
            sensors['bme280'].mode = adafruit_bme280.MODE_NORMAL
            sensors['bme280'].standby_period = adafruit_bme280.STANDBY_TC_500
            sensors['bme280'].iir_filter = adafruit_bme280.IIR_FILTER_X16
            print("✅ BME280 (Temp/Humidity/Pressure) - OK")
        except Exception as e:
            print(f"❌ BME280 initialization failed: {e}")

    # TSL2591 - Światło (Lux)
    if tsl2591_available:
        try:
            sensors['tsl2591'] = TSL2591(i2c)
            print("✅ TSL2591 (Light sensor) - OK")
        except Exception as e:
            print(f"❌ TSL2591 initialization failed: {e}")

    # ICM20948 - Akcelerometr + Żyroskop + Magnetometr
    if icm20948_available:
        try:
            sensors['icm20948'] = ICM20948(i2c, address=0x68)
            print("✅ ICM20948 (Accelerometer/Gyro/Magnetometer) - OK")
        except Exception as e:
            print(f"❌ ICM20948 initialization failed: {e}")

    # LTR390 - UV (promieniowanie UV)
    if ltr390_available:
        try:
            sensors['ltr390'] = adafruit_ltr390.LTR390(i2c, address=0x53)
            print("✅ LTR390 (UV sensor) - OK")
        except Exception as e:
            print(f"❌ LTR390 initialization failed: {e}")

    return sensors


def read_bme280(sensor):
    """Odczyt BME280 - Temperatura, Wilgotność, Ciśnienie"""
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        pressure = sensor.pressure

        return {
            'temperature': round(temp, 2),
            'humidity': round(humidity, 2),
            'pressure': round(pressure, 2)
        }
    except Exception as e:
        print(f"❌ BME280 read error: {e}")
        return None


def read_tsl2591(sensor):
    """Odczyt TSL2591 - Światło (Lux)"""
    try:
        lux = sensor.lux
        infrared = sensor.infrared
        visible = sensor.visible

        return {
            'lux': round(lux, 2) if lux is not None else 0,
            'infrared': infrared,
            'visible': visible
        }
    except Exception as e:
        print(f"❌ TSL2591 read error: {e}")
        return None


def read_icm20948(sensor):
    """Odczyt ICM20948 - Akcelerometr, Żyroskop, Magnetometr"""
    try:
        accel_x, accel_y, accel_z = sensor.acceleration
        gyro_x, gyro_y, gyro_z = sensor.gyro
        mag_x, mag_y, mag_z = sensor.magnetic

        return {
            'acceleration': {
                'x': round(accel_x, 2),
                'y': round(accel_y, 2),
                'z': round(accel_z, 2)
            },
            'gyro': {
                'x': round(gyro_x, 2),
                'y': round(gyro_y, 2),
                'z': round(gyro_z, 2)
            },
            'magnetic': {
                'x': round(mag_x, 2),
                'y': round(mag_y, 2),
                'z': round(mag_z, 2)
            }
        }
    except Exception as e:
        print(f"❌ ICM20948 read error: {e}")
        return None


def read_ltr390(sensor):
    """Odczyt LTR390 - UV"""
    try:
        uv = sensor.uvs
        light = sensor.light
        uvi = sensor.uvi

        return {
            'uv': uv,
            'light': light,
            'uvi': round(uvi, 2) if uvi is not None else 0
        }
    except Exception as e:
        print(f"❌ LTR390 read error: {e}")
        return None


def print_readings(sensors):
    """Wyświetl odczyty wszystkich czujników"""

    print("\n" + "=" * 60)
    print("📊 ODCZYTY CZUJNIKÓW")
    print("=" * 60)

    # BME280
    if 'bme280' in sensors:
        data = read_bme280(sensors['bme280'])
        if data:
            print(f"\n🌡️  BME280 (Środowisko):")
            print(f"   Temperatura:  {data['temperature']} °C")
            print(f"   Wilgotność:   {data['humidity']} %")
            print(f"   Ciśnienie:    {data['pressure']} hPa")

    # TSL2591
    if 'tsl2591' in sensors:
        data = read_tsl2591(sensors['tsl2591'])
        if data:
            print(f"\n💡 TSL2591 (Światło):")
            print(f"   Natężenie:    {data['lux']} lux")
            print(f"   Infrared:     {data['infrared']}")
            print(f"   Visible:      {data['visible']}")

    # ICM20948
    if 'icm20948' in sensors:
        data = read_icm20948(sensors['icm20948'])
        if data:
            print(f"\n📐 ICM20948 (Ruch):")
            print(f"   Acceleration: X={data['acceleration']['x']} "
                  f"Y={data['acceleration']['y']} Z={data['acceleration']['z']} m/s²")
            print(f"   Gyro:         X={data['gyro']['x']} "
                  f"Y={data['gyro']['y']} Z={data['gyro']['z']} °/s")
            print(f"   Magnetic:     X={data['magnetic']['x']} "
                  f"Y={data['magnetic']['y']} Z={data['magnetic']['z']} µT")

    # LTR390
    if 'ltr390' in sensors:
        data = read_ltr390(sensors['ltr390'])
        if data:
            print(f"\n☀️  LTR390 (UV):")
            print(f"   UV:           {data['uv']}")
            print(f"   Light:        {data['light']}")
            print(f"   UV Index:     {data['uvi']}")

    print("\n" + "=" * 60)


def main():
    """Główna funkcja programu"""

    print("🚀 Waveshare Environment Sensor HAT - Test")
    print("=" * 60)

    # Inicjalizacja czujników
    sensors = init_sensors()

    if not sensors:
        print("\n❌ Nie znaleziono żadnych czujników!")
        print("Sprawdź:")
        print("  1. Czy HAT jest poprawnie zamontowany")
        print("  2. Czy I2C jest włączony (sudo raspi-config)")
        print("  3. Czy biblioteki są zainstalowane")
        return

    print(f"\n✅ Znaleziono {len(sensors)} czujników")
    print("\nNaciśnij Ctrl+C aby zakończyć\n")

    try:
        while True:
            print_readings(sensors)
            time.sleep(2)  # Odczyt co 2 sekundy

    except KeyboardInterrupt:
        print("\n\n👋 Program zakończony przez użytkownika")


if __name__ == "__main__":
    main()
