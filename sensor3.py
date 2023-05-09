import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import websocket
import json

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x_list = []
y_list = []
z_list = []

def update_plot():
    ax.clear()
    ax.plot(x_list, y_list, z_list, 'o-', markersize=2, color='blue')
    plt.draw()
    plt.pause(0.0001)

def on_message(ws, message):
    values = json.loads(message)['values']
    x = values[0]
    y = values[1]
    z = values[2]
    print(f"x = {x} , y = {y} , z = {z}")
    if len(x_list) > 0:
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

connect("ws://192.168.0.106:8081/sensor/connect?type=android.sensor.gyroscope")

plt.show()
