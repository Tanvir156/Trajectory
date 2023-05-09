import cv2

# Replace the IP address with your IP Webcam server address
url = 'http://192.168.0.101:8080/video'

# Open the video stream
cap = cv2.VideoCapture(url)

# Define the desired frame width and height
frame_width = 640
frame_height = 480

# Loop through the frames
while True:
    # Read the next frame from the video stream
    ret, frame = cap.read()

    # Resize the frame to the desired size
    frame = cv2.resize(frame, (frame_width, frame_height))

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream
cap.release()

# Close all windows
cv2.destroyAllWindows()
