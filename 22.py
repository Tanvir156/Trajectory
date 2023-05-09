import cv2
import numpy as np

# Define the KLT parameters
lk_params = dict(winSize=(21, 21), 
                 maxLevel=3, 
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

# Initialize some variables
old_frame = None
old_points = None
trajectory = np.zeros((480, 640, 3), np.uint8)  # Create an empty image for the trajectory

# Start capturing video from the laptop camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # If this is the first frame, initialize some variables
    if old_frame is None:
        old_frame = gray
        old_points = cv2.goodFeaturesToTrack(old_frame, 200, 0.3, 7)
    
    # Track the feature points using the KLT algorithm
    new_points, status, error = cv2.calcOpticalFlowPyrLK(old_frame, gray, old_points, None, **lk_params)
    
    # Filter the good points
    good_new = new_points[status==1]
    good_old = old_points[status==1]
    
    # Compute the homography matrix
    H, mask = cv2.findHomography(good_old, good_new, cv2.RANSAC)
    
    # Extract the translation vector from the homography matrix
    dx, dy, dz = -H[0:3, 2]
    
    # Draw the trajectory
    cv2.line(trajectory, (int(dx)+320, int(dy)+240), (int(dx)+320, int(dy)+240), (0, 255, 0), 2)
    
    # Print the estimated motion
    print("dx: %.2f, dy: %.2f, dz: %.2f" % (dx, dy, dz))
    
    # Update the variables for the next frame
    old_frame = gray.copy()
    old_points = good_new.reshape(-1, 1, 2)
    
    # Display the frame and trajectory
    cv2.imshow("Frame", frame)
    cv2.imshow("Trajectory", trajectory)
    
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
