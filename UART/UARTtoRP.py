"""
import serial
ser = serial.Serial('/dev/serial0', 115200)
ser.write(b'Hello Pico! Im Zero.')
ser.close()
"""
import chardet
str = 'Hello Pico'
print(chardet.detect(str.encode('ascii')))
print(str)
print(str.decode())