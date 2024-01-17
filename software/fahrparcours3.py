from basecar import *
from sonic_car import *
import time

def drive_until_obstacle(sc = SonicCar, max_distance=30, speed=50, direction=1):
    '''Drive Until an Obstacle is spotted by the SonicCar Sensor

    Args:
        (max_distance(integer), speed(integer), direction = -1 Rückwerts 0 leerlauf 1 vorwärts) 
    '''
    #sc=SonicCar()
    
    while True:
        distance_to_obstacle = sc.get_distance_to_obstacle()
        print (f"Distanz:{distance_to_obstacle}")

        if distance_to_obstacle <= max_distance:
            print("Hindernis erkannt! Stopping...")
            sc.stop()
            break
        sc.steering_angle = 90
        sc.drive(speed, direction)
        time.sleep(0.5)

