from UltraSound import UltraSound
from Motor import Motor
from UARTtoPi import UARTtoPi
from sd import SDCard
class ShortRange():
    def __init__(self):
        self.ultrasound = UltraSound()
        #self.uarttopi = UARTtoPi()
        self.motor = Motor()
        #self.card = SDCard()
    def move_phase(self):
        print("近距離フェーズ")
        print("切り替わりました")
        """
        while (self.ultrasound.read_distance() > 2):
            self.card.write("-------------")
            self.card.write("distance")
            if(270 <= self.uarttopi < 370):
                print("forward")
                self.motor.forward()
            elif(self.uarttopi < 270):
                print("left")
                self.motor.left()
            elif(self.uarttopi >= 370):
                print("right")
                self.motor.right()
            """
