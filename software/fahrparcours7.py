from sensor_car import  *
from record import *

def follow_line_with_obstacle(ir, min_distance=5, max_distance=50, speed_min=20, speed_max=30 ):
    
    t = RecordingThread(ir)
    t.start()
    
    ir.ir_calibriation()
    messung = ir.get_ir_messung()
    winkel = ir.get_steering_angle(messung)
    print(f"Messung: {messung}")
    print(f"winkel: {winkel}")
    print(f"Wert der Kalibrierung: {ir.get_calibration()}")
    ir.steering_angle = 90
    p= input("Bitte Fzg auf die Linien setzen und Taste drücken") 
         
    parcour = True
    speed = speed_max
    
    while parcour:
        try:
            distance_to_obstacle = ir.get_distance_to_obstacle()
            if distance_to_obstacle <= min_distance:
               print("Hindernis erkannt! Stopping...")
               ir.stop()
               parcour = False
               break
            
            if distance_to_obstacle <= max_distance or distance_to_obstacle == 1000 :
                print("Hindernis erkannt! langsamer...")
                speed = speed_min
            else:
                speed = speed_max
                
            ir.drive(speed, 1)
            messung = ir.get_ir_messung()
            ir.steering_angle = ir.get_steering_angle(messung)
        except KeyboardInterrupt:
            parcour=False  

    ir.stop()
    ir.steering_angle = 90 
    t.stop_record()
    t.join()