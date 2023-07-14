from GPS import GPS
from PressTemp import BMP280
from Motor import Motor
from bno055 import *
from SDCard.sd import SDCard
from machine import Pin,I2C,UART,SPI,SoftI2C
import utime
class LongRange():

    def __init__(self):
        self.goal = [1,2]#ゴールの緯度経度入れる
        self.gps = GPS()
        press_temp = BMP280()
        self.press_temp_measure = press_temp.measure()
        self.motor = Motor()
        self.i2c = machine.I2C(0, sda=Pin(2), scl=Pin(3))
        self.imu = BNO055(i2c)
        self.card = SDCard()
    def falling(self):
        return self.imu.lin_acc()
    def move_phase(self):
        goal_lat = 35.862734
        goal_long = 139.607167
        self.card.write("--------------")
        data1,data2 =  self.gps.GPSwatch()
        self.card.write(f"lat:{data1},long{data2}")
        distance = self.gps.cal_distance(goal_lat,goal_long,data1,data2)
        self.card.write(f"distance:{distance}")
        heading = self.gps.cal_azimuth()
        self.card.write(f"heading:{heading}")
        while True:
            if(distance > 10):#kmをmに直さないといけない
                if(-45 <= heading <= 45):
                    self.motor.forward()
                elif(heading > 45):
                    self.motor.right()
                elif(heading < -45):
                    self.motor.left()
                else:
                    self.motor.back()
            else:
                break
if __name__ == '__main__':
    cansat = LongRange()
    cansat.move_phase()