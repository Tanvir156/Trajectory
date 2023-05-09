import cv2
import numpy as np
from plyer import accelerometer, orientation

# Enable the accelerometer and gyroscope sensors
accelerometer.enable()
orientation.enable()

# Replace the IP address with your IP Webcam server address
url = 'http://192.168.0.101:8080/video'

# Open the video stream
cap = cv2.VideoCapture(url)

# Define the desired frame width and height
frame_width = 640
frame_height = 480

# Create an empty mask
mask = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

# Define the initial position
x, y = 0, 0

# Loop through the frames
while True:
    # Read the next frame from the video stream
    ret, frame = cap.read()

    # Resize the frame to the desired size
    frame = cv2.resize(frame, (frame_width, frame_height))

    # Get the latest sensor data
    acc_data = accelerometer.acceleration[:3]
    gyro_data = orientation.orientation[:3]

    # Draw a line from the previous position to the current position
    x1, y1 = x, y
    x2, y2 = x + 10, y + 10
    x1, y1 = int(x1), int(y1)
    x2, y2 = int(x2), int(y2)
    mask = cv2.line(mask, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

    # Display the frame and mask
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    # Update the position
    x, y = x + 10, y + 10

    # Print the sensor data
    print("Accelerometer data:", acc_data)
    print("Gyroscope data:", gyro_data)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream
cap.release()

# Disable the sensors when finished
accelerometer.disable()
orientation.disable()

# Close all windows
cv2.destroyAllWindows()
