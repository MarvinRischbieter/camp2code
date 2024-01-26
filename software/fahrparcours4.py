from sonic_car import *
from fahrparcours3 import *
from record import *

US_THRESHOLD = 40

def fahrparcours_4(sc):
    '''
    Erkundungstour, variieren der Fahrtrichtung und der Geschwindigkeit. 
    Bei Hindernis soll die Fahrtrichtung geändert werden, bei Änderung der Fahrtrichtung
    Maximaler Lenkwinkel und Rückwärtsfahren.
    
    @input sc: SonicCar
    @output: Keine Rückgabe
    '''
    print("Fahrparcours 4 startet")
    t = RecordingThread(sc)
    t.start()
    
    sc.steering_angle = 90
    parcour = True

    while parcour:
        try:       
            drive_until_obstacle(sc)
            print("Hindernis erkennt, rangieren...")

            while sc.get_distance_to_obstacle() < US_THRESHOLD + 20:
                sc.steering_angle = -48 
                sc.drive(50, -1) 
                time.sleep(1)
            sc.stop()
            sc.steering_angle = 90 

        except KeyboardInterrupt:
            parcour=False     

    sc.stop()
    sc.steering_angle = 90 
    t.stop_record()
    t.join()

       