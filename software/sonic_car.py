from basisklassen import  *
from basecar import *
import threading
import datetime
import json
import pathlib

lock = threading.Lock()
lock_file = threading.Lock()

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
        for i in range(100):
            distance = self.get_distance_to_obstacle()
            if distance == 1000:
                unit = 'Error'
            else:
                unit = 'cm'
            print(f'{i}: {distance} {unit}')
            time.sleep(1)


class RecordingThread(threading.Thread):
    def __init__(self, sc):
        threading.Thread.__init__(self)
        self._sc = sc
        self._stop_record = False
        self._filename = f'data.json'
    
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
            time.sleep(.1)

        #print(f'Recording done')
        lock_file.acquire()
        old_records = []
        file = pathlib.Path(self._filename)
        if file.exists() and file.stat().st_size > 0:
            with pathlib.Path(self._filename).open('r', encoding='utf8') as fp:
                data = json.load(fp)
                old_records = data if data else old_records
        with pathlib.Path(self._filename).open('w', encoding='utf8') as fp:
            json.dump(old_records + data_recorded, fp, indent=2, default=str)
        lock_file.release()
