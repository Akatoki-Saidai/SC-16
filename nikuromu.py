from machine import Pin
import utime
import time
a = Pin(8,Pin.OUT)
b = Pin(25,Pin.OUT)
a.value(0)
b.value(0)
while True:
    a.value(1)
    b.value(1)