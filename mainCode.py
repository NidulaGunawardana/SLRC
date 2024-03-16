from Raveen.motorRotating import *
import tty, sys, termios

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
x = 0


duty = 30


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
    if x == "8":
        goForward(duty)
        sleep(1)
        stop()
    elif x == "2":
        goBackward(duty)
        sleep(1)
        stop()
    elif x == "4":
        goLeft(duty)
        sleep(1)
        stop()
    elif x == "6":
        goRight(duty)
        sleep(1)
        stop()
    elif x == "+":
        turnRight(duty)
        sleep(0.5)
        stop()
    elif x == "-":
        turnLeft(duty)
        sleep(0.5)
        stop()
    elif x == "9":
        frontRight(duty)
        sleep(0.5)
        stop()
    elif x == "1":
        backLeft(duty)
        sleep(0.5)
        stop()
    elif x == "7":
        frontLeft(duty)
        sleep(0.5)
        stop()
    elif x == "3":
        backRight(duty)
        sleep(0.5)
        stop()
    elif x == "r":
        break
        
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)