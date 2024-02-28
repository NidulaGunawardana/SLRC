import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(20)

for dc in range(101):
    pwm.ChangeDutyCycle(dc)
    print(dc)
    sleep(0.01)
