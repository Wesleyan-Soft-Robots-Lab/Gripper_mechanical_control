from xarm import version
from xarm.wrapper import XArmAPI
import serial
import time

ip = '192.168.1.232'

arm = XArmAPI(ip)

arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

speed = 100
# arm.move_gohome(wait=True)

arm.set_servo_angle(angle=[-45, 0,-10, 0,0,0], speed=speed/2)

ser = serial.Serial('COM4', 9600)
time.sleep(2)

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            value = int(line)
            print(value)
            if value >= 10000:
                pass
            elif value >= 800:
                arm.set_servo_angle(angle=[30, 0,-10,0,0,0], speed=speed)
            else:
                arm.set_servo_angle(angle=[-45, 0,-10, 0,0,0], speed=speed/2)
        except ValueError:
            print('Invalid input received')

arm.disconnect()