import RPi.GPIO as GPIO
from time import sleep
import tty, sys, termios

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
x = 0


rightFront1 = 6
rightFront2 = 13
rightPWM1 = 5

rightBack1 = 20
rightBack2 = 16
rightPWM2 = 12

leftBack2 = 24
leftBack1 = 23
leftPWM1 = 18

leftFront1 = 10
leftFront22 = 9
leftPWM2 = 11

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(rightFront1, GPIO.OUT)
GPIO.setup(rightFront2, GPIO.OUT)
GPIO.setup(rightPWM1, GPIO.OUT)

GPIO.setup(leftBack2, GPIO.OUT)
GPIO.setup(leftBack1, GPIO.OUT)
GPIO.setup(leftPWM1, GPIO.OUT)

GPIO.setup(rightBack1, GPIO.OUT)
GPIO.setup(rightBack2, GPIO.OUT)
GPIO.setup(rightPWM2, GPIO.OUT)

GPIO.setup(leftFront1, GPIO.OUT)
GPIO.setup(leftFront22, GPIO.OUT)
GPIO.setup(leftPWM2, GPIO.OUT)

pwm1 = GPIO.PWM(rightPWM1, 100)
pwm2 = GPIO.PWM(leftPWM1,100)
pwm3 = GPIO.PWM(rightPWM2, 100)
pwm4 = GPIO.PWM(leftPWM2,100)
pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)

def goLeft(duty):
    GPIO.output(rightFront1,GPIO.HIGH)
    GPIO.output(rightFront2,GPIO.LOW)

    GPIO.output(leftBack2,GPIO.HIGH)
    GPIO.output(leftBack1,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.LOW)
    GPIO.output(rightBack2,GPIO.HIGH)

    GPIO.output(leftFront1,GPIO.HIGH)
    GPIO.output(leftFront22,GPIO.LOW)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty)

    #sleep(0.05)

def goRight(duty):
    GPIO.output(rightFront1,GPIO.LOW)
    GPIO.output(rightFront2,GPIO.HIGH)

    GPIO.output(leftBack1,GPIO.HIGH)
    GPIO.output(leftBack2,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.HIGH)
    GPIO.output(rightBack2,GPIO.LOW)

    GPIO.output(leftFront1,GPIO.LOW)
    GPIO.output(leftFront22,GPIO.HIGH)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty)

    #sleep(0.05)

def goForward(duty):
    GPIO.output(rightFront1,GPIO.LOW)
    GPIO.output(rightFront2,GPIO.HIGH)

    GPIO.output(leftBack2,GPIO.HIGH)
    GPIO.output(leftBack1,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.LOW)
    GPIO.output(rightBack2,GPIO.HIGH)

    GPIO.output(leftFront1,GPIO.LOW)
    GPIO.output(leftFront22,GPIO.HIGH)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty)

    #sleep(0.05)

def goBackword(duty):
    GPIO.output(rightFront1,GPIO.HIGH)
    GPIO.output(rightFront2,GPIO.LOW)

    GPIO.output(leftBack1,GPIO.HIGH)
    GPIO.output(leftBack2,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.HIGH)
    GPIO.output(rightBack2,GPIO.LOW)

    GPIO.output(leftFront1,GPIO.HIGH)
    GPIO.output(leftFront22,GPIO.LOW)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty)

    #sleep(0.05)

def stop():
    GPIO.output(rightFront1,GPIO.LOW)
    GPIO.output(rightFront2,GPIO.LOW)

    GPIO.output(leftBack1,GPIO.LOW)
    GPIO.output(leftBack2,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.LOW)
    GPIO.output(rightBack2,GPIO.LOW)

    GPIO.output(leftFront1,GPIO.LOW)
    GPIO.output(leftFront22,GPIO.LOW)

    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(0)
    
