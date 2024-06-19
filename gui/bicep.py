
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np



mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Calculate angles
def calculate_angle(a, b, c):
 a = np.array(a)  # First
 b = np.array(b)  # Mid
 c = np.array(c)  # End
 
 radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
 angle = np.abs(radians * 180.0 / np.pi)
 
 if angle > 180.0:
  angle = 360 - angle
 
 return angle


# Curl counter
bicep_counter = [0]
def bicep():
 cap = cv2.VideoCapture(0)
 camera_feed_placeholder = st.empty()
 # Check if the "Stop" button is clicked
 stop_button = st.button("Stop")
 if stop_button:
     # Release the camera when done
     cap.release()
     # Clear the placeholder image
     camera_feed_placeholder.empty()
     # Update the stream status to stop
     st.session_state.stream_status["running"] = False
     return
 
 # Set the window dimensions
 window_width = 1280
 window_height = 720
 
 # Curl counter variables
 counter = 0
 stage = '0'
 
 counter1 = 0
 stage1 = '0'
 
 angle = 0
 angle1 = 0
 
 ## Setup mediapipe instance
 with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
  while cap.isOpened():
   ret, frame = cap.read()
   
   # Recolor image to RGB
   image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   image.flags.writeable = False
   
   # Make detection
   results = pose.process(image)
   
   # Recolor back to BGR
   image.flags.writeable = True
   image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
   
   # Extract landmarks
   try:
    landmarks = results.pose_landmarks.landmark
    
    # Get coordinates
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    
    shoulder1 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbow1 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wrist1 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    # Calculate angle
    angle = calculate_angle(shoulder, elbow, wrist)
    angle1 = calculate_angle(shoulder1, elbow1, wrist1)
    
    # Visualize angle
    cv2.putText(image, str(angle),
                tuple(np.multiply(elbow, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                )
    
    cv2.putText(image, str(angle1),
                tuple(np.multiply(elbow1, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                )
    
    # # Curl counter logic
    # if angle > 160:
    #  stage = "down"
    # if angle < 30 and stage == 'down':
    #  stage = "up"
    #  counter += 1
    #  bicep_counter[0] += 1
    #  print(counter)
    #
    #
    #
    # if angle1 > 160:
    #  stage1 = "down"
    # if angle1 < 30 and stage1 == 'down':
    #  stage1 = "up"
    #  counter1 += 1
    #  bicep_counter[0] += 1
    #  print(counter1)
     
   
   
   
   except:
    pass
   
   # Render curl counter
   # Setup status box
   cv2.rectangle(image, (0, 0), (900, 100), (245, 117, 16), -1)
   
   # Rep data
   cv2.putText(image, 'REPS', (15, 12),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
   cv2.putText(image, str(counter),
               (15, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (245, 245, 245), 1, cv2.LINE_AA)
   
   # Stage data
   cv2.putText(image, 'STAGE', (145, 12),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
   cv2.putText(image, str(stage),
               (145, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (245, 245, 245), 1, cv2.LINE_AA)
   
   cv2.putText(image, 'REPS', (350, 12),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
   cv2.putText(image, str(counter1),
               (350, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (245, 245, 245), 1, cv2.LINE_AA)
   
   cv2.putText(image, 'STAGE', (450, 12),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
   cv2.putText(image, str(stage1),
               (450, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (245, 245, 245), 1
               , cv2.LINE_AA)

   if 20 < angle1 < 170:
    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2, circle_radius = 2),
                              mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2, circle_radius = 2)
                              )
   elif 20 < angle < 170:
    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2, circle_radius = 2),
                              mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2, circle_radius = 2)
                              )
   else:
    # Render detections
    # Curl counter logic
    if angle > 160:
     stage = "down"
    if angle < 30 and stage == 'down':
     stage = "up"
     counter += 1
     bicep_counter[0] += 1
     print(counter)

    if angle1 > 160:
     stage1 = "down"
    if angle1 < 30 and stage1 == 'down':
     stage1 = "up"
     counter1 += 1
     bicep_counter[0] += 1
     print(counter1)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2, circle_radius = 2),
                              mp_drawing.DrawingSpec(color = (0, 0, 255), thickness = 2, circle_radius = 2))
   
   # cv2.imshow('Mediapipe Feed', image)
   camera_feed_placeholder.image(image, caption = "Camera Feed", channels = "BGR", use_column_width = True)
   
   if cv2.waitKey(10) & 0xFF == ord('q'):
    break
  
  cap.release()
  cv2.destroyAllWindows()