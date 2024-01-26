from basisklassen import  *
from sonic_car import *
import numpy as np
from scipy.ndimage import interpolation
class SensorCar(SonicCar):
    def __init__(self):
        super().__init__()
        self.irm = Infrared()
        self.ir_calib = 0

    def get_calibration(self):
        """
        Get the calibration value for infrared sensors.

        @return: Calibration value
        """
        return self.ir_calib
    
    def ir_calibriation(self):
        """
        Perform infrared calibration.
        """
        while True:
            input("Sensoren auf homogenen Untergrund platzieren und Taste Drücken...")
            tmpcalib = self.irm.get_average(10)
            print("Messergebnis:", tmpcalib)

            user_in = input("Ergebsnis verwenden? (j/n/q)")

            if user_in == "n":
                    print("Fahre fort...")
                    break
            elif user_in == "j":
                messung = np.array(tmpcalib)
                self.ir_calib = messung.mean() / messung
                print("kalibrier0:",self.ir_calib)
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
        """
        Read calibrated values from the config file.
        """
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
        """
        Print current IR measurement values. Deviation from the mean is calculated.
        """
        iraverage = self.irm.get_average(3)
        print("Average Wert ohne Kalibrierung:")  
        print(iraverage)  

    def get_ir_messung(self):
        """
        Get IR measurement values after calibration.

        @return: List of IR measurement values
        """
        ir_messwerte = ((self.irm.get_average(3) - np.array(self.ir_calib)).round(2).tolist())
        return ir_messwerte

    def get_steering_angle(self, ir_messung):
        """
        Get the steering angle based on the IR measurements.

        @input ir_messung: List of IR measurement values
        @return: Steering angle
        """
        steering_interpol = np.linspace(self.max_steer_angle_left, self.max_steer_angle_right, num=30).round(2)
        x = np.array(ir_messung)
        i = 30
        z = i / len(x)

        ir_messwerte_interpol = (interpolation.zoom(x,z).round(2).tolist())
        array_pos_min_wert2 = ir_messwerte_interpol.index(min(ir_messwerte_interpol))
        steering_angle_interpol_2 = steering_interpol[array_pos_min_wert2]

        return steering_angle_interpol_2

