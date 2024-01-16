#from basisklassen import  *
from basecar import *
import traceback
import time

def main():
    """Function for testing the base classes


    Args:
        modus (int): The mode that can be choosen by the user
    """
    bc = BaseCar()
    bc.steering_angle = 0
    print (bc.steering_angle)
    time.sleep(2)
    bc.steering_angle = 122
    print (bc.steering_angle)
    time.sleep(2)
    bc.steering_angle = 90
    print (bc.steering_angle)
    time.sleep(2)
    bc.speed = 50
    print (f"Geschwindigkeit : {bc.speed}")
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
    
    #bc.steer(45)
    #bc.drive_fw(20)
    #print('Drehung nach links')
    #time.sleep(.5)
    #bc.steer(90)
    #bc.drive_stop()
    
    
if __name__ == '__main__':
    main()
