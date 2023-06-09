import websocket
import json


def on_message(ws, message):
    values = json.loads(message)['values']
    x = values[0]*5
    y = values[1]*5
    z = values[2]*5
    print(f"x = {x} , y = {y} , z = {z}")

def on_error(ws, error):
    print("error occurred")
    print(error)

def on_close(ws, close_code, reason):
    print("connection close")
    print("close code : ", close_code)
    print("reason : ", reason  )

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