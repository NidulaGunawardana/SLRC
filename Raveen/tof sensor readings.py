import time
import VL53L0X

# Create a VL53L0X object for device on TCA9548A bus 1
tof1 = VL53L0X.VL53L0X(tca9548a_num=0, tca9548a_addr=0x70)
# Create a VL53L0X object for device on TCA9548A bus 2
tof2 = VL53L0X.VL53L0X(tca9548a_num=1, tca9548a_addr=0x70)
tof1.open()
tof2.open()

# Start ranging on TCA9548A bus 1
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
# Start ranging on TCA9548A bus 2
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof1.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))

while True:
    # Get distance from VL53L0X  on TCA9548A bus 1
    tof1.start_ranging(1)
    tof2.start_ranging(1)
    distance1 = tof1.get_distance()
    distance2 = tof2.get_distance()
    if distance1 > 0:
        print("1: %d mm, %d mm "% (distance1, (distance2)))

    # Get distance from VL53L0X  on TCA9548A bus 2

    # if distance2 > 0:
    #     print("2: %d mm, %d cm"% (distance2, (distance2/10)))

    time.sleep(timing/10000000.00)

tof1.stop_ranging()
tof2.stop_ranging()

tof1.close()
tof2.close()
