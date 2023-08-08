#https://www.hiramine.com/physicalcomputing/arduino/sdreadwrite.html
#上はArudinoでやっているから、これをPicoに置き換える
from machine import Pin, SPI
import utime
import os, sdcard
class SDCard:
    def __init__(self,spi_number=0,baudrate=115200,sck=Pin(2),mosi=Pin(3),miso=Pin(4),CSn = Pin(5)):
        spi = SPI(spi_number,baudrate=baudrate,sck=sck,mosi=mosi,miso=miso)
        sd = sdcard.SDCard(spi, CSn)
        os.mount(sd, '/sd')
        os.chdir('sd')

    def write(self,message):
        with open('log.txt', 'a') as f:
            print("-------------------------------------------------",file=f)
            for i in range(len(message)):
                print(f"{message[i]}", file=f)
                utime.sleep(0.1)
            
if __name__ == '__main__':
    message = ["a","b","c","d"]
    card = SDCard()
    card.write(message)