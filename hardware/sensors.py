# czujnik Waveshare HAT
import time

import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
from adafruit_tsl2591 import TSL2591
from adafruit_icm20x import ICM20948
import adafruit_ltr390
import serial
import asyncio
from datetime import datetime



class SensorHub:
    """Klasa do obsługi czujników na Waveshare Environment Sensor HAT"""

    def __init__(self, num_reads : int):
        self.num_reads = num_reads

        self.i2c = board.I2C()
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c, address=0x76)
        self.tsl2591 = TSL2591(self.i2c)
        self.ltr390 = adafruit_ltr390.LTR390(self.i2c, address=0x53)

        # temperatura
        self.temperatura = None
        self.pressure = None
        self.humidity = None

        self.light = None
        self.uvi = None

        self.moisture = None


        # arduino moisture
        self.serial_port = '/dev/ttyACM0'
        self.baud_rate = 9600
        self.timoute = 1
    async def read_data(self):
        bem = {
            'temperature': 0.0,
            'pressure': 0.0,
            'humidity': 0.0
        }

        light = []
        uv_list = []

        for i in range(self.num_reads):
            temperature = self.bme280.temperature
            bem['temperature'] += temperature

            pressure = self.bme280.pressure
            bem['pressure'] += pressure

            humidity = self.bme280.humidity
            bem['humidity'] += humidity

            lux = self.tsl2591.lux
            light.append(lux)

            uv = self.ltr390.uvi
            uv_list.append(uv)

            await asyncio.sleep(0.9)

        self.temperatura = round(bem['temperature'] / self.num_reads, 2)
        self.pressure =  round(bem['pressure'] / self.num_reads, 2)
        self.humidity =  round(bem['humidity'] / self.num_reads, 2)

        self.light = round(sum(light) / self.num_reads, 2)

        self.uvi = round(sum(uv_list) / self.num_reads, 2)

        # print(f'temperatura : {self.temperatura}, cisnienie {self.pressure}, wilgotnosc {self.humidity}')
        # print(f'światlo lux {self.light}')
        # print(f'indeks uv {self.uvi}')
        return self.temperatura

    async def read_arduino(self):
        """Robust read from Arduino: waits for device, reads lines, parses percent or SOIL:raw:percent."""
        try:
            ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            await asyncio.sleep(2)
            ser.reset_input_buffer()

            readings = []
            attempts = 0
            while len(readings) < self.num_reads and attempts < self.num_reads * 5:
                line = ser.readline()  # bytes or b''
                attempts += 1
                if not line:
                    continue
                try:
                    text = line.decode('utf-8', errors='replace').strip()
                    value = int(text)
                    readings.append(value)
                except (ValueError, IndexError):
                    continue
                await asyncio.sleep(0.1)

            ser.close()
            if readings:
                self.moisture = round(sum(readings) / len(readings), 2)
                # print(f'wilgotnosc {self.moisture} %')
            else:
                print("No valid readings received")
        except serial.SerialException as e:
            print(f"❌ Błąd Serial: {e}")

    async def data_pipline(self):
        functions = await asyncio.gather(
            self.read_data(),
            self.read_arduino()
        )

    def run_pipline(self):
        asyncio.run(self.data_pipline())
        return {
            "temperature" : self.temperatura,
            "pressure": self.pressure,
            "humidity" : self.humidity,
            "light": self.light,
            "UVI": self.uvi,
            "moisture": self.moisture,
            "time_pnt": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    # helper dla servo
    def read_light(self):
        light = []
        for i in range(2):
            lux = self.tsl2591.lux
            light.append(lux)
            time.sleep(0.5)

        avg_light = round(sum(light) / 2, 2)
        return avg_light

    # helper dla pump
    def read_moisture(self):
        try:
            ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            time.sleep(2)
            ser.reset_input_buffer()

            readings = []
            attempts = 0
            while len(readings) < self.num_reads and attempts < self.num_reads * 5:
                line = ser.readline()  # bytes or b''
                attempts += 1
                if not line:
                    continue
                try:
                    text = line.decode('utf-8', errors='replace').strip()
                    value = int(text)
                    readings.append(value)
                except (ValueError, IndexError):
                    continue
                time.sleep(0.5)

            ser.close()
            if readings:
                moisture = round(sum(readings) / len(readings), 2)
                return moisture
            else:
                print("No valid readings received")
        except serial.SerialException as e:
            print(f"❌ Błąd Serial: {e}")


