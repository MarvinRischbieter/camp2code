from basecar import *
from sonic_car import *
import time

def drive_until_obstacle(sc = SonicCar(), min_distance=20, max_distance=50, speed_min=20, speed_max=50, direction=1):
    '''Drive Until an Obstacle is spotted by the SonicCar Sensor

    Args:
        (max_distance(integer), speed(integer), direction = -1 Rückwerts 0 leerlauf 1 vorwärts) 
    '''
    #sc=SonicCar()
    print (f"Recording start")
    t = RecordingThread(sc)
    t.start()
    while True:
        distance_to_obstacle = sc.get_distance_to_obstacle()
        print (f"Distanz:{distance_to_obstacle}")

        if distance_to_obstacle <= min_distance:
            print("Hindernis erkannt! Stopping...")
            sc.stop()
            break
        if distance_to_obstacle <= max_distance or distance_to_obstacle == 1000 :
            print("Hindernis erkannt! langsamer...")
            sc.steering_angle = 90
            sc.drive(speed_min, direction)
            time.sleep(0.5)
            continue
        else:
            sc.steering_angle = 90
            sc.drive(speed_max, direction)
            time.sleep(0.5)
    print (f"Recording stop")
    t.stop_record()
    t.join()
