from time import sleep
import VL53L0X
import statistics
dev = 0.1 #constant deviation

tof2 = VL53L0X.VL53L0X(tca9548a_num=0, tca9548a_addr=0x70) # tof initialize


tof2.open()
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)  #start ranging

timing2 = tof2.get_timing()

if timing2 < 20000:   #set timing budget
    timing2 = 20000

#get the distance readings
def tof2Readings():
    global tof2
    distance2 = tof2.get_distance()
    if distance2 > 0:
        distance2 = distance2
    else:
        distance2 = 0
  
    return distance2  

#identify the cylinder or box
def cylinder():
    distance = []
    tot = 0
    for i in range(20):         #insert distance readings to the distance array
        dist = tof2Readings()
        distance.append(dist)
        #tot += dist
        sleep(0.5)

    #avg_dist = tot/20
    deviation = statistics.stdev(distance)    #get the deviation of the array
    if(deviation<=dev):
        return "cylinder"
    else:
        return "box"

tof2.stop_ranging()
tof2.close()

