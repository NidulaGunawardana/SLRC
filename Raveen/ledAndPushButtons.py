import RPi.GPIO as GPIO
from time import sleep

led1 = 8 #green led
led2 = 7 #blue led
pb = 4 #push botton

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(pb, GPIO.IN)
#led3 = 25


#led4 = 22

def led_on(color):
    if(color == "green"):
        GPIO.output(led1,GPIO.HIGH)   #green led on
    
    if(color == "blue"):
        GPIO.output(led2,GPIO.HIGH)   #blue led on
        
def led_off(color):
    if(color == "green"):
        GPIO.output(led1,GPIO.LOW)   #green led on
    
    if(color == "blue"):
        GPIO.output(led2,GPIO.LOW)   #blue led on
    
def push_button():
    if(GPIO.input(pb) == True):
        return 1
    else:
        return 0

