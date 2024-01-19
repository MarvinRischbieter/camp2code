import datetime
import pathlib
import threading
import time

from basecar import Speed, Direction, Angle
from sonic_car import SonicCar, RecordingThread

def road_test():
    sc = SonicCar()

    print(f'Recording start')
    recording_thread = RecordingThread(sc)
    recording_thread.start()

    # Drive
    sc.drive_with_params(Speed.MIN_SPEED.value, Direction.FORWARD.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(3)

    # Stop
    sc.drive_with_params(Speed.STOP_SPEED.value, Direction.STANDSTILL.value, Angle.STRAIGHT_AHEAD.value)
    time.sleep(1)

    print(f'Recording stop')
    recording_thread.stop_record()
    recording_thread.join()


if __name__ == '__main__':
    road_test()
