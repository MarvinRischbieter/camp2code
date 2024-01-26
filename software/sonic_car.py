from basecar import *
import threading

class SonicCar(BaseCar):
    def __init__(self):
        """
        Initialize the SonicCar class, inheriting from BaseCar.

        Initializes the Ultrasonic sensor and a threading lock for distance measurements.
        """
        super().__init__()
        self._usm = Ultrasonic(timeout=self.timeout_sonic)
        self._lock = threading.Lock()

    def get_distance_to_obstacle(self):
        """
        Get the distance to the obstacle measured by the Ultrasonic sensor.

        @return: The distance to the obstacle in centimeters. Returns `Distance.INF_DISTANCE.value` if an error occurs.
        """
        self._lock.acquire()
        distance = self._usm.distance()
        self._lock.release()

        if distance >= 0:
            return distance
        else:
            return Distance.INF_DISTANCE.value

    def make_measures(self):
        """
        Perform a series of distance measurements and print the results.

        @input: None
        @return: None
        """
        for i in range(100):
            distance = self.get_distance_to_obstacle()

            if distance == Distance.INF_DISTANCE.value:
                unit = 'Error'
            else:
                unit = 'cm'
                
            print(f'{i}: {distance} {unit}')
            time.sleep(1)


