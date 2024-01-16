from basecar import  *

def main():
    """Function for testing the base classes


    Args:
        modus (int): The mode that can be choosen by the user
    """
    print("Fahrparcours 1 startet")
    bc = BaseCar()
    bc.drive(50, 1)
    time.sleep(3)
    # Stop 1 Sek
    bc.stop()
    time.sleep(1)
    # Rueckwaerts 3sec
    bc.drive(50, -1)
    time.sleep(3)
    print("Fahrparcours 1 beendet")
    bc.stop()



if __name__ == '__main__':
    main()
