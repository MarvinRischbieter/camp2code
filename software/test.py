from basisklassen import  *
from basecar import *
from sonic_car import *
from sensor_car import *
from fahrparcours1 import *
from fahrparcours2 import *
from fahrparcours3 import * 
from fahrparcours4 import *
from fahrparcours5 import *
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
            print("Fahrprogramme:\n   1: diverse BaseCar\n   2: Test SonicCar\n   3: Test Parcours 1\n   4: Test Parcours 2\n   5: Test Parcours 3\n   6: Test Parcours 4 \n   7: Test Parcours 5 \n   8: Abbruch ")
            p= input("Bitte wählen Sie ein Fahrprogramm : ")
            programm = int(p)
            if programm <= 0 or programm > 8:
                print("Bitte 5einen nummerischen Wert im Wertebereich eingeben")
                time.sleep(2)
                continue
        except:     
            print("Bitte 5einen nummerischen Wert im Wertebereich eingeben")
            time.sleep(2)
            continue
        else:

            if programm == 1:
                #################### Test Base Car #########################     
                bc = BaseCar()
                bc.steering_angle = 45
                print (bc.steering_angle)
                time.sleep(2)
                bc.steering_angle = 135
                print (bc.steering_angle)
                time.sleep(2)
                bc.steering_angle = 90
                print (bc.steering_angle)
                time.sleep(2)
                bc.speed = 50
                print (f"Geschwindigkeit : {bc.speed}")
                time.sleep(2)
                bc.speed = 0
                time.sleep(2)
                bc.drive(50, 1)
                time.sleep(2)
                bc.stop()
                time.sleep(2)
                bc.drive(300, -1)
                time.sleep(2)
                bc.stop()
                bc.drive(-300, -1)
                time.sleep(2)
                bc.stop()
            elif programm == 2:
                ##################### Test Sonic Car #########################
                sc = SonicCar()
                sc.steering_angle = 45
                print (sc.steering_angle)
                time.sleep(2)
                sc.steering_angle = 135
                print (sc.steering_angle)
                time.sleep(2)
                sc.steering_angle = 90
                print (sc.steering_angle)
                time.sleep(2)
                #sc.make_measures() # 100 Mal
                #distance_obs = sc.get_distance_to_obstacle() # 1 Mal
                #print(f'distance: {distance_obs}')
            elif programm == 3:
                ###################### Test parcours1 #########################
                bc = BaseCar()
                fahrparcours1(bc)
                time.sleep(2)
            elif programm == 4:
                ###################### Test parcours2 #########################
                bc = BaseCar()
                fahrparcours2(bc)
                time.sleep(2)
            elif programm == 5:
                ##################### Test parcours3 #########################
                sc = SonicCar()
                drive_until_obstacle(sc)
                time.sleep(2)
            elif programm == 6:
                ##################### Test parcours4 #########################
                sc = SonicCar()
                fahrparcours_4(sc)
                time.sleep(2)
            elif programm == 7:
                ##################### Test parcours4 #########################
                ir = SensorCar()
                follow_line(ir)
                time.sleep(2)
            else:
                print("Goodby")
                bc = BaseCar()
                bc.steering_angle = 90
                time.sleep(2)
                ausführen=False

    
if __name__ == '__main__':
    main()
