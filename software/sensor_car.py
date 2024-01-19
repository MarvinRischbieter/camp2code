from basisklassen import  *
from sonic_car import *
import numpy as np
from scipy.ndimage import interpolation

#lock = threading.Lock()
#lock_file = threading.Lock()

class SensorCar(SonicCar):

    def __init__(self):
        super().__init__()
        self.irm = Infrared()
        self.ir_calib = 0

    def get_calibration(self):
        return self.ir_calib
    

    def ir_calibriation(self):
        #print("ircalib"
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
        #print("Avg Werte mit Kalirbrierung - Array ir_messwerte:")
        #print(ir_messwerte)
        return ir_messwerte

    def get_steering_angle(self, ir_messung):
        # Array auf 15 Werte vergrößern
        steering_interpol = np.linspace(self.max_steer_angle_left, self.max_steer_angle_right, num=30).round(2)
        #print("Interpolierter steering angle Methode 2")
        #print(steering_interpol)

        # Messwerte ebenfalls auf 15 Werte vergrößern, dazwischen interpolieren:
        x = np.array(ir_messung)
        i = 30
        z = i / len(x)
        ir_messwerte_interpol = (interpolation.zoom(x,z).round(2).tolist())
        #print("Interpolierte IR Messwerte 2")
        #print(ir_messwerte_interpol)

        #print("Min Wert Methode 2")
        #print(min(ir_messwerte_interpol))

        #print("Array Position des Min Werts Methode 2")
        array_pos_min_wert2 = ir_messwerte_interpol.index(min(ir_messwerte_interpol))
        #print(array_pos_min_wert2)

        steering_angle_interpol_2 = steering_interpol[array_pos_min_wert2]
        #print("Interpolierter steering angle Methode 2")
        #print(steering_angle_interpol_2)
        return steering_angle_interpol_2

