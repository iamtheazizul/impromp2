import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Moving average buffer and parameters
buffer_size = 10
x_coords_buffer = np.zeros(buffer_size)
y_coords_buffer = np.zeros(buffer_size)
buffer_index = 0

# Individual cooldowns for each direction
last_alert_time_left = last_alert_time_right = last_alert_time_up = last_alert_time_down = 0
alert_cooldown = 2  # Seconds
# increasing threshold decreases sensitivity
# decreasing threshold increases sensitivity
horizontal_movement_threshold_left = 0.05  
horizontal_movement_threshold_right = 0.05  
vertical_movement_threshold_up = 0.05
vertical_movement_threshold_down = 0.05

def update_buffer(buffer, index, value):
    buffer[index % len(buffer)] = value
    return (index + 1) % len(buffer), np.mean(buffer)

# Function to perform calibration
def calibrate_neutral_position(cap, pose):
    print("Calibrating... Please look directly at the camera in a neutral position.")
    time.sleep(2)  # Gives the user time to prepare
    success, neutral_poses = [], []
    while len(neutral_poses) < 30:  # Capture 30 frames for averaging
        ret, frame = cap.read()
        if not ret:
            continue
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            neutral_poses.append(landmarks[mp_pose.PoseLandmark.NOSE.value].y)
        time.sleep(0.1)  # Wait a bit between captures
    neutral_nose_y = np.mean(neutral_poses)
    print("Calibration complete.")
    return neutral_nose_y

# Capture video from webcam.
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Calibrate neutral position
neutral_nose_y = calibrate_neutral_position(cap, pose)

# Right after calibration is complete, set a calibration time marker
calibration_complete_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    current_time = time.time()

    # Process the image
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        nose_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x
        nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y

        # Update smoothed coordinates
        buffer_index, smoothed_nose_x = update_buffer(x_coords_buffer, buffer_index, nose_x)
        _, smoothed_nose_y = update_buffer(y_coords_buffer, buffer_index, nose_y)

        ear_midpoint_x = (landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x + landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x) / 2
        eyes_midpoint_y = (landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y + landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y) / 2

        # Adjusted horizontal movement detection with individual thresholds
        if smoothed_nose_x < ear_midpoint_x - horizontal_movement_threshold_left and current_time - last_alert_time_left > alert_cooldown and current_time - calibration_complete_time > 2:
            print("You looked to the left.")
            last_alert_time_left = current_time
        elif smoothed_nose_x > ear_midpoint_x + horizontal_movement_threshold_right and current_time - last_alert_time_right > alert_cooldown:
            print("You looked to the right.")
            last_alert_time_right = current_time

        # Vertical movement detection with individual cooldowns and adjusted thresholds
        if smoothed_nose_y < neutral_nose_y - vertical_movement_threshold_up and current_time - last_alert_time_up > alert_cooldown and current_time - calibration_complete_time > 2:
            print("You looked up.")
            last_alert_time_up = current_time
        elif smoothed_nose_y > neutral_nose_y + vertical_movement_threshold_down and current_time - last_alert_time_down > alert_cooldown:
            print("You looked down.")
            last_alert_time_down = current_time

    # Display the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()
