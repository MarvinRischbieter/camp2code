"""Class BaseCar: Class to control vehicle regarding speed, direction and steering angle
                   Sensors are not part of this class
"""
from enum import Enum

from basisklassen import *


class Distance(Enum):
    MAX_DISTANCE = 300
    INF_DISTANCE = 1_000


class Angle(Enum):
    MIN_ANGLE = 45
    STRAIGHT_AHEAD = 90
    MAX_ANGLE = 135


class Direction(Enum):
    FORWARD = 1
    STANDSTILL = 0
    BACKWARD = -1


class Speed(Enum):
    STOP_SPEED = 0
    VERY_SLOW_SPEED = 20
    SLOW_SPEED = 30
    NORMAL_SPEED = 50
    HIGH_SPEED = 80
    MAX_SPEED = 100


class BaseCar(object):
    def __init__(self):
        self._steering_angle = Angle.STRAIGHT_AHEAD.value
        self._speed = Speed.STOP_SPEED.value
        self._direction = Direction.STANDSTILL.value

        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                self.turning_offset = data["turning_offset"]
                self.forward_A = data["forward_A"]
                self.forward_B = data["forward_B"]
                self.timeout_sonic = data["timeout_sonic"]
                print("Daten in config.json:")
                print(f" - Turning Offset: {self.turning_offset}")
                print(f" - Forward A: {self.forward_A}")
                print(f" - Forward B: {self.forward_B}")
                print(f" - Timeout sonic: {self.timeout_sonic}")
        except:
            print("Fehler beim einlesen der config.json")
        else:
            self.fw = FrontWheels(self.turning_offset)
            self.bw = BackWheels(self.forward_A, self.forward_B)

    @property
    def steering_angle(self):
        """getter Function "steering_angle" returns the current steering angle
        Args:
            ()
        """
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, value: int):
        """Setter Function "steering_angle" sends the angle to the vehicle and sets the variable
        Args:
            value: represents the steering angle as integer in [45..135]
        """
        if value < Angle.MIN_ANGLE.value:
            angle_n = Angle.MIN_ANGLE.value
        elif Angle.MAX_ANGLE.value < value:
            angle_n = Angle.MAX_ANGLE.value
        else:
            angle_n = value
        self._steering_angle = self.fw.turn(angle_n)

    @property
    def speed(self):
        """getter Function "speed" returns the current speed
        Args:
            ()
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """Setter Function "speed" sends the speed to the vehicle and sets the variable
        Args:
            value: represents the speed as integer in [0..100]
        """
        if value < Speed.STOP_SPEED.value:
            value_n = Speed.STOP_SPEED.value
        elif Speed.MAX_SPEED.value < value:
            value_n = Speed.MAX_SPEED.value
        else:
            value_n = value
        self.bw.speed = value_n
        self._speed = self.bw.speed

    @property
    def direction(self):
        """getter Function "direction" returns the current direction
        Args:
            ()
        """
        return self._direction

    def drive(self, speed: int, direction: int):
        """Function "drive" sends the speed and direction to the vehicle and sets the variables accordingly
        Args:
            speed: speed of the car as integer [0..100]
            direction: direction of the back wheels as integer[-1..1]
        """
        self.speed = speed
        if direction < Direction.BACKWARD.value:
            value_n = Direction.BACKWARD.value
        elif Direction.FORWARD.value < direction:
            value_n = Direction.FORWARD.value
        else:
            value_n = direction
        self._direction = value_n
        print(f"Drehrichtung: {self.direction}-{Direction(self.direction).name}")
        print(f"Speed: {self.speed}")
        if self.direction == Direction.FORWARD.value:
            self.bw.forward()
        elif self.direction == Direction.BACKWARD.value:
            self.bw.backward()
        elif self.direction == Direction.STANDSTILL.value:
            self.bw.stop()
        else:
            raise Exception(f'Unsuported direction value {self.direction}')

    def stop(self):
        """Function "stop" stops the vehicle and sets the variables accordingly
        Args:
            ()
        """
        self.speed = Speed.STOP_SPEED.value
        self.steering_angle = Angle.STRAIGHT_AHEAD.value

    def drive_with_params(self, speed, direction, angle):
        """ Drive with parameters and sets the properties accordingly
        Args:
            speed: speed of the car as integer [0..100]
            direction: direction of the back wheels as integer[-1..1]
            angle: steering angle of the front wheels as integer [45..135]
        """
        self.steering_angle = angle
        self.drive(speed, direction)
