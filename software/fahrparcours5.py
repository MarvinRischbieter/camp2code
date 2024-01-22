from sensor_car import  *
from record import *

def follow_line(ir):
    
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
    while parcour:
        try: 
            ir.drive(30, 1)
            messung = ir.get_ir_messung()
            ir.steering_angle = ir.get_steering_angle(messung)
        except KeyboardInterrupt:
            parcour=False  
    ir.stop()
    ir.steering_angle = 90 # Lenkung wieder gerade
    t.stop_record()
    t.join()