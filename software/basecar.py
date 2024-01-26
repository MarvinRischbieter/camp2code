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
    """
    Class BaseCar: Class to control the vehicle regarding speed, direction, and steering angle.
    Sensors are not part of this class.
    """
    def __init__(self):
        """
        Constructor for the BaseCar class.
        """
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
                self.max_steer_angle_left = data["max_steer_angle_left"]
                self.max_steer_angle_right = data["max_steer_angle_right"]
                self.speed_min = data["speed_min"]
                self.speed_max = data["speed_max"]
                self.speed_approach = data["speed_approach"]
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
        """
        Getter for the current steering angle.
        
        @return: the current steering angle.
        """
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, value: int):
        """
        Setter Function "steering_angle" sends the angle to the vehicle and sets the variable.
        
        @input value: represents the steering angle as an integer in [45..135]
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
        """
        Getter Function "speed" returns the current speed.
        
        @return: the current speed.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """
        Setter Function "speed" sends the speed to the vehicle and sets the variable.

        @input value: represents the speed as an integer in [0..100]
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
        """
        Getter for the current direction.
        
        @return: the current direction.
        """
        return self._direction

    def drive(self, speed: int, direction: int):
        """
        Function "drive" sends the speed and direction to the vehicle and sets the variables accordingly.

        @input speed: speed of the car as an integer [0..100]
        @input direction: direction of the back wheels as an integer [-1..1]
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
        """
        Function "stop" stops the vehicle and sets the variables accordingly.
        """
        self.speed = Speed.STOP_SPEED.value
        self.steering_angle = Angle.STRAIGHT_AHEAD.value

    def drive_with_params(self, speed, direction, angle):
        """
        Drive with parameters and sets the properties accordingly.

        @input speed: speed of the car as an integer [0..100]
        @input direction: direction of the back wheels as an integer [-1..1]
        @input angle: steering angle of the front wheels as an integer [45..135]
        """
        self.steering_angle = angle
        self.drive(speed, direction)
