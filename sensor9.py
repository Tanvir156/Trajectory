import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import websocket
import json

fig = plt.figure(facecolor='white')  # Set the facecolor of the figure to white
ax = fig.add_subplot(111, projection='3d')

x_list = []
y_list = []
z_list = []

start_pos = None  # Initialize the start position

def update_plot():
    ax.clear()
    ax.plot(x_list, y_list, z_list, '-', linewidth=2, color='red', alpha=0.5)
    ax.plot(x_list[-1:], y_list[-1:], z_list[-1:], 'o', markersize=5, color='red')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_xlim3d([-10, 10])
    ax.set_ylim3d([-10, 10])
    ax.set_zlim3d([-10, 10])
    
    # Set the color of the axes spines to black
    ax.w_xaxis.line.set_color("black")
    ax.w_yaxis.line.set_color("black")
    ax.w_zaxis.line.set_color("black")
    
    # Calculate the limits of the plot based on the data
    if len(x_list) > 0:
        x_range = max(x_list) - min(x_list)
        y_range = max(y_list) - min(y_list)
        z_range = max(z_list) - min(z_list)
        max_range = max(x_range, y_range, z_range)
        center_x = (max(x_list) + min(x_list)) / 2
        center_y = (max(y_list) + min(y_list)) / 2
        center_z = (max(z_list) + min(z_list)) / 2
        ax.set_xlim3d([center_x - max_range, center_x + max_range])
        ax.set_ylim3d([center_y - max_range, center_y + max_range])
        ax.set_zlim3d([center_z - max_range, center_z + max_range])

    plt.draw()
    plt.pause(0.0001)


def on_message(ws, message):
    global start_pos
    values = json.loads(message)['values']
    x = values[0] * 6
    y = values[1] * 6
    z = values[2] * 6
    print(f"x = {x} , y = {y} , z = {z}")
    if start_pos is None:  # Set the start position if it hasn't been set already
        start_pos = (x, y, z)
    if len(x_list) > 4:
        prev_x, prev_y, prev_z = x_list[-1], y_list[-1], z_list[-1]
        dist = np.sqrt((x-prev_x)**2 + (y-prev_y)**2 + (z-prev_z)**2)
        if dist >= 1:  # only update plot if distance is >= 1 meter
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
            update_plot()
    else:  # for the first data point, always add it and update plot
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
        update_plot()


# Rest of the code is the same as before

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
