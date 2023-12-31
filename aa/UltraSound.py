from machine import Pin
import utime

class UltraSound():
    def __init__(self,trigger=Pin(17,Pin.OUT),echo=Pin(16,Pin.IN)):
        self.trigger = trigger#Trig – トリガー 超音波出力用の信号を送信
        self.echo = echo#Echo – エコー 超音波入力用の信号を受信
        self.signalon = 0
        self.signaloff = 0
    def read_distance(self):
        self.trigger.low()
        utime.sleep_us(2)
        self.trigger.high()
        utime.sleep(0.00001)
        self.trigger.low()
        while self.echo.value() == 0:
            self.signaloff = utime.ticks_us()
        while self.echo.value() == 1:
            self.signalon = utime.ticks_us()
        timepassed = self.signalon - self.signaloff
        distance = (timepassed * 0.0343) / 2
        return distance

if __name__ == '__main__':
    sound = UltraSound()
    while True:
        distance_data = sound.read_distance()
        utime.sleep(0.1)
        print("dinstance: ",distance_data,"cm")
