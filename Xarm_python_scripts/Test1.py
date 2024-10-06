#!/usr/bin/env python3

import os
import sys
import time
import math
import serial

from xarm.wrapper import XArmAPI


ip = '192.168.1.232'

arm = XArmAPI(ip)

arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

speed = 100
arm.move_gohome(speed=speed, wait=True)

arm.set_servo_angle(angle=[0,0,-90,0,0,0], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

#arm.move_gohome(wait=True)

ser = serial.Serial('COM4', 9600)
time.sleep(2)

while True:
    line = ser.readline().decode('utf-8').strip()


arm.disconnect()

