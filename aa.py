
import cv2

# URL of the IP Webcam video stream
url = "http://192.168.0.101:8080/video"

# Create a VideoCapture object
cap = cv2.VideoCapture(url)

# Check if the VideoCapture object was successfully opened
if not cap.isOpened():
    print("Error opening video stream or file")

# Set the size of the resized frame
width = 640
height = 480

# Loop through the video frames
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        print("Error reading frame from video stream")
        break

    # Resize the frame to the desired size
    resized_frame = cv2.resize(frame, (width, height))

    # Display the resized frame in a window
    cv2.imshow("IP Webcam", resized_frame)

    # Wait for a key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()
