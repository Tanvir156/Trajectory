import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import websocket
import json

fig = plt.figure(facecolor='black')
ax = fig.add_subplot(111, projection='3d', facecolor='black')

x_list = []
y_list = []
z_list = []

# Define a global start position variable
start_pos = None

def update_plot():
    global start_pos  # Access global start_pos variable
    
    ax.clear()
    ax.plot(x_list, y_list, z_list, '-', linewidth=2, color='red', alpha=0.5)
    ax.plot(x_list[-1:], y_list[-1:], z_list[-1:], 'o', markersize=5, color='red')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_xlim3d([-10, 10])
    ax.set_ylim3d([-10, 10])
    ax.set_zlim3d([-10, 10])
    
    # Adjust start position to the first received values from gyroscope sensor
    if start_pos is None:
        start_pos = np.array([x_list[0], y_list[0], z_list[0]])
    
    # Shift all points to start from the origin (0, 0, 0)
    x_shifted = np.array(x_list) - start_pos[0]
    y_shifted = np.array(y_list) - start_pos[1]
    z_shifted = np.array(z_list) - start_pos[2]
    
    ax.plot(x_shifted, y_shifted, z_shifted, '-', linewidth=2, color='red', alpha=0.5)
    ax.plot(x_shifted[-1:], y_shifted[-1:], z_shifted[-1:], 'o', markersize=5, color='red')
    
    plt.draw()
    plt.pause(0.0001)


def on_message(ws, message):
    global start_pos  # Access global start_pos variable
    
    values = json.loads(message)['values']
    x = values[0] * 6
    y = values[1] * 6
    z = values[2] * 6
    
    print(f"x = {x} , y = {y} , z = {z}")
    
    if len(x_list) > 0:
        prev_x, prev_y, prev_z = x_list[-1], y_list[-1], z_list[-1]
        dist = np.sqrt((x-prev_x)**2 + (y-prev_y)**2 + (z-prev_z)**2)
        if dist >= 7:  # only update plot if distance is >= 1 meter
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
            update_plot()
    else:  # for the first data point, always add it and update plot
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
        update_plot()

def on_error(ws, error):
    print("error occurred")
    print(error)

def on_close(ws, close_code, reason):
    print("connection close")
    print("close code : ", close_code)
    print("reason : ", reason)

def on_open(ws):
    print("connected")

def connect(url):
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()

connect("ws://192.168.0.100:8080/sensor/connect?type=android.sensor.gyroscope")

plt.show()
