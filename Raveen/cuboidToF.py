from time import sleep
import VL53L0X

tof2 = VL53L0X.VL53L0X(tca9548a_num=2, tca9548a_addr=0x70)


tof2.open()
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing2 = tof2.get_timing()

if timing2 < 20000:
    timing2 = 20000

def tof2Readings():
    global tof2
    distance2 = tof2.get_distance()
    if distance2 > 0:
        distance2 = distance2
    else:
        distance2 = 0
  
    return distance2

def Cylinder():
    distance = []
    tot = 0
    for i in range(20):
        dist = tof2Readings()
        distance.append(dist)
        tot += dist
        sleep(0.1)

    avg_dist = tot/20
    if(avg_dist>260 & avg_dist<270):
        print("Cylinder")
    else:
        print("Box")

tof2.stop_ranging()
tof2.close()   