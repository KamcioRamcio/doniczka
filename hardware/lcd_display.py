from RPLCD.i2c import CharLCD
import RPLCD.i2c
import time
import sqlite3

class LCD:
    def __init__(self):
        self.db_file = "database/doniczka.db"
        self.data = None
        self.formated_data = {}

    def get_data(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        query = """SELECT * FROM env_sensor e JOIN moist_sensor m ON e.time_pnt = m.time_pnt ORDER BY id DESC LIMIT 1"""
        cursor.execute(query)
        self.data = cursor.fetchall()

        cursor.close()
        conn.close()
        return self.data

    def format_data(self):
        self.formated_data = {
            "temperature": self.data[0][2],
            "pressure": self.data[0][3],
            "humidity": self.data[0][4],
            "light": self.data[0][5],
            "uv": self.data[0][6],
            "moisture": self.data[0][9]
        }
        return self.formated_data


    def display(self):
        lcd = CharLCD('PCF8574', 0x27, port=0, charmap='A00',
                      cols=16, rows=2, dotsize=8,
                      auto_linebreaks=True,
                      backlight_enabled=True)

        lcd.clear()

        padding = ' ' * 2
        text = "temp:" + str(self.formated_data["temperature"]) + "C" + padding + "pres:" + str(
            int(self.formated_data["pressure"])) + "hPa" + padding + "hum:" + str(
            self.formated_data["humidity"]) + "%" + padding + "light:" + str(
            int(self.formated_data["light"])) + "Lux" + padding + "UV:" + str(self.formated_data["uv"], ) + padding + "moist:" + str(
            int(self.formated_data["moisture"])) + "%"

        separator = ' ' * 4
        scroll_text = text + separator

        for i in range(len(scroll_text)):
            frame = ''
            for j in range(16):
                frame += scroll_text[(i + j) % len(scroll_text)]
            lcd.cursor_pos = (0, 0)
            lcd.write_string(frame)
            time.sleep(0.3)


def main():
    lcd = LCD()
    while True:
        lcd.get_data()
        lcd.format_data()
        lcd.display()

if __name__ == "__main__":
    main()