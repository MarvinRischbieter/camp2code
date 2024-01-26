from basisklassen import  *
from basecar import *
from sonic_car import *
from sensor_car import *
from fahrparcours1 import *
from fahrparcours2 import *
from fahrparcours3 import * 
from fahrparcours4 import *
from fahrparcours5 import *
from fahrparcours6 import *
from fahrparcours7 import *
import time

def main():
    """
    Run the selected test program based on the user's choice.

    @inoput: program_choice (int): The chosen test program number.
    """
    ausführen=True
    while ausführen:
        try:
            print("Fahrprogramme:\n   1: Parcours 1: vorwärts rückwärts\n   2: Parcours 2: Kreisfahrt\n   3: Parcours 3: Vorwärts bis Hinderniss \n   4: Parcours 4: Erkundungstour\n   5: Parcours 5: Linenverfolgung einfach\n   6: Parcours 6: Linienverfolgung komplex\n   7: Parcours 7: Linenverfolgung mit Hindernisserk.  \n   8: Print IR Werte\n   9: Abbruch ")
            p= input("Bitte wählen Sie ein Fahrprogramm : ")
            programm = int(p)
            if programm <= 0 or programm > 9:
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
                fahrparcours5(ir, -5, 15)
                time.sleep(2)
            elif programm == 6:
                ##################### Test parcours4 #########################
                ir = SensorCar()
                fahrparcours6(ir, -5, 15 )
                time.sleep(2)
            elif programm == 7:
                ir = SensorCar()
                follow_line_with_obstacle(ir)
                time.sleep(2)
            elif programm == 8:
                ir = SensorCar()
                initialisieren(ir)
                print_ir_value(ir)
            else:
                print("Goodby")
                bc = BaseCar()
                bc.steering_angle = 90
                time.sleep(2)
                ausführen=False

if __name__ == '__main__':
    main()
