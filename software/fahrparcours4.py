from sonic_car import *

US_THRESHOLD = 40

def fahrparcours_4(sc = SonicCar):
    print("Fahrparcours 4 startet")
    sc = SonicCar()
    sc.steering_angle = 90

    # Threshold Ultraschall zu Distance:
    while (sc.get_distance_to_obstacle() - US_THRESHOLD) > 0:
        time.sleep(0.5) # 0.5 Sek. warten, Fzg. rangiert.
        sc.drive(50, 1)
 
    if (sc.get_distance_to_obstacle() - US_THRESHOLD) <= 0:
        print("Hindernis erkennt, rangieren...")
        sc.stop()
        # Solange zurück fahren und lenken bis Distanz erreicht ist:
        while (sc.get_distance_to_obstacle() - US_THRESHOLD) < 20:
            sc.steering_angle = -48 # Max. Steering Angle
            sc.drive(50, -1) # Zurück fahren
            sc.stop()
            sc.steering_angle = 0 # Lenkung wieder gerade
    
