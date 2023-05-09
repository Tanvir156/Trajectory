import matplotlib.pyplot as plt
import numpy as np

import websocket
import json

fig, ax = plt.subplots(facecolor='black')

x_list = []
y_list = []

def update_plot():
    ax.clear()
    ax.plot(x_list, y_list, '-', linewidth=2, color='red', alpha=0.5)
    ax.plot(x_list[-1:], y_list[-1:], 'o', markersize=5, color='red')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    plt.draw()
    plt.pause(0.0001)

def on_message(ws, message):
    values = json.loads(message)['values']
    x = values[0] * 4
    y = values[1] * 4
    print(f"x = {x} , y = {y}")
    if len(x_list) > 0:
        prev_x, prev_y = x_list[-1], y_list[-1]
        dist = np.sqrt((x-prev_x)**2 + (y-prev_y)**2)
        if dist >= 2:  # only update plot if distance is >= 1 meter
            x_list.append(x)
            y_list.append(y)
            update_plot()
    else:  # for the first data point, always add it and update plot
        x_list.append(x)
        y_list.append(y)
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
