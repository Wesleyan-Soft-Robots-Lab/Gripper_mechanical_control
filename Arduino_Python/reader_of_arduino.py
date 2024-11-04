import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


ser = serial.Serial('COM4', 9600)
time.sleep(2)

readings = np.array([])
times = np.array([])
start_time = time.time()
# times = np.append(times, start_time-start_time)
# print)
while time.time()-start_time<40:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            curr_time = time.time()-start_time
            times = np.append(times, curr_time)
            value = int(line)
            readings = np.append(readings, value)
            print(value, curr_time)
        except ValueError:
            print("Invalid data received")
# print(times, readings)
fig, ax = plt.subplots()
point, = ax.plot([],[],'ro')
ax.plot(times, readings)
ax.set_xlabel('Time')
ax.set_ylabel('Capacitance')
ax.set_xlim(15,40) 
ax.set_ylim(-2000,6000)
ax.legend()

def init():
    point.set_data([],[])
    return point,

def animate(i):
    point.set_data(times[i], readings[i])
    return point,

ani = FuncAnimation(fig, animate, frames = len(times)-15, init_func=init, blit=True)

plt.show()