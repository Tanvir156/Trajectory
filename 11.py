import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from monovideoodometery import MonoVideoOdometery

# Camera calibration parameters
focal = 718.8560
pp = (607.1928, 185.2157)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(21,21), criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 30, 0.01))

# Create a video capture object for the laptop camera
cap = cv.VideoCapture(0)

# Create an instance of the MonoVideoOdometry class
vo = MonoVideoOdometery(focal=focal, pp=pp, lk_params=lk_params)

# Create an empty numpy array for the trajectory visualization
traj = np.zeros((600, 800, 3), dtype=np.uint8)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Set the current frame in the MonoVideoOdometry instance
    vo.set_current_frame(frame)

    # Process the current frame and update the visual odometry
    vo.process_frame()

    # Get the estimated camera pose
    pose = vo.get_camera_pose()

    # Display the current frame and the estimated camera pose
    cv.imshow('frame', frame)
    print('Estimated camera pose:')
    print(pose)

    # Draw the estimated camera trajectory on the trajectory visualization
    x, y, z = pose[:3, 3]
    x, z = int(x) + 400, int(z) + 100
    traj = cv.circle(traj, (x, z), 1, (0, 255, 0), 2)
    cv.imshow('trajectory', traj)

    # Exit if the 'q' key is pressed
    if cv.waitKey(1) == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv.destroyAllWindows()
