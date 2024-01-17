from basisklassen import  *

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
                print("Daten in config.json:")
                print(f" - Turning Offset: {self.turning_offset}")
                print(f" - Forward A: {self.forward_A}")
                print(f" - Forward B: {self.forward_B}")
        except:
            print("Fehler beim einlesen der config.json")
        else:
            self.fw = FrontWheels(self.turning_offset)
            self.bw = BackWheels(self.forward_A,self.forward_B)
            
            
    @property
    def steering_angle(self):  
        return self._steering_angle
    
    @steering_angle.setter
    def steering_angle(self, value):
        self._steering_angle = self.fw.turn(value)
    
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self.bw.speed = value
        self._speed = value
        
    @property
    def direction(self):
        return self._direction

        
    def drive(self, geschwindigkeit:int, drehrichtung: int):
        if geschwindigkeit > 100 : geschwindigkeit = 100
        elif geschwindigkeit < 0 : geschwindigkeit = 0
        self.bw.speed = geschwindigkeit
        self._speed = self.bw.speed
        self._direction = drehrichtung
        print(f"Drehrichtung: {self._direction}")
        print(f"Speed: {self._speed}")
        if drehrichtung > 0:
            self.bw.forward()
        elif drehrichtung < 0:
            self.bw.backward()
        else:
            self.stop()

    def stop(self):
        self.bw.stop()    
    
