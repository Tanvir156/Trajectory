import cv2
import numpy as np
import matplotlib.pyplot as plt
cap = cv2.VideoCapture('video.mp4')
frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
# Create a feature detector
orb = cv2.ORB_create()

# Detect features in the first frame
kp1, des1 = orb.detectAndCompute(frames[0], None)

# Initialize the previous keypoint and descriptor
prev_kp, prev_des = kp1, des1

# Loop through all the frames and perform feature detection and tracking
for i in range(1, len(frames)):
    # Detect features in the current frame
    kp2, des2 = orb.detectAndCompute(frames[i], None)
    
    # Match the features between the previous and current frame
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(prev_des, des2)
    
    # Filter the matches based on their distance
    good_matches = []
    for m in matches:
        if m.distance < 50:
            good_matches.append(m)
    
    # Get the matched keypoints in both frames
    prev_pts = np.float32([prev_kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    curr_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    # Compute the optical flow between the matched keypoints
    flow = cv2.calcOpticalFlowPyrLK(frames[i-1], frames[i], prev_pts, curr_pts)
    
    # Extract the motion vectors from the optical flow
    dx = flow[:, :, 0].mean()
    dy = flow[:, :, 1].mean()
    
    # Compute the position of the camera in the current frame
    x, y = prev_kp[0].pt[0] + dx, prev_kp[0].pt[1] + dy
    
    # Draw a line between the previous and current positions
    cv2.line(frames[i], (int(prev_kp[0].pt[0]), int(prev_kp[0].pt[1])),
             (int(x), int(y)), (0, 0, 255), 2)
    
    # Update the previous keypoint and descriptor
    prev_kp, prev_des = kp2, des2
# Display the video with the trajectory line
for frame in frames:
    cv2.imshow('Video', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
