import datetime
import pathlib
import threading

from basecar import *


class SonicCar(BaseCar):

    def __init__(self):
        super().__init__()
        self._usm = Ultrasonic(timeout=self.timeout_sonic)
        self._lock = threading.Lock()

    def get_distance_to_obstacle(self):
        self._lock.acquire()
        distance = self._usm.distance()
        self._lock.release()
        if distance >= 0:
            return distance
        elif distance == -2:
            return Distance.MAX_DISTANCE.value
        else:
            return Distance.INF_DISTANCE.value

    def make_measures(self):
        for i in range(100):
            distance = self.get_distance_to_obstacle()
            if distance == Distance.INF_DISTANCE.value:
                unit = 'Error'
            else:
                unit = 'cm'
            print(f'{i}: {distance} {unit}')
            time.sleep(1)

    def drive_with_params(self, speed, direction, angle):
        self.steering_angle = angle
        super().drive(speed, direction)


class RecordingThread(threading.Thread):
    def __init__(self, sc):
        threading.Thread.__init__(self)
        self._sc = sc
        self._lock_file = threading.Lock()
        self._stop_record = False
        record_folder = pathlib.Path('records')
        record_folder.mkdir(parents=True, exist_ok=True)
        date_string = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        self._file = pathlib.Path(record_folder, f'{date_string}_data.csv')

    def stop_record(self):
        self._stop_record = True

    def run(self):
        data_recorded = []
        while not self._stop_record:
            # print(f'Recording')
            date_string = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
            data_recorded.append({
                'Time': date_string,
                'Speed': self._sc.speed,
                'Direction': self._sc.direction,
                'Angle': self._sc.steering_angle,
                'Distance': self._sc.get_distance_to_obstacle(),
            })
            time.sleep(.1)

        # print(f'Recording done')
        self._lock_file.acquire()
        header_exists = self._file.exists() and self._file.stat().st_size > 0
        with self._file.open('a+', encoding='utf8') as fp:
            if not header_exists:
                fp.write(';'.join(['Time', 'Speed', 'Direction', 'Angle', 'Distance']))
                fp.write('\n')
            for row in data_recorded:
                row_data = [row['Time'], row['Speed'], row['Direction'], row['Angle'], row['Distance']]
                row_data = [str(x) for x in row_data]
                fp.write(';'.join(row_data))
                fp.write('\n')
        self._lock_file.release()
