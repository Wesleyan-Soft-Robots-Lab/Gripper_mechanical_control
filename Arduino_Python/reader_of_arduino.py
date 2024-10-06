import serial
import time

ser = serial.Serial('COM4', 9600)
time.sleep(2)

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            value = int(line)
            print(value)
        except ValueError:
            print("Invalid data received")