from sensor_car import  *
from fahrparcours5 import  *
from record import *

def back(ir, linie_Schwellwert =-4):
    """
    back fährt rückwärts bis der Linien schwellwert erreicht ist.

    @input ir: Sensor Car
    @input linie_Schwellwert: Linien Schwellwert (default=-4)

    @output: Steuerwinkel oder wenn keine Linie gefunden wurde 90 Grad
    """
    print(f"Linie verloren. Rückwärts fahren bis zur Linie")

    found_line = False
    count_iterations = 0

    while not found_line:
        if count_iterations > 100 :
            found_line = True
        print("Fahre Rückwärts")
        ir.steering_angle = 90
        ir.drive(30, -1)
        found_line = line(ir, linie_Schwellwert)
        #time.sleep(0.1)
        winkel = ir.get_steering_angle(ir.get_ir_messung())    
        count_iterations += 1
        
    ir.stop()

    if count_iterations > 100 :
        return 90
    else :
        return winkel          
    
def back_forward(ir, linie_Schwellwert = -4, direction =1) :
    """
    back_forward fährt vorwärts und rückwärts mit entsprechenden Lenkwinkel

    @input ir: Sensor Car
    @input linie_Schwellwert: Linien Schwellwert (default=-4)
    @input direction: Kurvenrichtung (-1 = links, 1 = rechts)

    @output: True = linie gefunden, False = keine Linie
    """
    if direction == -1 :
        kurve1 = ir.max_steer_angle_right
        kurve2 = ir.max_steer_angle_left
    elif direction == 1 :
        kurve1 = ir.max_steer_angle_left
        kurve2 = ir.max_steer_angle_right
    
    line_found = False
    iterations = 0

    while not line_found :
        if iterations > 100 : 
            line_found = True
        ir.steering_angle = kurve1
        ir.drive(30, -1)
        time.sleep(0.3)
        ir.stop()
        time.sleep(0.1)
        ir.steering_angle = kurve2
        ir.drive(30, 1)
        time.sleep(0.3)
        ir.stop()
        time.sleep(0.1)
        line_found = line(ir,linie_Schwellwert)
        iterations +=1

    if iterations > 100 : 
        return False
    else :
        return True
            
def follow_line_complex(ir, linie_Schwellwert = -4, anzahl_linien_ende = 5 ):
    """
    Folgt der Linie bis keine Linie mehr detektiert werden kann.
    Wenn der letzte Lenkwinkel in dem Bereich 95-85 Grad liegt, wird das als Linienende interpretiert und abgebrochen.
    Wenn ein eindeutiger letzter Lenkwinkel identifizierbar ist, wird mit der Routine back_forward die entsprechende Kurve gefahren.

    @input ir: Sensor Car
    @input linie_Schwellwert: Linien Schwellwert (default=-4)
    @input anzahl_linien_ende: Anzahl der IR Messungen ohne Linie (default=5)
    """
    print("follwow line complex ausführen")    

    parcour = True
  
    while parcour:
        try: 
            letze_Winkel = follow_line(ir, linie_Schwellwert, anzahl_linien_ende)
            print(f"Letze Fahrrichtung : {letze_Winkel}")    
            #back(ir, linie_Schwellwert =-4)
            print(f"Letze Fahrrichtung nach Rückwärtsfahrt : {letze_Winkel}")  
            if letze_Winkel < 85 :
                print(f"Linie verloren. Kurve nach Links. Letze Winkel: {letze_Winkel}")
                parcour = back_forward(ir, linie_Schwellwert, direction = -1)   
            elif letze_Winkel > 95 :
                print(f"Linie verloren. Kurve nach rechts. Letze Winkel: {letze_Winkel}")
                parcour = back_forward(ir, linie_Schwellwert, direction = 1)
            else :            
                parcour=False   
        except KeyboardInterrupt:
            parcour=False  
            
def fahrparcours6(ir, linie_Schwellwert = -4, anzahl_linien_ende = 5 ):
    """
    Folgen einer Linie, die sowohl eine Rechts- als auch eine Linkskurve macht mit
    Kurvenradien kleiner als der maximale Lenkwinkel.

    @input ir: Sensor Car
    @input linie_Schwellwert: Linien Schwellwert (default=-4)
    @input anzahl_linien_ende: Anzahl der IR Messungen ohne Linie (default=5)
    """
    t = RecordingThread(ir)
    t.start()
    
    initialisieren(ir)
    follow_line_complex(ir, linie_Schwellwert, anzahl_linien_ende)
    
    ir.stop()
    ir.steering_angle = 90 
    t.stop_record()
    t.join()
            
            
            