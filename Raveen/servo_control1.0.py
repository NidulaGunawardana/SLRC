from gpiozero import AngularServo
from time import  sleep

servo = AngularServo(19,min_pulse_width=0.0006,max_pulse_width=0.0023)

while (True):
    for i in range(-90,90,1):
        servo.angle = i
        sleep(1) 
        
    for i in range(90,-90,-1):
        servo.angle = i
        sleep(1)     
    