def turnRight(duty):
    GPIO.output(rightFront1,GPIO.HIGH)
    GPIO.output(rightFront2,GPIO.LOW)

    GPIO.output(leftBack1,GPIO.LOW)
    GPIO.output(leftBack2,GPIO.HIGH)

    GPIO.output(rightBack1,GPIO.HIGH)
    GPIO.output(rightBack2,GPIO.LOW)

    GPIO.output(leftFront1,GPIO.LOW)
    GPIO.output(leftFront22,GPIO.HIGH)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty)  
    
def turnLeft(duty):
    GPIO.output(rightFront1,GPIO.LOW)
    GPIO.output(rightFront2,GPIO.HIGH)

    GPIO.output(leftBack1,GPIO.HIGH)
    GPIO.output(leftBack2,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.LOW)
    GPIO.output(rightBack2,GPIO.HIGH)

    GPIO.output(leftFront1,GPIO.HIGH)
    GPIO.output(leftFront22,GPIO.LOW)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty)    

def frontRight(duty):
    GPIO.output(rightFront1,GPIO.LOW)
    GPIO.output(rightFront2,GPIO.HIGH)

    GPIO.output(leftBack1,GPIO.LOW)
    GPIO.output(leftBack2,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.LOW)
    GPIO.output(rightBack2,GPIO.LOW)

    GPIO.output(leftFront1,GPIO.LOW)
    GPIO.output(leftFront22,GPIO.HIGH)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty) 
    
def frontLeft(duty):
    GPIO.output(rightFront1,GPIO.LOW)
    GPIO.output(rightFront2,GPIO.LOW)

    GPIO.output(leftBack1,GPIO.LOW)
    GPIO.output(leftBack2,GPIO.HIGH)

    GPIO.output(rightBack1,GPIO.LOW)
    GPIO.output(rightBack2,GPIO.HIGH)

    GPIO.output(leftFront1,GPIO.LOW)
    GPIO.output(leftFront22,GPIO.LOW)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty) 
    
def backRight(duty):
    GPIO.output(rightFront1,GPIO.LOW)
    GPIO.output(rightFront2,GPIO.LOW)

    GPIO.output(leftBack1,GPIO.HIGH)
    GPIO.output(leftBack2,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.HIGH)
    GPIO.output(rightBack2,GPIO.LOW)

    GPIO.output(leftFront1,GPIO.LOW)
    GPIO.output(leftFront22,GPIO.LOW)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty) 
    
def backLeft(duty):
    GPIO.output(rightFront1,GPIO.HIGH)
    GPIO.output(rightFront2,GPIO.LOW)

    GPIO.output(leftBack1,GPIO.LOW)
    GPIO.output(leftBack2,GPIO.LOW)

    GPIO.output(rightBack1,GPIO.LOW)
    GPIO.output(rightBack2,GPIO.LOW)

    GPIO.output(leftFront1,GPIO.HIGH)
    GPIO.output(leftFront22,GPIO.LOW)

    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    pwm3.ChangeDutyCycle(duty)
    pwm4.ChangeDutyCycle(duty) 

while True:
    # goForward(40)
    # sleep(2)
    # goLeft(40)
    # sleep(2)
    # goBackword(40)
    # sleep(2)
    # goRight(40)
    # sleep(2)
    x=sys.stdin.read(1)[0]
    print("You pressed", x)
    if x == "w":
        goForward(40)
        sleep(1)
        stop()
    elif x == "s":
        goBackword(40)
        sleep(1)
        stop()
    elif x == "a":
        goLeft(40)
        sleep(1)
        stop()
    elif x == "d":
        goRight(40)
        sleep(1)
        stop()
    elif x == "e":
        turnRight(40)
        sleep(0.5)
        stop()
    elif x == "q":
        turnLeft(40)
        sleep(0.5)
        stop()
    elif x == "x":
        frontRight(40)
        sleep(0.5)
        stop()
    elif x == "c":
        backLeft(40)
        sleep(0.5)
        stop()
    elif x == "z":
        frontLeft(40)
        sleep(0.5)
        stop()
    elif x == "v":
        backRight(40)
        sleep(0.5)
        stop()
    elif x == "r":
        break
        
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)