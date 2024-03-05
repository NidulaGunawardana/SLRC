import RPi.GPIO as GPIO
from time import sleep

rightFront1 = 6
rightFront2 = 13
rightPWM1 = 5

rightBack1 = 20
rightBack2 = 16
rightPWM2 = 12

leftFront2 = 24
leftFront1 = 23
leftPWM1 = 18

leftBack1 = 10
leftBack2 = 9
leftPWM2 = 11

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(rightFront1, GPIO.OUT)
GPIO.setup(rightFront2, GPIO.OUT)
GPIO.setup(rightPWM1, GPIO.OUT)
GPIO.setup(leftFront2, GPIO.OUT)
GPIO.setup(leftFront1, GPIO.OUT)
GPIO.setup(leftPWM1, GPIO.OUT)

GPIO.setup(rightBack1, GPIO.OUT)
GPIO.setup(rightBack2, GPIO.OUT)
GPIO.setup(rightPWM2, GPIO.OUT)
GPIO.setup(leftBack1, GPIO.OUT)
GPIO.setup(leftBack2, GPIO.OUT)
GPIO.setup(leftPWM2, GPIO.OUT)


def turnleft(duty):
    pwm1 = GPIO.PWM(rightPWM1, 100)
    pwm2 = GPIO.PWM(leftPWM2,100)
    pwm3 = GPIO.PWM(rightPWM1, 100)
    pwm4 = GPIO.PWM(leftPWM2,100)
    pwm1.start(duty)
    pwm2.start(duty)
    pwm3.start(duty)
    pwm4.start(duty)
    while True:
        GPIO.output(rightFront1,GPIO.HIGH)
        GPIO.output(rightFront2,GPIO.LOW)

        GPIO.output(leftFront1,GPIO.HIGH)
        GPIO.output(leftFront1,GPIO.LOW)

        GPIO.output(rightBack1,GPIO.HIGH)
        GPIO.output(rightBack2,GPIO.LOW)

        GPIO.output(leftFront1,GPIO.HIGH)
        GPIO.output(leftFront1,GPIO.LOW)

        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)
        pwm3.ChangeDutyCycle(duty)
        pwm4.ChangeDutyCycle(duty)

        sleep(0.05)

def turnright(duty):
        pwm1 = GPIO.PWM(rightPWM1, 100)
        pwm2 = GPIO.PWM(leftPWM1,100)
        pwm3 = GPIO.PWM(rightPWM2, 100)
        pwm4 = GPIO.PWM(leftPWM2,100)
        pwm1.start(duty)
        pwm2.start(duty)
        pwm3.start(duty)
        pwm4.start(duty)
        while True:
            GPIO.output(rightFront1,GPIO.HIGH)
            GPIO.output(rightFront2,GPIO.LOW)

            GPIO.output(leftFront1,GPIO.HIGH)
            GPIO.output(leftFront1,GPIO.LOW)

            GPIO.output(rightBack1,GPIO.HIGH)
            GPIO.output(rightBack2,GPIO.LOW)

            GPIO.output(leftFront1,GPIO.HIGH)
            GPIO.output(leftFront1,GPIO.LOW)

            pwm1.ChangeDutyCycle(duty)
            pwm2.ChangeDutyCycle(duty)
            pwm3.ChangeDutyCycle(duty)
            pwm4.ChangeDutyCycle(duty)

            sleep(0.05)
def goforward(duty):
    pwm1 = GPIO.PWM(rightPWM1, 100)
    pwm2 = GPIO.PWM(leftPWM1,100)
    pwm3 = GPIO.PWM(rightPWM1, 100)
    pwm4 = GPIO.PWM(leftPWM2,100)
    pwm1.start(0)
    pwm2.start(0)
    pwm3.start(0)
    pwm4.start(0)
    while True:
        GPIO.output(rightFront1,GPIO.HIGH)
        GPIO.output(rightFront2,GPIO.LOW)

        GPIO.output(leftFront2,GPIO.HIGH)
        GPIO.output(leftFront1,GPIO.LOW)

        GPIO.output(rightBack1,GPIO.HIGH)
        GPIO.output(rightBack2,GPIO.LOW)

        GPIO.output(leftBack1,GPIO.HIGH)
        GPIO.output(leftBack2,GPIO.LOW)

        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)
        pwm3.ChangeDutyCycle(duty)
        pwm4.ChangeDutyCycle(duty)

        sleep(0.05)
def goBackward(duty):
    pwm1 = GPIO.PWM(rightPWM1, 100)
    pwm2 = GPIO.PWM(leftPWM1,100)
    pwm3 = GPIO.PWM(rightPWM2, 100)
    pwm4 = GPIO.PWM(leftPWM2,100)
    pwm1.start(0)
    pwm2.start(0)
    pwm3.start(0)
    pwm4.start(0)
    while True:
        GPIO.output(rightFront1,GPIO.HIGH)
        GPIO.output(rightFront2,GPIO.LOW)

        GPIO.output(leftFront1,GPIO.HIGH)
        GPIO.output(leftFront1,GPIO.LOW)

        GPIO.output(rightBack1,GPIO.HIGH)
        GPIO.output(rightBack2,GPIO.LOW)

        GPIO.output(leftFront1,GPIO.HIGH)
        GPIO.output(leftFront1,GPIO.LOW)

        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)
        pwm3.ChangeDutyCycle(duty)
        pwm4.ChangeDutyCycle(duty)

        sleep(0.05)

goforward(50)