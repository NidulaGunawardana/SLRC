from gpiozero import AngularServo
from time import  sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo = AngularServo(19,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)

while (True):
    # servo.angle = 90
    # sleep(2)
    # servo.angle = 0
    # sleep(2)
    # servo.angle = -90
    # sleep(2)
    for i in range(-90,40,1):
        servo.angle = i
        print(i)
        sleep(0.01)
        
    
    for i in range(40,-90,-1):
        servo.angle = i
        print(i)
        sleep(0.01)
    # servo.angle = 30
    # sleep(2)
    # servo.angle = 35
    # sleep(2)
    # servo.angle = 32
    # sleep(2)
    # servo.angle = 29
    # sleep(2.5)
    # servo.angle = 32
    # sleep(2)


 ########################################################################
    ######Code2##############   
"""
import RPi.GPIO as GPIO  
from time import sleep   
GPIO.setmode(GPIO.BCM) 

GPIO.setup(19,GPIO.OUT)  
pwm = GPIO.PWM(19, 100)     
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(19, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(19, False)
	pwm.ChangeDutyCycle(0)

while(True):
    SetAngle(90)
    sleep(1)
    SetAngle(0)
    sleep(1)
    SetAngle(-90)
    sleep(1)

    
pwm.stop()                 
GPIO.cleanup() 
"""