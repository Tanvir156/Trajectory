import websocket
import json
import turtle

# set up turtle graphics
turtle.setup(800, 800)
turtle.penup()
turtle.setposition(0, 0)
turtle.pendown()
turtle.pensize(2)

# previous x, y, z coordinates
prev_x, prev_y, prev_z = None, None, None

def on_message(ws, message):
    global prev_x, prev_y, prev_z
    
    # get x, y, z coordinates from message
    values = json.loads(message)['values']
    x, y, z = values[0]*6, values[1]*6, values[2]*6
    
    # if this is the first coordinate received, set it as the previous coordinate
    if prev_x is None and prev_y is None and prev_z is None:
        prev_x, prev_y, prev_z = x, y, z
        return
    
    # draw a line from the previous coordinate to the current coordinate
    turtle.goto(prev_x, prev_y)
    turtle.pendown()
    turtle.goto(x, y)
    turtle.penup()
    
    # update the previous coordinate to the current coordinate
    prev_x, prev_y, prev_z = x, y, z

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

# connect to websocket server
connect("ws://192.168.0.100:8080/sensor/connect?type=android.sensor.accelerometer")
