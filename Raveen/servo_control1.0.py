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
