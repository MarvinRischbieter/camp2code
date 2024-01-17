from basisklassen import  *
from basecar import *

class SonicCar(BaseCar):

    def __init__(self):
        super().__init__()

        self.usm = Ultrasonic()

    def get_distance_to_obstacle(self):
        return self.usm.distance()


    def make_measures(self):
        for i in range(100):
            distance = self.get_distance_to_obstacle()
            if distance < 0:
                unit = 'Error'
            else:
                unit = 'cm'
            print(f'{i}: {distance} {unit}')
            time.sleep(.5)
