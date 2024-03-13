import VL53L0X
import time

tof = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
print("Python: Initialized")
tof.open()
print("Python: Opened")


time_start = time.time()

while True:
    time_end = time.time()
    time_elapsed = time_end - time_start

    print("")
    print("--- Time : {:.1f}s ---".format(time_elapsed))

    # tof.start_ranging(1)    # 1 = Short Range
    # distance_mm = tof.get_distance()
    # print("Short Range Distance: {}mm".format(distance_mm))
    # tof.stop_ranging()

    ### --- Medium Range --- ###
    tof.start_ranging(2)    # 2 = Medium Range
    distance_mm = tof.get_distance()
    print("Medium Range Distance: {}mm".format(distance_mm))
    tof.stop_ranging()

    # ### --- Long Range --- ###
    # tof.start_ranging(3)    # 3 = Long Range
    # distance_mm = tof.get_distance()
    # print("Long Range Distance: {}mm".format(distance_mm))
    # tof.stop_ranging()


    time.sleep(1)
