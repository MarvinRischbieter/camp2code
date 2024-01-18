###
# Infrarod Sensor zu Steering angle
###
from basisklassen import  *
from basecar import *

import numpy as np

class SensorCar():

    # Initialisierung der Klasse SensorCar.
    def __init__(self):
        # Infrared Klasse einlesen:
        self.ir = Infrared()

    @property
    def ir_analog(self):
        # Analogwerte der 5 IR-Sensoren auslesen mit Durschnitt aus 10 Messungen
        # Ausgabe als Liste
        self._ir_analog = (self.ir.get_average(10))
        return self._ir_analog
    
    def ir_normalize(arr, t_min, t_max):
        # IR Messung auf eine range t_min und t_max normieren
        # Aufruf in ir_to_steering
        ir_normalized = []
        diff = t_max - t_min
        diff_arr = max(arr) - min(arr)
        for i in arr:
            temp = (((i - min(arr))*diff)/diff_arr) + t_min
            ir_normalized.append(temp)
            return ir_normalized
      
    def ir_to_steering(self):
        # Lookup Table steering angle to IR-value
        # np.arange(start=-10, stop=10, step=0.5)
       
        self._ir_to_sa = {
            -2: -45,
            -1.5: -33.75,
            -1: -22.5,
            -0.5: -11.25,
            0: 0,
            0.5: 11.25,
            1: 22.5,
            1.5: 33.75,
            2: 45,
            }
        # IR Analog-Werte als Array:
        ir_messwerte = np.array(self.ir_analog)
                
        # auf Max. Wert normieren ("prozentual")
        ir_normiert = ir_messwerte / np.max(ir_messwerte) * 100
        
        # auf Bereich der Übertragungsfunktion (umwandeln:
        ir_range_to_normalize = (-2,2)
        
        # Funktion zum normilisieren aufrufen:
        ir_normal = ir_normalize(ir_normiert,
                                 ir_range_to_normalize[0],
                                 ir_range_to_normalize[1])
                
        # Die summe der 5 analogen Messwerte müsste die Lager der Linie sein
        # Bei Summe 0 sollte Linie mittig sein
        ir_summe = np.sum(ir_normal)
        
        # Lenkwinkel auf Basis der Übertragungsfunktion:
        self._ir_steering_angle = self._ir_to_sa.get(ir_summe)
        return self._ir_steering_angle
