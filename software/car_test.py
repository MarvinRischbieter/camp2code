import time

from basecar import BaseCar, Speed, Direction, Angle
from sonic_car import SonicCar, RecordingThread


def road_test():
    sc = SonicCar()

    print(f'Recording start')
    recording_thread = RecordingThread(sc)
    recording_thread.start()

    # Drive
    sc.drive_with_params(Speed.SLOW_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(3)

    # Stop
    sc.drive_with_params(Speed.STOP_SPEED.value, Direction.STANDSTILL.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)

    print(f'Recording stop')
    recording_thread.stop_record()
    recording_thread.join()


def road_1():
    car = BaseCar()
    # Stop
    print('1-Stop')
    car.stop()
    time.sleep(1)

    # Drive
    print('2-Drive')
    car.drive_with_params(Speed.SLOW_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(3)

    # Stop
    print('3-Stop')
    car.stop()
    time.sleep(1)

    # Drive
    print('4-Drive')
    car.drive_with_params(Speed.SLOW_SPEED.value, Direction.BACKWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(3)

    # Stop
    print('5-Stop')
    car.stop()
    time.sleep(1)



def road_2():
    car = BaseCar()
    # Stop
    print('1-Stop')
    car.stop()
    time.sleep(1)

    # Drive
    print('2-Drive')
    car.drive_with_params(Speed.SLOW_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)

    # Stop
    print('3-Stop')
    car.stop()
    time.sleep(1)

    # Drive
    print('4-Drive')
    car.drive_with_params(Speed.SLOW_SPEED.value, Direction.FORWARD.value, Angle.MAX_ANGLE.value)
    time.sleep(8)

    # Stop
    print('5-Stop')
    car.stop()
    time.sleep(1)

    # Drive
    print('6-Drive')
    car.drive_with_params(Speed.SLOW_SPEED.value, Direction.BACKWARD.value, Angle.MAX_ANGLE.value)
    time.sleep(8)

    # Stop
    print('7-Stop')
    car.stop()
    time.sleep(1)

    # Drive
    print('8-Drive')
    car.drive_with_params(Speed.SLOW_SPEED.value, Direction.BACKWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)

    # Stop
    print('7-Stop')
    car.stop()
    time.sleep(1)


def road_3():

    stop_dist = 20
    reduce_speed_dist = 50

    car = SonicCar()
    
    print(f'Recording start')
    recording_thread = RecordingThread(car)
    recording_thread.start()

    # Stop
    print('1-Stop')
    car.stop()
    time.sleep(1)

    while True:
        distance = car.get_distance_to_obstacle()
        if distance < stop_dist:
            print(f'distance={distance} < {stop_dist} --> stop')
            car.stop()
            break
        
        if distance < reduce_speed_dist:
            print(f'distance={distance} < {reduce_speed_dist} --> reduced speed')
            car.drive_with_params(Speed.SLOW_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)
        else:
            print(f'distance={distance} >= {reduce_speed_dist} --> normal speed')
            car.drive_with_params(Speed.NORMAL_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)

        time.sleep(.1)

    # Stop
    print('3-Stop')
    car.stop()
    time.sleep(1)

    print(f'Recording stop')
    recording_thread.stop_record()
    recording_thread.join()

if __name__ == '__main__':
    # road_test()
    # road_1()
    # road_2()
    road_3()
