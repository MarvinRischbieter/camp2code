from basecar import *
import threading

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


