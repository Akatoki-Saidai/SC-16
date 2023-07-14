import time
from machine import Pin,PWM

class Motor:
    def __init__(self,motor1_pin=[26,27],motor2_pin=[6,7],duty = 65535):
        self.motor1_IN1 = PWM(Pin(motor1_pin[0]))
        self.motor1_IN2 = PWM(Pin(motor1_pin[1]))
        self.motor2_IN1 = PWM(Pin(motor2_pin[0]))
        self.motor2_IN2 = PWM(Pin(motor2_pin[1]))
        self.motor1_IN1.freq(1000000)
        self.motor1_IN2.freq(1000000)
        self.motor2_IN1.freq(1000000)
        self.motor2_IN2.freq(1000000)
        self.duty = duty

    def forward(self):
        print("forward")
        self.motor1_IN1.duty_u16(int(self.duty))
        self.motor1_IN2.duty_u16(0)
        self.motor2_IN1.duty_u16(int(self.duty))
        self.motor2_IN2.duty_u16(0)
        time.sleep(5)
        self.motor1_IN1.duty_u16(0)
        self.motor1_IN2.duty_u16(0)
        self.motor2_IN1.duty_u16(0)
        self.motor2_IN2.duty_u16(0)

    def back(self):
        print("back")
        self.motor1_IN1.duty_u16(0)
        self.motor1_IN2.duty_u16(int(self.duty))
        self.motor2_IN1.duty_u16(0)
        self.motor2_IN2.duty_u16(int(self.duty))
        time.sleep(5)
        self.motor1_IN1.duty_u16(0)
        self.motor1_IN2.duty_u16(0)
        self.motor2_IN1.duty_u16(0)
        self.motor2_IN2.duty_u16(0)

    def right(self):
        print("right")
        self.motor1_IN1.duty_u16(int(self.duty))
        self.motor1_IN2.duty_u16(0)
        self.motor2_IN1.duty_u16(0)
        self.motor2_IN2.duty_u16(0)
        time.sleep(5)
        self.motor1_IN1.duty_u16(0)
        self.motor1_IN2.duty_u16(0)
        self.motor2_IN1.duty_u16(0)
        self.motor2_IN2.duty_u16(0)
    
    def left(self):
        print("left")
        self.motor1_IN1.duty_u16(0)
        self.motor1_IN2.duty_u16(0)
        self.motor2_IN1.duty_u16(int(self.duty))
        self.motor2_IN2.duty_u16(0)
        time.sleep(5)
        self.motor1_IN1.duty_u16(0)
        self.motor1_IN2.duty_u16(0)
        self.motor2_IN1.duty_u16(0)
        self.motor2_IN2.duty_u16(0)
    
if __name__ == '__main__':
    test = Motor()
    test.forward()
    test.back()
    test.right()
    test.left()
