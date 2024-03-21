import time
import VL53L0X

# Create a VL53L0X object for device on TCA9548A bus 1
tof1 = VL53L0X.VL53L0X(tca9548a_num=1, tca9548a_addr=0x70)
# tof2 = VL53L0X.VL53L0X(tca9548a_num=1, tca9548a_addr=0x70)
# tof3 = VL53L0X.VL53L0X(tca9548a_num=7, tca9548a_addr=0x70)
# tof4 = VL53L0X.VL53L0X(tca9548a_num=6, tca9548a_addr=0x70)

tof1.open()
# tof2.open()
# tof3.open()
# tof4.open()


# Start ranging on TCA9548A bus 1
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
# tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
# tof3.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
# tof4.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing1 = tof1.get_timing()
# timing2 = tof2.get_timing()
# timing3= tof3.get_timing()
# timing4= tof4.get_timing()

if timing1 < 20000:
    timing1 = 20000

# if timing2 < 20000:
#     timing2 = 20000

# if timing3 < 20000:
#     timing3 = 20000

# if timing4 < 20000:
#     timing4 = 20000


def tof1Readings():
    
    # Get distance from VL53L0X  on TCA9548A bus 1
    tof1.start_ranging(1)
    distance1 = tof1.get_distance()
    if distance1 > 0:
        # print("1: %d mm% (distance1))
        pass

    # Get distance from VL53L0X  on TCA9548A bus 2

    # if distance2 > 0:
    #     print("2: %d mm, %d cm"% (distance2, (distance2/10)))

    
    return distance1

# def tof2Readings():
#     # Get distance from VL53L0X  on TCA9548A bus 1
#     tof2.start_ranging(1)
#     distance2 = tof2.get_distance()
#     if distance2 > 0:
#         print("1: %d mm, %d mm "% (distance2))

#     # Get distance from VL53L0X  on TCA9548A bus 2

#     # if distance2 > 0:
#     #     print("2: %d mm, %d cm"% (distance2, (distance2/10)))

#     time.sleep(timing2/10000000.00)

# def tof3Readings():
#     # Get distance from VL53L0X  on TCA9548A bus 1
#     tof3.start_ranging(1)
#     distance3 = tof3.get_distance()
#     if distance3 > 0:
#         print("1: %d mm, %d mm "% (distance3))

#     # Get distance from VL53L0X  on TCA9548A bus 2

#     # if distance2 > 0:
#     #     print("2: %d mm, %d cm"% (distance2, (distance2/10)))

#     time.sleep(timing3/10000000.00)

# def tof2Readings():
#     # Get distance from VL53L0X  on TCA9548A bus 1
#     tof4.start_ranging(1)
#     distance4 = tof4.get_distance()
#     if distance4 > 0:
#         print("1: %d mm, %d mm "% (distance4))

#     # Get distance from VL53L0X  on TCA9548A bus 2

#     # if distance2 > 0:
#     #     print("2: %d mm, %d cm"% (distance2, (distance2/10)))

#     time.sleep(timing4/10000000.00)

# # tof1.stop_ranging()
# # tof2.stop_ranging()
# # tof3.stop_ranging()
# # tof4.stop_ranging()

# # tof1.close()
# # tof2.close()
# # tof3.close()
# # tof4.close()

while(True):
    read1 = tof1Readings()
    print(read1)
    time.sleep(timing1/10000000.00)
