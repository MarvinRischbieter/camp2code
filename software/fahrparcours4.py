from sonic_car import *
from fahrparcours3 import *

US_THRESHOLD = 40

def fahrparcours_4(sc = SonicCar()):
    print("Fahrparcours 4 startet")
    # sc = SonicCar()
    sc.steering_angle = 90

    # Threshold Ultraschall zu Distance:
    parcour = True
    while parcour:
        '''
        distance = sc.get_distance_to_obstacle()
        if distance > US_THRESHOLD:
            sc.drive(50, 1)
            time.sleep(0.5) # 0.5 Sek. warten, Fzg. rangiert.
            continue
        elif distance <= US_THRESHOLD or distance == 1000:
        '''
        drive_until_obstacle(sc)
        print("Hindernis erkennt, rangieren...")
        # Solange zurück fahren und lenken bis Distanz erreicht ist:
        while sc.get_distance_to_obstacle() < US_THRESHOLD + 20:
            sc.steering_angle = -48 # Max. Steering Angle
            sc.drive(50, -1) # Zurück fahren
            time.sleep(1)
        sc.stop()
        sc.steering_angle = 90 # Lenkung wieder gerade
