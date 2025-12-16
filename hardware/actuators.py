import time
import pigpio
from hardware.sensors import SensorHub
from gpiozero import OutputDevice

class Servo:
    def __init__(self):
        self.current_positon = None
        self.light_sensor = SensorHub(5)
        self.light_value = self.read_light()
        self.pi = pigpio.pi()
        self.servo_pin = 18

    def _pi_setup(self):
        self.pi.set_mode(self.servo_pin, pigpio.OUTPUT)

    def read_light(self):
        return self.light_sensor.read_light()

    def set_servo_angle(self, angle):
        pulse_width = 1500 + (angle * 1000 / 120)
        pulse_width = int(max(500, min(2500, pulse_width)))

        self.pi.set_servo_pulsewidth(self.servo_pin, pulse_width)

    def adjust_servo(self):
        angle = self.current_positon if self.current_positon is not None else 0
        current_light = self.light_value
        while current_light < 200 and (angle > -70 or angle < 70):
            self.set_servo_angle(angle)
            temp_light = self.read_light()
            if temp_light >= current_light:
                angle += 5
                current_light = temp_light
            elif temp_light < current_light:
                angle -= 5
                current_light = temp_light
            else:
                break
        self.current_positon = angle

    def run_servo(self):
        self._pi_setup()
        self.adjust_servo()

    def rotate_plant(self, current_positon : int, sleep_time: float = 30):
        angle = current_positon
        self.set_servo_angle(angle)
        time.sleep(2)

        if 1 <= angle < 60:
            angle += 5
            self.set_servo_angle(angle)
        elif -60 < angle <= 0:
            angle -= 5
            self.set_servo_angle(angle)
        elif angle >= 60:
            while angle >= 1:
                angle -= 5
                self.set_servo_angle(angle)
                time.sleep(sleep_time)
        elif angle <= -60:
            while angle <= 0:
                angle += 5
                self.set_servo_angle(angle)
                time.sleep(sleep_time)
        time.sleep(1.5)
        return self.rotate_plant(angle)


    def user_rotate_plant(self, direction: str, current_positon: int):
        angle = current_positon
        self.set_servo_angle(angle)
        time.sleep(0.5)

        if direction == "right" and angle < 70:
            angle += 10
            self.set_servo_angle(angle)
        elif direction == "left" and angle > -70:
            angle -= 10
            self.set_servo_angle(angle)
        time.sleep(0.5)
        return angle

class Pump:
    def __init__(self):
        self.moisture_sensor = SensorHub(5)
        self.moisture_value = self.read_moisture()
        self.pump_pin = 17
        self.relay = None

    def read_moisture(self):
        return self.moisture_sensor.read_moisture()

    def _relay_setup(self):
        self.relay = OutputDevice(self.pump_pin, active_high=False, initial_value=False)

    def water_plant(self):
        current_moisture = self.moisture_value
        while current_moisture < 30:
            self.relay.on()
            time.sleep(1)
            self.relay.off()
            current_moisture = self.read_moisture()

    def run_pump(self):
        self._relay_setup()
        self.water_plant()

    def user_water_plant(self, duration: int):
        if duration is None or duration > 2:
            duration = 1

        self._relay_setup()
        self.relay.on()
        time.sleep(duration)
        self.relay.off()
        self.relay.close()

    def stop_pump(self):
        self.relay.off()


def main():
    test = Servo()
    test.rotate_plant(0)

if __name__ == "__main__":
    main()

