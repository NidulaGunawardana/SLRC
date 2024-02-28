import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23, GPIO.OUT)
pwm = GPIO.PWM(23, 100)
pwm.start(20)

while True:
    for dc in range(101):
        pwm.ChangeDutyCycle(dc)

        sleep(0.01)
        
    for dc in range(100,0,-1):
        pwm.ChangeDutyCycle(dc)

        sleep(0.01)
    
