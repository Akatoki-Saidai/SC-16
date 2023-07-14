from machine import Pin,I2C
import utime

class BMP280:
    def __init__(self,i2c_number=0,scl=Pin(1),sda=Pin(0),baudrate=115200):
        self.i2c = I2C(i2c_number,scl=scl,sda=sda,freq=baudrate)
        self.bmp280_addr = 0x76
        self.id_register = 0xd0
        self.temp_register = 0xfa
        self.press_register = 0xf7
        ctrl_register = 0xf4
        osrs_temp = b'00100000'
        osrs_press = b'00000100'
        mode = b'00000011'
        
        self.i2c.writeto_mem(self.bmp280_addr,ctrl_register,osrs_temp)
        self.i2c.writeto_mem(self.bmp280_addr,ctrl_register,osrs_press)
        self.i2c.writeto_mem(self.bmp280_addr,ctrl_register,mode)
        
    def measure(self):
        data = self.i2c.readfrom_mem(self.bmp280_addr,self.temp_register,3)
        return data[0],data[1],data[2]

if __name__ == '__main__':
    test = BMP280()
    test_measure = test.measure()
    print(test_measure)