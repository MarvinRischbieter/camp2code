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
    MIN_SPEED = 20
    NORMAL_SPEED = 50
    MAX_SPEED = 100


class BaseCar(object):
    def __init__(self):
        self._steering_angle = 90
        self._speed = 0
        self._direction = 0

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
            (integer which represents the steering angle:[45..135])
        """
        self._steering_angle = self.fw.turn(value)

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
            (integer which represents the speed: [0..100])
        """
        if value > 100:
            value = 100
        elif value < 0:
            value = 0
        self.bw.speed = value
        self._speed = value

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
            (speed as integer: [0..100], direction as integer [-1,1] )
        """
        if speed > 100:
            speed = 100
        elif speed < 0:
            speed = 0
        self.bw.speed = speed
        self._speed = self.bw.speed
        self._direction = direction
        print(f"Drehrichtung: {self._direction}")
        print(f"Speed: {self._speed}")
        if direction > 0:
            self.bw.forward()
        elif direction < 0:
            self.bw.backward()
        else:
            self.stop()

    def stop(self):
        """Function "stop" stops the vehicle and sets the variables accordingly
        Args:
            ()
        """
        self.bw.stop()
        self._speed = 0
