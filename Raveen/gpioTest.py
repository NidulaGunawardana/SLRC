from gpiozero import LED
from time import sleep 

red_LED= LED(18)

while True:
    red_LED.on()
    sleep(0.5) 
    red_LED.off()
    sleep(1)
