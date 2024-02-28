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


def turnleft(duty):
    pwm1 = GPIO.PWM(rightPWM, 100)
    pwm2 = GPIO.PWM(leftPWM,100)
    pwm1.start(duty)
    pwm2.start(duty)
    while True:
        GPIO.output(rightMotor1,GPIO.HIGH)
        GPIO.output(rightMotor2,GPIO.LOW)

        GPIO.output(leftMotor1,GPIO.HIGH)
        GPIO.output(leftMotor2,GPIO.LOW)
        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)

        sleep(0.05)

def turnright(duty):
    pwm1 = GPIO.PWM(rightPWM, 100)
    pwm2 = GPIO.PWM(leftPWM,100)
    pwm1.start(duty)
    pwm2.start(duty)
    while True:
        GPIO.output(rightMotor1,GPIO.HIGH)
        GPIO.output(rightMotor2,GPIO.LOW)

        GPIO.output(leftMotor1,GPIO.HIGH)
        GPIO.output(leftMotor2,GPIO.LOW)
        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)

        sleep(0.05)
            
def goforward(duty):
    pwm1 = GPIO.PWM(rightPWM, 100)
    pwm2 = GPIO.PWM(leftPWM,100)
    pwm1.start(duty)
    pwm2.start(duty)
    while True:
        GPIO.output(rightMotor1,GPIO.HIGH)
        GPIO.output(rightMotor2,GPIO.LOW)

        GPIO.output(leftMotor1,GPIO.HIGH)
        GPIO.output(leftMotor2,GPIO.LOW)
        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)

        sleep(0.05)
        
def goBackward(duty):
    pwm1 = GPIO.PWM(rightPWM, 100)
    pwm2 = GPIO.PWM(leftPWM,100)
    pwm1.start(duty)
    pwm2.start(duty)
    while True:
        GPIO.output(rightMotor1,GPIO.HIGH)
        GPIO.output(rightMotor2,GPIO.LOW)

        GPIO.output(leftMotor1,GPIO.HIGH)
        GPIO.output(leftMotor2,GPIO.LOW)
        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)

        sleep(0.05)