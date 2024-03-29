import time
import VL53L0X
from cuboidToF import *

# Create a VL53L0X object for device on TCA9548A bus 1
tof1 = VL53L0X.VL53L0X(tca9548a_num=1, tca9548a_addr=0x70)
tof1.open()
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BEST)

tof3 = VL53L0X.VL53L0X(tca9548a_num=0, tca9548a_addr=0x70)
tof3.open()
tof3.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BEST)

tof4 = VL53L0X.VL53L0X(tca9548a_num=7, tca9548a_addr=0x70)
tof4.open()
tof4.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)

# Start ranging on TCA9548A bus 1



timing1 = tof1.get_timing()
timing2 = tof3.get_timing()
timing3 = tof4.get_timing()

if timing1 < 20000:
    timing1 = 20000
    
if timing2 < 20000:
    timing2 = 20000

if timing3 < 20000:
    timing3 = 20000
    
def tof1Readings():
    global tof1
    # Get distance from VL53L0X  on TCA9548A bus 1
    distance1 = tof1.get_distance()
    if distance1 > 0:
        distance1 = distance1
    else:
        distance1 = 0
  
    return distance1-16

def tof3Readings():
    # global tof3
        # Get distance from VL53L0X on TCA9548A bus 0
    distance2 = tof3.get_distance()
    if distance2 > 0:
        distance2 = distance2
    else:
        distance2 = 0
      
    return distance2-15


def tof4Readings():
    # global tof3
        # Get distance from VL53L0X on TCA9548A bus 0
    distance3 = tof4.get_distance()
    if distance3> 0:
        distance3 = distance3-10
    else:
        distance3 = 0
      
    return distance3

# x = 0
# # tof = 0
while(True):
    read1 = tof1Readings()
    read2 = tof3Readings()
    read3 = tof4Readings()
    read4 = tof2Readings()
    print(read1,read2,read3,read4)
    time.sleep(timing2/10000000.00)
    # x+=1
    
# tof.stop_ranging()
# tof.close()
