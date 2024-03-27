#!/quanta/bin/env python3
import serial
import time


ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
ser.reset_input_buffer()


def cylinderLed():
    ser.write(b"Cylinder\n")
    line = ser.readline().decode("utf-8").rstrip()


def boxLed():
    ser.write(b"Box\n")
    line = ser.readline().decode("utf-8").rstrip()


def highLed():
    ser.write(b"High\n")
    line = ser.readline().decode("utf-8").rstrip()


def midLed():
    ser.write(b"Mid\n")
    line = ser.readline().decode("utf-8").rstrip()


def lowLed():
    ser.write(b"Low\n")
    line = ser.readline().decode("utf-8").rstrip()
    

def offLed():
    ser.write(b"Off\n")
    line = ser.readline().decode("utf-8").rstrip()


while True:
    cylinderLed()
    boxLed()
    midLed()
    highLed()
    lowLed()
    offLed()