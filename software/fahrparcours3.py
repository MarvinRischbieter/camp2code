# course_functions.py

from basecar import drive, stop, measure_distance, soniccar
import time

def drive_until_obstacle(max_distance=30, speed=20, direction=1):
    '''Drive Until an Obstacle is spotted by the SonicCar Sensor

    Args:
        (max_distance(integer), speed(integer), direction = -1 Rückwerts 0 leerlauf 1 vorwärts) 
    '''
    while True:
        distance_to_obstacle = measure_distance()

        if distance_to_obstacle <= max_distance:
            print("Hindernis erkannt! Stopping...")
            stop()
            break

        drive(speed, direction)
        time.sleep(0.1)


if __name__ == "__main__":
    # Fahrparcours 3 durchführen (vorwärtsfahren, bis ein Hindernis erkannt wird)
    drive_until_obstacle(distance_threshold=25, speed=15, direction=1)