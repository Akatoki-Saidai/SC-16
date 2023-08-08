#
# Example. Using I2C at P9, P10
#
from machine import Pin
import bme280_float as bme280

i2c = machine.I2C(1,sda=machine.Pin(10), scl=machine.Pin(11))
bme = bme280.BME280(i2c=i2c)
while True:
    print(bme.values)