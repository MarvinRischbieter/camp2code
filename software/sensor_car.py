from basisklassen import  *
from basecar import *
import numpy as np


lock = threading.Lock()
lock_file = threading.Lock()

class SonicCar(BaseCar):

    def __init__(self):
        super().__init__()

irm = Infrared()

print("Ausgabe Messwerte:")
for i in range(5):
    data = irm.get_average(10)
    print('{} : {}'.format(i, data))
    time.sleep(.2)
    
#-------------------------
# Benutzer Eingabe:
#-------------------------
while True:
    input("Sensoren auf homogenen Untergrund platzieren und Taste Drücken...")
    tmpcalib = irm.get_average(10)
    print("Messergebnis:", tmpcalib)
    user_in = input("Ergebsnis verwenden? (j/n/q)")
    if user_in == "n":
            print("Fahre fort...")
            break
    elif user_in == "j":
        # Homogener Untergrund  - Abweichung zum Mittelwert = Kalibrier-Werte
        messung = np.array(tmpcalib)
        # Prozentuale Verrechnung ginge auch:
        ir_calib = messung.mean() / messung
        print("kalibrier0:",ir_calib)
        # Nehmen jetzt den Mittelwert und subtrahieren diesen später
        ir_calib = messung.mean()
        print("kalibrier1:",ir_calib)
        ir_calib = ir_calib.round(4)
        print("kalibrier2:",ir_calib)
        data = {}
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
        except:
            print("Read File error ")
        data["ir_calib"] = ir_calib.tolist()
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
    
#-------------------------
# Kalirbrier-Werte aus Config lesen:
#-------------------------
print("Lese Kalibrier-Werte aus Config:")
with open("config.json", "r") as f:
    data = json.load(f)
    ir_calib = data.get("ir_calib")
    if ir_calib != None:
        ir_calib = ir_calib
    else:
        ir_calib = [1, 1, 1, 1, 1]
print("Kalibrierwert:", ir_calib)

#-------------------------
# Ausgabe der aktuellen IR Messwerte:
#-------------------------
iraverage = irm.get_average(3)
print("Average Wert ohne Kalibrierung:")  
print(iraverage)  

#-------------------------
# Ausgabe der kalibrierten IR Messwerte:
#-------------------------
# Kalibrierung verrechnung (Abweichung zum Mittelwert)
ir_messwerte = ((irm.get_average(3) - np.array(ir_calib)).round(2).tolist())
print("Avg Werte mit Kalirbrierung - Array ir_messwerte:")
print(ir_messwerte)

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

