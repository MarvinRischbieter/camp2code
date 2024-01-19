from basecar import  *

def fahrparcours2(bc = BaseCar):
    """Das Auto fährt 1 Sekunde geradeaus,
dann für 8 Sekunden mit maximalen Lenkwinkel im Uhrzeigersinn und stoppt.
Dann soll das Auto diesen Fahrplan in umgekehrter Weise abfahren und an den Ausgangspunkt
zurückkehren. Die Vorgehensweise soll für eine Fahrt im entgegengesetzten Uhrzeigersinn
wiederholt werden.
    Args:
        ()
    """
    print("Fahrparcours 2 kurve im Uhrzeigersinn vorwärts")
    #bc = BaseCar()
    bc.steering_angle = bc.max_steer_angle_right
    bc.drive(50, 1)
    time.sleep(8)
    bc.stop()
    print("Fahrparcours 2 kurve im Uhrzeigersinn rückwärts")
    bc.steering_angle = bc.max_steer_angle_right
    bc.drive(50, -1)
    time.sleep(8)
    bc.stop()
    time.sleep(2)
    print("Fahrparcours 2 kurve gegen den Uhrzeigersinn vorwärts")
    bc = BaseCar()
    bc.steering_angle = bc.max_steer_angle_left
    bc.drive(50, 1)
    time.sleep(8)
    bc.stop()
    print("Fahrparcours 2 kurve gegen den Uhrzeigersinn rückwärts")
    bc.steering_angle = bc.max_steer_angle_left
    bc.drive(50, -1)
    time.sleep(8)
    bc.stop()
    bc.steering_angle = 90
    print("Fahrparcours 2 beendet")
    time.sleep(5)