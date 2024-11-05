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
while time.time()-start_time-15<10:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            curr_time = time.time()-start_time-15
            times = np.append(times, curr_time)
            value = int(line)
            readings = np.append(readings, value)
            print(value, curr_time)
        except ValueError:
            print("Invalid data received")
# print(len(times), len(readings))
# times = np.ravel(times)
# readings = np.ravel(readings)
mask = times >= 0
times = times[mask]
readings = readings[mask]
fig, ax = plt.subplots()
ax.plot(times, readings, label='Capacitance over time')
point, = ax.plot([],[],'ro')
ax.set_xlabel('Time')
ax.set_ylabel('Capacitance')
ax.set_xlim(np.min(times), np.max(times)) 
ax.set_ylim(np.min(readings)-1, np.max(readings) + 1)
ax.legend()

print('times shape: ', times.shape)
print('readings shape: ', readings.shape)

def init():
    point.set_data([],[])
    return point,

def animate(i):
    # print(times[i], readings[i])
    if i < len(times) and i < len(readings):
        x_val = float(times[i])
        y_val = float(readings[i])
        print(f"Animating point at ({x_val}, {y_val})")
        point.set_data([x_val], [y_val])
    return point,

ani = FuncAnimation(fig, animate, frames = len(times), init_func=init, blit=True)

ani.save('animation.gif', writer="pillow", fps=30)

# plt.show()