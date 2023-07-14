import utime
from machine import UART, Pin

class UARTtoPi():
    def __init__(self,uart_number=1, baudrate=115200, tx=Pin(4), rx=Pin(5)):
        self.uart1 = UART(uart_number, baudrate=baudrate, tx=tx, rx=rx)

    def connect(self):
        rxData = bytes()
        while self.uart1.any() > 0:
            rxData += self.uart1.read(1)
        if len(rxData) > 0:
            print(rxData.decode('ascii'))
        utime.sleep(1)