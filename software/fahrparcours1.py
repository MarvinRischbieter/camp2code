from basecar import  *

def fahrparcours1(bc):
    """
    Das Auto fährt mit langsamer Geschwindigkeit 3 Sekunden geradeaus,
    stoppt für 1 Sekunde und fährt 3 Sekunden rückwärts.
    
    :param: bc: BaseCar
    @output: Keine Rückgabe
    """
    print("Fahrparcours 1 startet")

    bc.steering_angle = 90
    bc.drive(bc.speed_approach, 1)
    time.sleep(3)

    bc.stop()
    time.sleep(1)

    bc.steering_angle = 90
    bc.drive(bc.speed_approach, -1)
    time.sleep(3)
    print("Fahrparcours 1 beendet")
    bc.stop()
    bc.steering_angle = 90
