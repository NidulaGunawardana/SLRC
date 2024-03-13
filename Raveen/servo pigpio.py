import pigpio
from time import sleep

# connect to the 
pi = pigpio.pi()

# loop forever
while True:

    pi.set_servo_pulsewidth(19, 0)    # off
    sleep(1)
    pi.set_servo_pulsewidth(19, 1000) # position anti-clockwise
    sleep(1)
    pi.set_servo_pulsewidth(19, 1500) # middle
    sleep(1)
    pi.set_servo_pulsewidth(19, 2000) # position clockwise
    sleep(1)