import cv2
import numpy as np
K = np.array([[600, 0, 320],
              [0, 600, 240],
              [0, 0, 1]])

# Set the camera intrinsic parameters

# Initialize the feature detector and descriptor extractor
detector = cv2.FastFeatureDetector_create()
extractor = cv2.SIFT_create()

# Initialize some variables
prev_frame = None
prev_kp = None
prev_des = None
R_f = np.eye(3)
t_f = np.zeros((3, 1))
trajectory = np.zeros((600, 800, 3), dtype=np.uint8)

# Start the video stream from IP Webcam
cap = cv2.VideoCapture("http://192.168.0.106:8080/video")

while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to a smaller size for faster processing
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_frame is None:
        # First frame, detect features and descriptors
        prev_frame = gray
        prev_kp = detector.detect(prev_frame)
        prev_kp, prev_des = extractor.compute(prev_frame, prev_kp)
        prev_points = np.array([kp.pt for kp in prev_kp], dtype=np.float32).reshape(-1, 1, 2)
        continue

    # Track features and estimate camera motion
    curr_kp, curr_des = extractor.detectAndCompute(gray, None)
    if len(curr_kp) < 10:
        continue

    curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_frame, gray, prev_points, None)
    prev_points = curr_points[status == 1]
    curr_points = curr_points[status == 1]
    curr_des = curr_des[status == 1]

    E, mask = cv2.findEssentialMat(curr_points, prev_points, K, cv2.RANSAC, 0.999, 1.0, None)
    _, R, t, mask = cv2.recoverPose(E, curr_points, prev_points, K, None, None, None)

    # Update the camera pose
    t_f = t_f + R_f.dot(t)
    R_f = R.dot(R_f)

    # Draw the estimated camera pose on the trajectory
    x, y, z = t_f
    draw_x, draw_y = int(x) + 300, int(z) + 100
    cv2.circle(trajectory, (draw_x, draw_y), 1, (0, 255, 0), 2)
    cv2.rectangle(trajectory, (10, 30), (550, 50), (0, 0, 0), -1)
    cv2.putText(trajectory, "Coordinates: x=%2fm y=%2fm z=%2fm" % (x, y, z), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Display the current frame with the estimated camera pose
    cv2.imshow('frame', frame)
    cv2.imshow('trajectory', trajectory)

    # Wait for keypress to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()
