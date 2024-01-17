from basisklassen import  *
from basecar import *

class SonicCar(BaseCar):

    def __init__(self):
        super().__init__()

        self.usm = Ultrasonic(self.timeout_sonic)

    def get_distance_to_obstacle(self):
        distance = self.usm.distance()
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
