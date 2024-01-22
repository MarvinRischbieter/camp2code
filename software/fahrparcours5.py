from sensor_car import  *
from record import *

def follow_line(ir, linie_Schwellwert = -4, anzahl_linien_ende = 5 ):
    
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
    linie = True
    keine_linie = 0
    while parcour and linie:
        try: 
            ir.drive(30, 1)
            messung = ir.get_ir_messung()
            print (messung)
            ir.steering_angle = ir.get_steering_angle(messung)
            
            linie = False
            for i in messung :
                #print (f"Sensorwert: {i}")
                if i <= linie_Schwellwert :
                    linie = True
                    keine_linie = 0
            if  not linie:
                keine_linie +=1
                linie = True
                print("keine Linie")
            if keine_linie >= anzahl_linien_ende:
                linie = False
                print("Linien Ende erreicht")
                
        except KeyboardInterrupt:
            parcour=False  
    ir.stop()
    ir.steering_angle = 90 # Lenkung wieder gerade
    t.stop_record()
    t.join()