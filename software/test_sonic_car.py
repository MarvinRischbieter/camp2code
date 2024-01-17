from sonic_car import *

US_THRESHOLD = 20

def main():
    sc = SonicCar()
    sc.make_measures() # 100 Mal

    distance_obs = sc.get_distance_to_obstacle() # 1 Mal
    print(f'distance: {distance_obs}')


def road_4():
    print("Fahrparcours 4 startet")
    sc = SonicCar()

    # Threshold Ultraschall zu Distance:
    while (sc.get_distance_to_obstacle() - US_THRESHOLD) > 0:
        time.sleep(1) # 1 Sek. warten, Fzg. rangiert.
        sc.drive(50, 1)
 
    if (sc.get_distance_to_obstacle() - US_THRESHOLD) <= 0:
        print("Hindernis erkennt, rangieren...")
        sc.stop()
        # Solange zurück fahren und lenken bis Distanz erreicht ist:
        while (sc.get_distance_to_obstacle() - US_THRESHOLD) > 20:
            sc.steering_angle = -40 # Max. Steering Angle
            sc.drive(50, -1) # Zurück fahren
            sc.stop()
            sc.steering_angle = 0 # Lenkung wieder gerade
    


if __name__ == '__main__':
    main()
