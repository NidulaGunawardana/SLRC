import RPi.GPIO as GPIO
from time import sleep

rightMotor1 = 23
rightMotor2 = 24
rightPWM = 18

leftMotor1 = 16
leftMotor2 = 20
leftPWM = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(rightMotor1, GPIO.OUT)
GPIO.setup(rightMotor2, GPIO.OUT)
GPIO.setup(rightPWM, GPIO.OUT)
GPIO.setup(leftMotor1, GPIO.OUT)
GPIO.setup(leftMotor2, GPIO.OUT)
GPIO.setup(leftPWM, GPIO.OUT)



pwm1 = GPIO.PWM(rightPWM, 100)
pwm2 = GPIO.PWM(leftPWM,100)
pwm1.start(0)
pwm2.start(0)

while True:
    GPIO.output(rightMotor1,GPIO.HIGH)
    GPIO.output(rightMotor2,GPIO.LOW)

    GPIO.output(rightMotor1,GPIO.HIGH)
    GPIO.output(rightMotor2,GPIO.LOW)

    for dc in range(101):
        pwm1.ChangeDutyCycle(dc)
        pwm2.ChangeDutyCycle(dc)

        sleep(0.01)
        
    for dc in range(100,0,-1):
        pwm1.ChangeDutyCycle(dc)
        pwm2.ChangeDutyCycle(dc)

        sleep(0.01)

