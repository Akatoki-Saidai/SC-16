from LongRange  import LongRange
from ShortRange import ShortRange
from machine import Pin
import utime
class Cansat():
    def __init__(self):
        self.long_range = LongRange()
        self.short_range = ShortRange()
    def run(self):
        #self.long_range.falling()     
        self.long_range.move_phase()
        utime.sleep(2)
        self.short_range.move_phase()
        print("finish")
if __name__ == "__main__":
    led = Pin(25,Pin.OUT)
    led.value(1)
    cansat = Cansat()
    cansat.run()
    