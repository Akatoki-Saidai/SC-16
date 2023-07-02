from machine import Pin
import utime
print("Hello")
trigger = Pin(14, Pin.OUT)#Trig – トリガー 超音波出力用の信号を送信
echo = Pin(15, Pin.IN)#Echo – エコー 超音波入力用の信号を受信
print("1")
def read_distance():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep(0.00001)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2

    print("dinstance: ",distance,"cm")
while True:
   read_distance()
   utime.sleep(0.1)