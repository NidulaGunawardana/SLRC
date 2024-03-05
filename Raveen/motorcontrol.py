import RPi.GPIO as GPIO
from time import sleep

rightMotor11 = 6
rightMotor12 = 13
rightPWM1 = 5

rightMotor11 = 16
rightMotor12 = 20
rightPWM2 = 12

leftMotor1 = 27
leftMotor2 = 22
leftPWM1 = 17

leftMotor1 = 10
leftMotor2 = 9
leftPWM2 = 11

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(rightMotor11, GPIO.OUT)
GPIO.setup(rightMotor12, GPIO.OUT)
GPIO.setup(rightPWM1, GPIO.OUT)
GPIO.setup(leftMotor11, GPIO.OUT)
GPIO.setup(leftMotor12, GPIO.OUT)
GPIO.setup(leftPWM1, GPIO.OUT)

GPIO.setup(rightMotor21, GPIO.OUT)
GPIO.setup(rightMotor22, GPIO.OUT)
GPIO.setup(rightPWM2, GPIO.OUT)
GPIO.setup(leftMotor21, GPIO.OUT)
GPIO.setup(leftMotor22, GPIO.OUT)
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
        GPIO.output(rightMotor11,GPIO.HIGH)
        GPIO.output(rightMotor12,GPIO.LOW)

        GPIO.output(leftMotor12,GPIO.HIGH)
        GPIO.output(leftMotor12,GPIO.LOW)

        GPIO.output(rightMotor21,GPIO.HIGH)
        GPIO.output(rightMotor22,GPIO.LOW)

        GPIO.output(leftMotor12,GPIO.HIGH)
        GPIO.output(leftMotor12,GPIO.LOW)

        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)
        pwm3.ChangeDutyCycle(duty)
        pwm4.ChangeDutyCycle(duty)

        sleep(0.05)

def turnright(duty):
        pwm1 = GPIO.PWM(rightPWM, 100)
        pwm2 = GPIO.PWM(leftPWM,100)
        pwm3 = GPIO.PWM(rightPWM, 100)
        pwm4 = GPIO.PWM(leftPWM,100)
        pwm1.start(duty)
        pwm2.start(duty)
        pwm3.start(duty)
        pwm4.start(duty)
        while True:
            GPIO.output(rightMotor11,GPIO.HIGH)
            GPIO.output(rightMotor12,GPIO.LOW)

            GPIO.output(leftMotor12,GPIO.HIGH)
            GPIO.output(leftMotor12,GPIO.LOW)

            GPIO.output(rightMotor21,GPIO.HIGH)
            GPIO.output(rightMotor22,GPIO.LOW)

            GPIO.output(leftMotor12,GPIO.HIGH)
            GPIO.output(leftMotor12,GPIO.LOW)

            pwm1.ChangeDutyCycle(duty)
            pwm2.ChangeDutyCycle(duty)
            pwm3.ChangeDutyCycle(duty)
            pwm4.ChangeDutyCycle(duty)

            sleep(0.05)
def goforward(duty):
    pwm1 = GPIO.PWM(rightPWM, 100)
    pwm2 = GPIO.PWM(leftPWM,100)
    pwm3 = GPIO.PWM(rightPWM, 100)
    pwm4 = GPIO.PWM(leftPWM,100)
    pwm1.start(duty)
    pwm2.start(duty)
    pwm3.start(duty)
    pwm4.start(duty)
    while True:
        GPIO.output(rightMotor11,GPIO.HIGH)
        GPIO.output(rightMotor12,GPIO.LOW)

        GPIO.output(leftMotor12,GPIO.HIGH)
        GPIO.output(leftMotor12,GPIO.LOW)

        GPIO.output(rightMotor21,GPIO.HIGH)
        GPIO.output(rightMotor22,GPIO.LOW)

        GPIO.output(leftMotor12,GPIO.HIGH)
        GPIO.output(leftMotor12,GPIO.LOW)

        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)
        pwm3.ChangeDutyCycle(duty)
        pwm4.ChangeDutyCycle(duty)

        sleep(0.05)
def goBackward(duty):
    pwm1 = GPIO.PWM(rightPWM, 100)
    pwm2 = GPIO.PWM(leftPWM,100)
    pwm3 = GPIO.PWM(rightPWM, 100)
    pwm4 = GPIO.PWM(leftPWM,100)
    pwm1.start(duty)
    pwm2.start(duty)
    pwm3.start(duty)
    pwm4.start(duty)
    while True:
        GPIO.output(rightMotor11,GPIO.HIGH)
        GPIO.output(rightMotor12,GPIO.LOW)

        GPIO.output(leftMotor12,GPIO.HIGH)
        GPIO.output(leftMotor12,GPIO.LOW)

        GPIO.output(rightMotor21,GPIO.HIGH)
        GPIO.output(rightMotor22,GPIO.LOW)

        GPIO.output(leftMotor12,GPIO.HIGH)
        GPIO.output(leftMotor12,GPIO.LOW)

        pwm1.ChangeDutyCycle(duty)
        pwm2.ChangeDutyCycle(duty)
        pwm3.ChangeDutyCycle(duty)
        pwm4.ChangeDutyCycle(duty)

        sleep(0.05)