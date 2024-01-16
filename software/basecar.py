from basisklassen import  *

class BaseCar(object):
    def __init__(self):
        self.turning_offset = 35
        self.forward_A = 0
        self.forward_B = 0
        self._steering_angle = 90
        self._speed = 0
        self._direction = 0
        '''        try:
            with open("/home/pi/git/camp2code/software/config.json", "r") as f:
                data = json.load(f)
                self.turning_offset = data["turning_offset"]
                self.forward_A = data["forward_A"]
                self.forward_B = data["forward_B"]
                print("Daten in config.json:")
                print(" - Turning Offset: ", turning_offset)
                print(" - Forward A: ", forward_A)
                print(" - Forward B: ", forward_B)
                x =input('Weiter? Bitte eingabetaste')
        except:
            print("Keine geeignete Datei config.json gefunden!")
        else:
        '''
        self.fw = FrontWheels(self.turning_offset)
        self.bw = BackWheels(self.forward_A,self.forward_B)
        self.usm = Ultrasonic(timeout=0.15)
        self.irm = Infrared()
    
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
    
      
    def steer(self,Winkel):
        print('Drehung')
        self.fw.turn(Winkel)
      
    def drive_fw(self,speed):
        print('fahren')
        self.bw.speed = speed
        self.bw.forward()
    
    def drive_stop(self):
        print('anhalten')
        self.bw.stop()  
        
        
            
    # steering_angle: Setzen und Zugriff auf den Lenkwinkel (Property mit Setter)       
    #@property 
    #def steering_angle(self):
    
