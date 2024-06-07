import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins
pins = [8, 25, 22]

# Set the pins as input
GPIO.setup(pins, GPIO.IN)

# Function to read the state of a pin
def sensor_LEFT():
    """
    Returns the state of the left sensor.

    Returns:
        int: The state of the left sensor(white - 0 Black -1) .
    """
    state = GPIO.input(8)
    return state

def sensor_RIGHT():
    """
    Returns the state of the right sensor.

    Returns:
        int: The state of the right sensor (white - 0 Black -1).
    """
    state = GPIO.input(25)
    return state

def sensor_FRONT():
    """
    Returns the state of the front sensor.

    Returns:
        int: The state of the front sensor (white - 0 Black -1).
    """
    state = GPIO.input(22)
    return state
# 