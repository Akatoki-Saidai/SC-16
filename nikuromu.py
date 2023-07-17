from machine import Pin
import utime
a = Pin(0,Pin.OUT)
while True:
    a.value(1)