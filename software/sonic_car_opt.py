from basisklassen import  *
from basecar import *
import threading
import datetime
import json
import pathlib
from enum import Enum

class Distance(Enum):
    MAX_DISTANCE = 300
    INF_DISTANCE = 1_000


class SonicCar(BaseCar):

    def __init__(self):
        super().__init__()
        self._usm = Ultrasonic()
        self._lock = threading.Lock()

    def get_distance_to_obstacle(self):
        self._lock.acquire()
        distance = self._usm.distance()
        self._lock.release()
        if distance >= 0: 
            return distance
        if distance in (-1, -2):
            return Distance.MAX_DISTANCE.value
        return Distance.INF_DISTANCE.value


    def make_measures(self):
        t = RecordingThread(self)
        t.start()

        for i in range(10):
            distance = self.get_distance_to_obstacle()
            if distance == 1000:
                unit = 'Error'
            else:
                unit = 'cm'
            print(f'{i}: {distance} {unit}')
            time.sleep(1)

        t.stop_record()
        t.join()

    
    def drive(self, speed, direction, angle, record_data=True):
        if record_data:
            command_data = {
                'speed': speed,
                'direction': direction,
                'angle': angle,
            }
            t = RecordingThread(self, command_data)
            t.start()
        if angle is not None:
            self.steering_angle = angle
        super().drive(speed, direction)
        if record_data:
            return t
        return


class RecordingThread(threading.Thread):
    def __init__(self, sc, command_data=None):
        threading.Thread.__init__(self)
        self._sc = sc
        self._stop_record = False
        self._command_data = command_data if command_data else {}
    
    def stop_record(self):
        self._stop_record = True
   
    def run(self):
        data_recorded = []
        while not self._stop_record:
            date_string = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
            data_recorded.append({
                'Time': date_string,
                'Speed': self._sc.speed,
                'Direction': self._sc.direction,
                'Angle': self._sc.steering_angle,
                'Distance': self._sc.get_distance_to_obstacle(),
            })
            time.sleep(.1)

        command_str = ''
        if self._command_data:
            speed = str(self._command_data.get('speed', ''))
            speed = f'speed={speed}'if speed else ''
            direction = str(self._command_data.get('direction', ''))
            direction = f'direction={direction}'if direction else ''
            angle = str(self._command_data.get('angle', ''))
            angle = f'angle={angle}'if angle else ''
            elts = [speed, direction, angle]
            elts = [x for x in elts if x]
            command_str = '_'.join(elts)

        date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
        with pathlib.Path(f'{date_str}_{command_str}_data.json').open('w', encoding='utf8') as fp:
            json.dump(data_recorded, fp, indent=2, default=str)


def main():
    sc = SonicCar()

    # Drive with data recording
    t = sc.drive(20, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(3)
    if t:
        t.stop_record()
        t.join()

    # Stop with data recording
    t = sc.drive(20, Direction.STANDSTILL.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)
    if t:
        t.stop_record()
        t.join()

    #sc.drive_n_seconds(20, 0, n_sec=2)

def road_test():
    sc = SonicCar()

    t = sc.drive(20, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(3)
    if t:
        t.stop_record()
        t.join()

    t = sc.drive(20, Direction.FORWARD.value, Angle.MIN_ANGLE.value)
    time.sleep(3)
    if t:
        t.stop_record()
        t.join()

    t = sc.drive(20, Direction.FORWARD.value, Angle.MAX_ANGLE.value)
    time.sleep(3)
    if t:
        t.stop_record()
        t.join()

    # Stop with data recording
    t = sc.drive(20, Direction.STANDSTILL.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)
    if t:
        t.stop_record()
        t.join()


def road_3():
    min_distance=20
    max_distance=50

    sc = SonicCar()
    t = sc.drive(Speed.STOP_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)

    while True:
        distance_to_obstacle = sc.get_distance_to_obstacle()
        print(f"distance_to_obstacle: {distance_to_obstacle}")

        if distance_to_obstacle <= min_distance:
            print("Hindernis erkannt! Stopping...")
            sc.drive(Speed.STOP_SPEED.value, Direction.STANDSTILL.value, Angle.STRAIGHT_AHEAD.value, record_data=False)
            break

        if distance_to_obstacle <= max_distance:
            print("Hindernis erkannt! langsamer...")
            sc.drive(Speed.SLOW_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value, record_data=False)
        else:
            print("Kein Hindernis erkannt! normal...")
            sc.drive(Speed.NORMAL_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value, record_data=False)

        time.sleep(.5)

    if t:
        t.stop_record()
        t.join()


if __name__ == '__main__':
    #main()
    road_3()
    #road_test()
