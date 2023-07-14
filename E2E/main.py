from LongRange.LongRange  import LongRange
from ShortRange.ShortRange import ShortRange
class Cansat():
    def __init__(self):
        self.long_range = LongRange()
        self.short_range = ShortRange()
    def run(self):
        if(self.long_range.falling() > 0):
            self.long_range.move_phase()
            self.short_range.move_phase()
            print("finish")