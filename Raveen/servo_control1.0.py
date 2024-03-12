'''from gpiozero import AngularServo
from time import  sleep

servo = AngularServo(19,min_pulse_width=0.0006,max_pulse_width=0.0023)

while (True):
    servo.angle = 90
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.angle = -90
    sleep(2)
    '''
import RPi.GPIO as GPIO  
from time import sleep   
GPIO.setmode(GPIO.BOARD) 

GPIO.setup(19,GPIO.OUT)  
p = GPIO.PWM(19, 50)     
p.start(0)               

p.ChangeDutyCycle(3)    
sleep(1)                 
p.ChangeDutyCycle(12)   
sleep(1)

p.stop()                 
GPIO.cleanup() 
