from basisklassen import  *
from basecar import *
import threading
import datetime
import json
import pathlib

lock = threading.Lock()

class SonicCar(BaseCar):

    def __init__(self):
        super().__init__()

        self.usm = Ultrasonic(self.timeout_sonic)

    def get_distance_to_obstacle(self):
        lock.acquire()
        distance = self.usm.distance()
        lock.release()
        if distance >= 0: 
            return distance
        elif distance == -2:
            return 300
        else:
            return 1000


    def make_measures(self):
        t = RecordingThread(self)
        t.start()

        for i in range(100):
            distance = self.get_distance_to_obstacle()
            if distance == 1000:
                unit = 'Error'
            else:
                unit = 'cm'
            print(f'{i}: {distance} {unit}')
            time.sleep(1)

        t.stop_record()
        t.join()


    def drive(self, speed, direction):
        t = RecordingThread(self)
        t.start()
        super().drive(speed, direction)
        t.stop_record()
        t.join()


class RecordingThread(threading.Thread):
    def __init__(self, sc):
        threading.Thread.__init__(self)
        self._sc = sc
        self._stop_record = False
    
    def stop_record(self):
        self._stop_record = True
   
    def run(self):
        data_recorded = []
        while not self._stop_record:
            #print(f'Recording')
            date_string = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
            data_recorded.append({
                'Time': date_string,
                'Speed': self._sc.speed,
                'Direction': self._sc.direction,
                'Angle': self._sc.steering_angle,
                'Distance': self._sc.get_distance_to_obstacle(),
            })
            time.sleep(.5)

        #print(f'Recording done')
        date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
        with pathlib.Path(f'{date_str}_data.json').open('w', encoding='utf8') as fp:
            json.dump(data_recorded, fp, indent=2, default=str)
