from basisklassen import  *
from sonic_car import *
import numpy as np


#lock = threading.Lock()
#lock_file = threading.Lock()

class SensorCar(SonicCar):

    def __init__(self):
        super().__init__()
        self.irm = Infrared()
        self.ir_calib = 0


    def ir_calib(self):
        #-------------------------
        # Benutzer Eingabe:
        #-------------------------
        while True:
            input("Sensoren auf homogenen Untergrund platzieren und Taste Drücken...")
            tmpcalib = self.irm.get_average(10)
            print("Messergebnis:", tmpcalib)

            user_in = input("Ergebsnis verwenden? (j/n/q)")
            if user_in == "n":
                    print("Fahre fort...")
                    break
            elif user_in == "j":
                # Homogener Untergrund  - Abweichung zum Mittelwert = Kalibrier-Werte
                messung = np.array(tmpcalib)
                # Prozentuale Verrechnung ginge auch:
                self.ir_calib = messung.mean() / messung
                print("kalibrier0:",self.ir_calib)
                # Nehmen jetzt den Mittelwert und subtrahieren diesen später
                self.ir_calib = messung.mean()
                print("kalibrier1:",self.ir_calib)
                self.ir_calib = self.ir_calib.round(4)
                print("kalibrier2:",self.ir_calib)
                data = {}
                try:
                    with open("config.json", "r") as f:
                        data = json.load(f)
                except:
                    print("Read File error ")
                data["self.ir_calib"] = self.ir_calib.tolist()
                try:
                    with open("config.json", "w") as f:
                        json.dump(data, f)
                except:
                    print("Write File error")
                    break
                break
            else:
                print("Abbruch durch , fahre fort...")
                break
                
    def read_calib(self):
        #-------------------------
        # Kalirbrier-Werte aus Config lesen:
        #-------------------------
        print("Lese Kalibrier-Werte aus Config:")
        with open("config.json", "r") as f:
            data = json.load(f)
            self.ir_calib = data.get("ir_calib")
            if self.ir_calib != None:
                self.ir_calib = self.ir_calib
            else:
                self.ir_calib = [1, 1, 1, 1, 1]
        print("Kalibrierwert:", self.ir_calib)



    def print_ir_messung(self):
        #-------------------------
        # Ausgabe der aktuellen IR Messwerte:
        #-------------------------
        iraverage = self.irm.get_average(3)
        print("Average Wert ohne Kalibrierung:")  
        print(iraverage)  

    def get_ir_messung(self):
        #-------------------------
        # Ausgabe der kalibrierten IR Messwerte:
        #-------------------------
        # Kalibrierung verrechnung (Abweichung zum Mittelwert)
        ir_messwerte = ((self.irm.get_average(3) - np.array(self.ir_calib)).round(2).tolist())
        print("Avg Werte mit Kalirbrierung - Array ir_messwerte:")
        print(ir_messwerte)
        return ir_messwerte

    def get_steering_angle(self):
        ir_messwerte = get_ir_messung()
        # -----------------
        # METHODE 1 über Minimum im Array
        # dort wo das Minimum ist = Position der Schw. Linie
        # -----------------
        print("Position der Spur (Minimum im Array:):")
        location_min_IR_array_value = ir_messwerte.index(min(ir_messwerte))
        print(location_min_IR_array_value)

        IR_to_steering_x = [0, 1, 2, 3, 4]
        IR_to_steering_y = [-45, -22.5, 0, 22.5, 45]

        # steering angle aus look up table interpolieren:

        steering_angle_interp = np.interp(location_min_IR_array_value, IR_to_steering_x, IR_to_steering_y)
        print("Interpolierter steering angle")
        print(steering_angle_interp)
        return steering_angle_interp
    
    
'''
print("Ausgabe Messwerte:")
for i in range(5):
    data = self.irm.get_average(10)
    print('{} : {}'.format(i, data))
    time.sleep(.2)
'''    
