from sensor_car import  *
from record import *

def initialisieren(ir):
    """ Initialisieren der IR Sensoren
        Args:
            (Sensor Car)
        Return: keine Rückgabe 
    """
    ir.ir_calibriation()
    messung = ir.get_ir_messung()
    winkel = ir.get_steering_angle(messung)
    print(f"Messung: {messung}")
    print(f"winkel: {winkel}")
    print(f"Wert der Kalibrierung: {ir.get_calibration()}")
    ir.steering_angle = 90
    p= input("Bitte Fzg auf die Linien setzen und Taste drücken") 


def line(ir, linie_Schwellwert = -4 ):
    """ Führt eine IR Messung durch und prüft anhand des Schwellwerts ob eine Linie vorhanden ist
        Args:
            (Sensor Car, Schwellwert)
        Return: True = Linie gefunden, Fals = keine Linie
    """
    messung = ir.get_ir_messung()
    line_found = False

    for i in messung :
        if i <= linie_Schwellwert :
            line_found = True
    return line_found


def print_ir_value(ir):
    messen = True
    while messen :
        try:
            messung = ir.get_ir_messung()
            print (f"kalibierte Messwerte : {messung}")
            time.sleep(0.3)
        except KeyboardInterrupt:
            messen=False  

def follow_line(ir, linie_Schwellwert = -4, anzahl_linien_ende = 5 ):
    """ Linie Folgen bist mehrfach(anzahl_linien_ende) keine Linie detektiert wurden 
        Args:
            (Sensor Car, Schwellwert Linie, Anzahl der Messung ohne Linienerkennung)
        Return: Der letze lenkwinkel bei dem noch ein Linie detektiert wurde
    """      
    parcour = True
    found_line = True
    no_line = 0
    letze_Lenkwinkel = 90
    while parcour and found_line:
        try: 
            messung = ir.get_ir_messung()
            ir.steering_angle = ir.get_steering_angle(messung)
            ir.drive(30, 1)

            found_line = line(ir, linie_Schwellwert)
                    
            if  not found_line:
                no_line +=1
                found_line = True
            else :
                letze_Lenkwinkel = ir.steering_angle
                no_line = 0

            if no_line >= anzahl_linien_ende:
                found_line = False
                
        except KeyboardInterrupt:
            parcour=False  
    
    ir.stop()
    ir.steering_angle = 90 
    return letze_Lenkwinkel

def fahrparcours5(ir, linie_Schwellwert = -4, anzahl_linien_ende = 5 ):
    """ Folgen einer etwas 1,5 bis 2 cm breiten Linie auf
        dem Boden. Das Auto soll stoppen, sobald das Auto das Ende der Linie erreicht hat. Als
        Test soll eine Linie genutzt werden, die sowohl eine Rechts‑ als auch eine Linkskurve
        macht. Die Kurvenradien sollen deutlich größer sein als der maximale Radius, den das
        Auto ohne ausgleichende Fahrmanöver fahren kann.
        Args:
            (Sensor Car, Schwellwert Linie, Anzahl der Messung ohne Linienerkennung)
    """      
    t = RecordingThread(ir)
    t.start()
    
    initialisieren(ir)
    letze_Winkel = follow_line(ir, linie_Schwellwert, anzahl_linien_ende)
    
    t.stop_record()
    t.join()