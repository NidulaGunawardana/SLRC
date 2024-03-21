import time
import VL53L0X

# Create a VL53L0X object for device on TCA9548A bus 1
tof1 = VL53L0X.VL53L0X(tca9548a_num=1, tca9548a_addr=0x70)


tof1.open()



# Start ranging on TCA9548A bus 1
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)


timing1 = tof1.get_timing()


if timing1 < 20000:
    timing1 = 20000



def tof1Readings():
    global tof1
    # Get distance from VL53L0X  on TCA9548A bus 1
    distance1 = tof1.get_distance()
    if distance1 > 0:
        distance1 = distance1
    else:
        distance1 = 0

    
    return distance1,tof1


# x = 0
# tof = 0
# while(x<100):
#     read1,tof = tof1Readings(tof1)
#     print(read1)
#     # time.sleep(timing1/10000000.00)
#     x+=1
    
# tof.stop_ranging()
# tof.close()
