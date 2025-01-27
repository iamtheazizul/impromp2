import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Moving average buffer and parameters
buffer_size = 10
x_coords_buffer = np.zeros(buffer_size)
y_coords_buffer = np.zeros(buffer_size)
buffer_index = 0

# Individual cooldowns for each direction
last_alert_time_left = last_alert_time_right = last_alert_time_up = last_alert_time_down = 0
alert_cooldown = 2  # Seconds

horizontal_movement_threshold_left = 0.05
horizontal_movement_threshold_right = 0.05
vertical_movement_threshold_up = 0.05
vertical_movement_threshold_down = 0.05

# Open the file for writing
with open('head_movements.log', 'w') as file:
    def update_buffer(buffer, index, value):
        buffer[index % len(buffer)] = value
        return (index + 1) % len(buffer), np.mean(buffer)
    
    def capture_neutral_position(video_path, pose):
        print("Capturing neutral position from the video.")
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Cannot open video file")
            return None
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture a frame for calibration.")
            return None
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        cap.release()
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            neutral_nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y
            print("Neutral position captured.")
            return neutral_nose_y
        else:
            print("Failed to detect pose in calibration frame.")
            return None


    video_path = '/Users/jacob/Desktop/SBUHacks_SkidBits/Jacobs_Folder/recorded-video.webm'  # Change this to your video file path
    neutral_nose_y = capture_neutral_position(video_path, pose)
    video_path = 'D:/Recycle Bin/Video/sample.mp4'  # Change this to your video file path
    neutral_nose_y = capture_neutral_position(video_path, pose)

    if neutral_nose_y is None:
        exit()

    # Open the video file again for processing
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Cannot open video file")
        exit()

    calibration_complete_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break

        current_time = time.time()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            nose_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x
            nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y
            buffer_index, smoothed_nose_x = update_buffer(x_coords_buffer, buffer_index, nose_x)
            _, smoothed_nose_y = update_buffer(y_coords_buffer, buffer_index, nose_y)

            ear_midpoint_x = (landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x + landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x) / 2

            if smoothed_nose_x > ear_midpoint_x + horizontal_movement_threshold_left and current_time - last_alert_time_left > alert_cooldown:
                file.write("You looked to the right.\n")
                last_alert_time_left = current_time
            elif smoothed_nose_x < ear_midpoint_x - horizontal_movement_threshold_right and current_time - last_alert_time_right > alert_cooldown:
                file.write("You looked to the left.\n")
                last_alert_time_right = current_time

            if smoothed_nose_y < neutral_nose_y - vertical_movement_threshold_up and current_time - last_alert_time_up > alert_cooldown:
                file.write("You looked up.\n")
                last_alert_time_up = current_time
            elif smoothed_nose_y > neutral_nose_y + vertical_movement_threshold_down and current_time - last_alert_time_down > alert_cooldown:
                file.write("You looked down.\n")
                last_alert_time_down = current_time

    cap.release()
    cv2.destroyAllWindows()
