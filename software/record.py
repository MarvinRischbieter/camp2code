import datetime
import pathlib
import threading
from sonic_car import *
from sensor_car import *


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
            data_row = {
                'Time': date_string,
                'Speed': self._sc.speed,
                'Direction': self._sc.direction,
                'Angle': self._sc.steering_angle,
            }
            if isinstance(self._sc, SonicCar):
                data_row['Distance'] = self._sc.get_distance_to_obstacle()
            if isinstance(self._sc, SensorCar):
                data_row['IR Value'] = self._sc.get_ir_messung()
            data_recorded.append(data_row)
            time.sleep(.1)

        # print(f'Recording done')
        self._lock_file.acquire()
        header_row = list(data_recorded[0].keys())
        header_exists = self._file.exists() and self._file.stat().st_size > 0
        with self._file.open('a+', encoding='utf8') as fp:
            if not header_exists:
                fp.write(';'.join(header_row))
                fp.write('\n')
            for row in data_recorded:
                row_data = [row[x] for x in header_row]
                row_data = [str(x) for x in row_data]
                fp.write(';'.join(row_data))
                fp.write('\n')
        self._lock_file.release()
