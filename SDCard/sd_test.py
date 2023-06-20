#https://www.hiramine.com/physicalcomputing/arduino/sdreadwrite.html
#上はArudinoでやっているから、これをPicoに置き換える
from machine import Pin, SPI
import utime
import os, sdcard

spi = SPI(0,baudrate=115200)
print(spi)
print(Pin(2))
print(Pin(3))
print(Pin(4))
print(Pin(5))
sd = sdcard.SDCard(spi, Pin(5))

os.mount(sd, '/sd')
os.chdir('sd')
time = 0

while True:

    print("Hello")
    with open('log.txt', 'a') as f:
        print("Time: ", file=f)
        print("Temp: ", file=f)
        print(" ", file=f)
      
    utime.sleep(0.1)