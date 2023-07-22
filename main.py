from GPS import GPS
#from PressTemp import BMP280
from Motor import Motor
from bno055 import *
#from sd import SDCard
from machine import Pin,I2C,UART,SPI,SoftI2C
import utime
import math
import time

gps = GPS()
#press_temp = BMP280()
#press_temp_measure = press_temp.measure()
motor = Motor()
i2c = SoftI2C(sda=Pin(14), scl=Pin(15),timeout=1_000)
imu = BNO055(i2c)
#card = SDCard()
def falling():
    calibrated = False
    data = [0,0,0,0,0]
    count = 0
    t1 = time.time()
    while True:
        t2 = time.time()
        try:
            if not calibrated:
                calibrated = imu.calibrated()
                print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
            #print('Temperature {}°C'.format(imu.temperature()))
            print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
            print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
            #print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
            print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
            #print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
            #print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
            count += 1
            accel_z = imu.lin_acc()[2]
            data.append(abs(accel_z))
            data.pop(0)
            print(data)
            if(t2-t1 > 30):
                print("一定時間経過しました")
                break
            if(abs(accel_z) >  40 ):
                print("落下中")
            if(abs(data[0]) > 40 and data[4] < 10):
                print("着地しました")
                break
            else:
                pass
        except MemoryError:
            pass
def calculate_north_degree():

    mx,my,mz = imu.mag()        # 三次元磁力密度
    # Calculate magnetic strength and direction.
    magnitude = math.sqrt(mx * mx + my * my + mz * mz)
    if my > 0:
        direction = math.atan2(mx, my) * 180 / math.pi
    elif my < 0:
        direction = (math.atan2(mx, my) + 2 * math.pi) * 180 / math.pi
    else:
        if mx < 0:
            direction = 270.0
        else:
            direction = 90.0
    # Convert direction to heading.
    heading = 360 - direction +90
    if heading >= 360:
        heading -= 360
    if heading < 0:
        heading += 360
    
    #print("north_degree",heading)
    return heading
    
def degree_from_front_to_goal():
#print("nowlat,now_lon",now_lat,now_lon)
    goal_lat = 35.86107
    goal_long = 139.60703
    now_lat,now_lon = gps.GPSwatch()
    north_degree = calculate_north_degree()#330
    GPS_degree = gps.cal_azimuth(goal_lat,goal_long,now_lat,now_lon)

    degree = GPS_degree - north_degree
    return degree
def move_phase():
    print("長距離フェーズに入ります")
    goal_lat = 35.86107
    goal_long = 139.60703
    #card.write("--------------")
    #card.write(f"lat:{data1},long{data2}")
    #card.write(f"distance:{distance}")
    #card.write(f"heading:{heading}")
    while True:
        try:
            gps = GPS()
            data1,data2 = gps.GPSwatch()
            #print(f'lat:{data1},long:{data2}')
            print(data1,data2)
            #print(gps.cal_azimuth(goal_lat,goal_long,data1,data2))
            #calculate_north_degree()
            degree = abs(degree_from_front_to_goal())
            print("degree:" ,degree)
            distance = gps.cal_distance(goal_lat,goal_long,data1,data2)
            print(f"distance:{distance}m")
        except TypeError:
            continue
        if(distance > 10):#kmをmに直さないといけない
            if(degree <= 30):
                motor.forward()
            elif(50>degree > 30):
                motor.left()
            elif(225 > degree > 200 ):
                motor.right()
            elif(150 < degree < 200):
                motor.forward()
            elif(50 < degree < 150):
                motor.right()
            elif(225 < degree < 360):
                motor.left()
            #elif(degree <)
                
            else:
                motor.back()
            print("接近中")
        else:
            print("近距離フェーズに入ります")
            break
a = Pin(25,Pin.OUT)
a.value(1)
move_phase()
