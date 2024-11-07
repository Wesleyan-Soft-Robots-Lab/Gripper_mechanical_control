from xarm import version
from xarm.wrapper import XArmAPI
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import os

output_dir = r"C:\Users\softrobotslab\Gripper_mechanical_control\Data"

output_path = os.path.join(output_dir, "demonstration_2.gif")

ip = '192.168.1.232'

arm = XArmAPI(ip)

arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

speed = 100
arm.set_servo_angle(angle=[-45, 0,-10, 0,0,0], speed=speed/2)

ser = serial.Serial('COM4', 9600)
time.sleep(2)

readings = np.array([])
times = np.array([])
start_time = time.time()

touched = 2500

while time.time()-start_time-17<10:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            curr_time = time.time()-start_time-17
            times = np.append(times, curr_time)
            value = int(line)
            if value >= touched:
                readings = np.append(readings, 1.0)
            else:
                readings = np.append(readings, 0.0)
            # readings = np.append(readings, value)
            print(value, curr_time)
            
            if value >= 10000:
                pass
            elif value >= touched:
                arm.set_servo_angle(angle=[30, 0, -10, 0,0,0], speed=speed)
                # times = np.append(times, curr_time)
                # readings = np.append(readings, 1)
            # elif value >= 1500:
            #     arm.set_servo_angle(angle=[15, 0,-10,0,0,0], speed=speed/2)
            else:
                arm.set_servo_angle(angle=[-45, 0,-10, 0,0,0], speed=speed/2)
                # np.append(times, curr_time)
                # readings = np.append(readings, 0)
        except ValueError:
            print('Invalid input received')

arm.disconnect()
# print(times.shape, readings.shape)
mask = times >= 0
times = times[mask]
readings = readings[mask]
# print(times.shape, readings.shape)
fig, ax = plt.subplots()
ax.plot(times, readings, label="0.0 = Untouched; 1.0 = Touched")
point, = ax.plot([],[],'ro')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Touch')
ax.set_xlim(np.min(times), np.max(times)) 
ax.set_ylim(np.min(readings)-1, np.max(readings) + 1)
# ax.legend()

def init():
    point.set_data([],[])
    return point,

def animate(i):
    # print(times[i], readings[i])
    if i < len(times) and i < len(readings):
        x_val = float(times[i])
        y_val = float(readings[i])
        # print(f"Animating point at ({x_val}, {y_val})")
        point.set_data([x_val], [y_val])
    return point,

ani = FuncAnimation(fig, animate, frames = len(times), init_func=init, blit=True)

ani.save(output_path, writer="pillow", fps=30)
