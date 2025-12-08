# pompa i serwo
import time
import pigpio
from sensors import SensorHub
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

    # zakladamy optimal light na 200lux
    def adjust_servo(self):
        angle = 0
        current_light = self.light_value
        while current_light < 200 and (angle > -70 or angle < 70):
            print(f"aktualne swiatlo: {current_light}")
            self.set_servo_angle(angle)
            temp_light = self.read_light()
            if temp_light >= current_light:
                angle += 5
                current_light = temp_light
            elif temp_light < current_light:
                angle -= 5
                current_light = temp_light
            else:
                print("blad")
                break
        self.current_positon = angle #todo jakos uzywac tego do obrotu np dac angle = self.c...
    def run_servo(self):
        self._pi_setup()
        self.adjust_servo()

    def rotate_plant(self, current_positon : int):
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
                self.set_servo_angle(angle )
                time.sleep(0.5)
        elif angle <= -60:
            while angle <= 0:
                angle += 5
                self.set_servo_angle(angle)
                time.sleep(0.5)
        time.sleep(1.5)
        return self.rotate_plant(angle)



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
            print("Pompowanie woedy przez 1 sekunde")
            time.sleep(1)
            self.relay.off()
            current_moisture = self.read_moisture()

    def run_pump(self):
        self._relay_setup()
        self.water_plant()


#todo: można dodać wywoływanie tych klas po odczycie z bazy danych wartości niższych niż wymagane


def main():
    test = Servo()

    test.rotate_plant(0)

if __name__ == "__main__":
    main()




