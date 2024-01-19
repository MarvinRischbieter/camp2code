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
    car.drive_with_params(Speed.STOP_SPEED.value, Direction.STANDSTILL.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)

    # Drive
    print('2-Drive')
    car.drive_with_params(Speed.SLOW_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(3)

    # Stop
    print('3-Stop')
    car.drive_with_params(Speed.STOP_SPEED.value, Direction.STANDSTILL.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)

    # Drive
    print('4-Drive')
    car.drive_with_params(Speed.SLOW_SPEED.value, Direction.BACKWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(3)

    # Stop
    print('5-Stop')
    car.drive_with_params(Speed.STOP_SPEED.value, Direction.STANDSTILL.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)


if __name__ == '__main__':
    # road_test()
    road_1()
