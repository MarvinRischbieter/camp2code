from basisklassen import  *
from basecar import *
from sonic_car import *
from sensor_car import *
from fahrparcours1 import *
from fahrparcours2 import *
from fahrparcours3 import * 
from fahrparcours4 import *
from fahrparcours5 import *
from fahrparcours7 import *
import os
import traceback
import time

def main():
    """Function for testing the base classes


    Args:
        modus (int): The mode that can be choosen by the user
    """
    ausführen=True
    while ausführen:
        try:
            print("Fahrprogramme:\n   1: Parcours 1: vorwärts rückwärts\n   2: Parcours 2: Kreisfahrt\n   3: Parcours 3: Vorwärts bis Hinderniss \n   4: Parcours 4: Erkundungstour\n   5: Parcours 5: Linenverfolgung \n   6: Parcours 6: Linenverfolgung mit Hindernisserk.  \n   7: Abbruch ")
            p= input("Bitte wählen Sie ein Fahrprogramm : ")
            programm = int(p)
            if programm <= 0 or programm > 7:
                print("Bitte 5einen nummerischen Wert im Wertebereich eingeben")
                time.sleep(2)
                continue
        except:     
            print("Bitte 5einen nummerischen Wert im Wertebereich eingeben")
            time.sleep(2)
            continue
        else:

            if programm == 1:
                bc = BaseCar()
                fahrparcours1(bc)
                time.sleep(2)
            elif programm == 2:
                bc = BaseCar()
                fahrparcours2(bc)
                time.sleep(2)
            elif programm == 3:
                ###################### Test parcours1 #########################
                sc = SonicCar()
                drive_until_obstacle(sc)
                time.sleep(2)
            elif programm == 4:
                ###################### Test parcours2 #########################
                sc = SonicCar()
                fahrparcours_4(sc)
                time.sleep(2)
            elif programm == 5:
                ##################### Test parcours3 #########################
                ir = SensorCar()
                follow_line(ir,-3, 5)
                time.sleep(2)
            elif programm == 6:
                ##################### Test parcours4 #########################
                ir = SensorCar()
                follow_line_with_obstacle(ir)
                time.sleep(2)
            else:
                print("Goodby")
                bc = BaseCar()
                bc.steering_angle = 90
                time.sleep(2)
                ausführen=False

    
if __name__ == '__main__':
    main()
