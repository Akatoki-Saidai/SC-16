import utime
from machine import UART, Pin

class UARTtoPi():
    def __init__(self,uart_number=1, baudrate=115200, tx=Pin(8), rx=Pin(9)):
        self.uart1 = UART(uart_number, baudrate=baudrate, tx=tx, rx=rx)

    def connect(self):
        rxData = bytes()
        while self.uart1.any() > 0:
            rxData += self.uart1.read(1)
        if len(rxData) > 0:
            recv_data = rxData.decode('ascii')
            #print(recv_data)
            return recv_data
        utime.sleep(1)
if __name__ == '__main__':
    test = UARTtoPi()
    while True:
        recv_data = test.connect()
        print(recv_data)