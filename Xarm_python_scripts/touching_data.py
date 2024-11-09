from xarm import version
from xarm.wrapper import XArmAPI
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import os

output_dir = r"C:\Users\softrobotslab\Gripper_mechanical_control\Data\Python"
files = os.listdir(output_dir)

# output_path = os.path.join(output_dir, "demonstration_3.gif")

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
capacitance = np.array([])
times = np.array([])
start_time = time.time()

touched = 2500
# line = ser.readline().decode('utf-8').strip()
# init_val = int(line)
while time.time()-start_time-17<10:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            curr_time = time.time()-start_time-17
            times = np.append(times, curr_time)
            value = int(line)-1839.7731958762886
            capacitance = np.append(capacitance, value)
            if value >= touched:
                readings = np.append(readings, touched)
            else:
                readings = np.append(readings, 0.0)
            # readings = np.append(readings, value)
            print(curr_time, value)
            
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
capacitance = capacitance[mask]
print(np.average(capacitance))
# print(times.shape, readings.shape)
# fig, ax = plt.subplots(2,1, sharex=True)
# ax[0].plot(times, readings)
# point, = ax[0].plot([],[],'ro')
# ax[0].set_xlabel('Time (s)')
# ax[0].set_ylabel('Touch')
# ax[1].plot(times, capacitance)
# ax[1].set_ylabel('Capacitance')

# ax[0].set_xlim(np.min(times), np.max(times)) 
# ax[0].set_ylim(np.min(readings)-1, np.max(readings) + 1)
# # ax.legend()

fig, ax = plt.subplots()
ax.plot(times, readings, color='blue')
point1, = ax.plot([],[], 'ro')
ax.plot(times, capacitance, color='green')
ax.set_xlabel('Time(s)')
ax.set_ylabel('Capacitance(O)/Touch')
ax.set_xlim(np.min(times), np.max(times))
point2, = ax.plot([],[], 'bo')
# ax[0].set_ylim(np.min(readings)-1, np.max(readings) + 1) 

plt.tight_layout()

def init():
    point1.set_data([],[])
    point2.set_data([],[])
    return point1,point2

def animate(i):
    # print(times[i], readings[i])
    if i < len(times) and i < len(readings):
        x_val = float(times[i])
        y1_val = float(readings[i])
        y2_val = float(capacitance[i])
        # print(f"Animating point at ({x_val}, {y_val})")
        point1.set_data([x_val], [y1_val])
        point2.set_data([x_val], [y2_val])
    return point1, point2

ani = FuncAnimation(fig, animate, frames = len(times), init_func=init, blit=True)

i = len(files)
output_path = os.path.join(output_dir, f"demonstration_{i}.gif")
ani.save(output_path, writer="pillow", fps=30)
