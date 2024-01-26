from basecar import *
from sonic_car import *
from record import *
import time

def drive_until_obstacle(sc, min_distance=20, max_distance=50, speed_min=20, speed_max=50, direction=1):
    '''Drive Until an Obstacle is spotted by the SonicCar Sensor

    Args:
        sc: SonicCar object.
        min_distance: Minimum distance to the obstacle for stopping (default is 20).
        max_distance: Maximum distance for reduced speed (default is 50).
        speed_min: Minimum speed when obstacle is close (default is 20).
        speed_max: Maximum speed when no obstacles are nearby (default is 50).
        direction: Direction of movement (-1 for backward, 0 for idle, 1 for forward) (default is 1).
    '''
    print (f"Recording start")
    t = RecordingThread(sc)
    t.start()
    print (type(sc))

    if isinstance(sc, SonicCar) :
        print("true")

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
