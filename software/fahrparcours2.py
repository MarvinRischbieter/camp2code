from basecar import  *
import time 

bc = BaseCar()

#Fahrt im Uhrzeigersinn
bc.drive(50,1)
print(bc.direction)
time.sleep(1)
bc.steering_angle = 135
time.sleep(8)
bc.stop()
time.sleep(2)
bc.drive(50,-1)
time.sleep(8)
bc.steering_angle = 90
time.sleep(1)
bc.stop()
#Fahrt gegen den Uhrzeigersinn
bc.drive(50,1)
print(bc.direction)
time.sleep(1)
bc.steering_angle = 45
time.sleep(8)
bc.stop()
time.sleep(2)
bc.drive(50,-1)
time.sleep(8)
bc.steering_angle = 90
time.sleep(1)
bc.stop()