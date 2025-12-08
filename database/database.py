import sqlite3
import time
from datetime import datetime
from hardware.sensors import SensorHub
import asyncio
import json

class Database:
    def __init__(self, num_readings : int):
        self.database_file = "database/doniczka.db"
        self.data = {}
        self.sensor = SensorHub(num_readings)

    def read_data(self):
        data = self.sensor.run_pipline()
        self.data = data

    def insert_to_db(self):
        try:
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()

            hat_query = """INSERT INTO env_sensor(time_pnt, temperature, pressure, humidity, light, uv)
                            VALUES(:time_pnt, :temperature, :pressure, :humidity, :light, :uv)
                        """
            cursor.execute(hat_query, {
                'time_pnt': self.data['time_pnt'],
                'temperature': self.data['temperature'],
                'pressure': self.data['pressure'],
                'humidity': self.data['humidity'],
                'light': self.data['light'],
                'uv': self.data['UVI']
            })

            conn.commit()

            moist_query = """INSERT INTO moist_sensor(time_pnt, moisture) VALUES(:time_pnt, :moisture)"""
            cursor.execute(moist_query, {
                'time_pnt': self.data['time_pnt'],
                'moisture': self.data['moisture']
            })

            conn.commit()

            cursor.close()
            conn.close()
            return {"status": 'dodano'}
        except Exception as e:
            return {"error": str(e)}

    def read_db(self):
        try:
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()

            query = """SELECT * FROM env_sensor ORDER BY id DESC LIMIT 1"""
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return {'status': 'ok', 'data': result}
        except Exception as e:
            return {'error': str(e)}


def main():
    db = Database(5)
    try:
        while True:
            db.read_data()
            db.insert_to_db()
            time.sleep(10)
    except KeyboardInterrupt:
        result = db.read_db()
        print(result)
        return

if __name__ == "__main__":
    main()
