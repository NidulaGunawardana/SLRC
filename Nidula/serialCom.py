#!/quanta/bin/env python3
import serial
import time


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

def greenLed():
    ser.write(b"Green\n")
    line = ser.readline().decode('utf-8').rstrip()
    # print(line)
    time.sleep(1)
    # time.sleep(1)
    
def blueLed():
    ser.write(b"Blue\n")
    line = ser.readline().decode('utf-8').rstrip()
    # print(line)
    time.sleep(1)
    # time.sleep(1)

while True:
    greenLed()
    blueLed()
    # time.sleep(1)
    # time.sleep(1)


    
