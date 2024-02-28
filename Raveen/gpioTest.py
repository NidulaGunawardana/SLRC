from gpiozero import LED
from time import sleep 

red = LED(18)

while True:
    red.on()
    sleep(0.5) 
    red.off()
    sleep(1)