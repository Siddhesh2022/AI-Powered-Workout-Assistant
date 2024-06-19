import streamlit as st
import cv2
from imutils.video import VideoStream
import imutils
import numpy as np
import time
import mediapipe as mp
import pandas as pd
import pickle



def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle


# # Initialize session_state
# if "stream_status" not in st.session_state:
#     st.session_state.stream_status = {"running": False}

mp_drawing = mp.solutions.drawing_utils # drawing helpers
mp_pose = mp.solutions.pose

landmarks = ['class']
for val in range(1, 33+1):
    landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val), 'v{}'.format(val)]


with open('../models/deadlift_coords.pkl', 'rb') as f:
    model = pickle.load(f)
    
with open('../models/pushups.pkl', 'rb') as f:
    model2 = pickle.load(f)




deadlift_counter = [0]
deadlift_accuracy = [0]
pushup_counter = [0]
pushup_accuracy = [0]
squat_counter = [0]
squat_accuracy = [0]

def deadlift():
    
    # for deadlift, pushups

    # Add a condition to display the "Start" button and camera feed
    deadlift_counter[0] = 0
    deadlift_accuracy.clear()
    current_stage = ''
    
    cap = cv2.VideoCapture(0)
    camera_feed_placeholder = st.empty()
    
   

    # Check if the "Stop" button is clicked
    # stop_button = st.button("Stop")
    if st.button("Stop"):
        # Release the camera when done
        cap.release()
        # Clear the placeholder image
        camera_feed_placeholder.empty()
        # Update the stream status to stop
        st.session_state.stream_status["running"] = False
        return

    
    # initiate holistic model
    
    with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
        while cap.isOpened():
            
            ret, image = cap.read()
            # recolor feed
            
            image = cv2.resize(image, (640, 380))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # make detections
            
            results = pose.process(image)

            # recolor
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            print("i am before try")
            
            try:
                
                landmark_points = results.pose_landmarks.landmark
    
                print("i am try")
                # landmarks = results.pose_landmarks.landmark
                print("i am after landmarks")
                hip = [landmark_points[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       landmark_points[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmark_points[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmark_points[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmark_points[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                         landmark_points[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                knee1 = [landmark_points[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                         landmark_points[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                hip1 = [landmark_points[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmark_points[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                hip_mid = [(x + y) / 2 for x, y in zip(hip, hip1)]
                angle = calculate_angle(ankle, knee, hip)
                leg_angle = calculate_angle(knee, hip_mid, knee1)

                row = np.array(
                    [[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten()
                x = pd.DataFrame([row], columns = landmarks[1:])
                body_language_class = model.predict(x)[0]
                body_language_prob = model.predict_proba(x)[0]
                print(body_language_class, body_language_prob)

                # Visualize angle
                cv2.putText(image, str(leg_angle),
                            tuple(np.multiply(hip, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )
               
                if 30 <= leg_angle <= 180:
                    if body_language_class == 'down' and body_language_prob[body_language_prob.argmax()] >= .7:
                        current_stage = 'down'
                    elif current_stage == 'down' and body_language_class == 'up' and body_language_prob[
                        body_language_prob.argmax()] <= .7:
                        current_stage = 'up'
                        deadlift_counter
                        deadlift_counter[0] += 1
                        deadlift_accuracy.append(round(body_language_prob[np.argmax(body_language_prob)], 2))
                        print(current_stage)

                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                                                                     circle_radius = 4),
                                              mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2,
                                                                     circle_radius = 2))
                    
                    # if 20 <= angle <= 160:
                    #     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    #                               mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                    #                                                      circle_radius = 4),
                    #                               mp_drawing.DrawingSpec(color = (245, 66, 230), thickness = 2,
                    #                                                      circle_radius = 2))
                    # else:
                    #     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    #                               mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                    #                                                      circle_radius = 4),
                    #                               mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2,
                    #                                                      circle_radius = 2))
                elif (30 <= leg_angle <= 170) and current_stage == "down":
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                                                                     circle_radius = 4),
                                              mp_drawing.DrawingSpec(color = (0, 0, 255), thickness = 2,
                                                                     circle_radius = 2))
                else:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                                                                     circle_radius = 4),
                                              mp_drawing.DrawingSpec(color = (0, 0, 255), thickness = 2,
                                                                     circle_radius = 2))
                    
                  
                  
                # if body_language_class == 'down' and body_language_prob[body_language_prob.argmax()] >= .7:
                #     current_stage = 'down'
                # elif current_stage == 'down' and body_language_class == 'up' and body_language_prob[
                #     body_language_prob.argmax()] <= .7:
                #     current_stage = 'up'
                #     counter += 1
                #     print(current_stage)
                    
                    
                    
                
                    
                
                # status box
                cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)
                
                # display class
                cv2.putText(image, 'CLASS'
                            , (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, body_language_class.split(' ')[0]
                            , (95, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                # display probablity
                cv2.putText(image, 'PROB'
                            , (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2))
                            , (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                # display probablity
                cv2.putText(image, 'COUNT'
                            , (180, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(deadlift_counter[0])
                            , (175, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # round(body_language_prob[np.argmax(body_language_prob)], 2)

                

    
            
            
            except Exception as e:
                pass
            
            
            camera_feed_placeholder.image(image, caption = "Camera Feed", channels = "BGR", use_column_width = True)
    
            
            
    cap.release()
    cv2.destroyAllWindows()
    
    



# for push-ups
def pushup2():
    # for deadlift, pushups
    
    # Add a condition to display the "Start" button and camera feed
    pushup_counter[0] = 0
    pushup_accuracy.clear()
    
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
    
    # counter = 0
    current_stage = ''
    # initiate holistic model
    
    with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
        while cap.isOpened():
            ret, image = cap.read()
            # recolor feed
            
            image = cv2.resize(image, (640, 380))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # make detections
            
            results = pose.process(image)
            
            # recolor
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            #                           mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2, circle_radius = 4),
            #                           mp_drawing.DrawingSpec(color = (245, 66, 230), thickness = 2, circle_radius = 2))
            
            try:
 
                landmark_points = results.pose_landmarks.landmark
 
                print("i am try")
                # landmarks = results.pose_landmarks.landmark
                print("i am after landmarks")
                shoulder = [landmark_points[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                       landmark_points[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmark_points[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmark_points[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmark_points[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmark_points[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                angle = calculate_angle(shoulder, elbow, wrist)
             
               
                # landmarks = results.pose_landmarks.landmark
                row = np.array(
                    [[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten()
                x = pd.DataFrame([row], columns = landmarks[1:])
                body_language_class = model2.predict(x)[0]
                body_language_prob = model2.predict_proba(x)[0]
                print(body_language_class, body_language_prob)
                
                if 100 < angle < 170:
                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                           mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                                                                  circle_radius = 4),
                                           mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2,
                                                                  circle_radius = 2))
                else:
                 if body_language_class == 'down' and body_language_prob[body_language_prob.argmax()] >= .7:
                  current_stage = 'down'
                 elif current_stage == 'down' and body_language_class == 'up' and body_language_prob[
                  body_language_prob.argmax()] <= .7:
                  current_stage = 'up'
  
                  pushup_counter[0] += 1
                  pushup_accuracy.append(round(body_language_prob[np.argmax(body_language_prob)], 2))
                  print(current_stage)

                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                           mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                                                                  circle_radius = 4),
                                           mp_drawing.DrawingSpec(color = (0, 0, 255), thickness = 2,
                                                                  circle_radius = 2))


                cv2.putText(image, str(angle),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )
                
                # status box
                cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)
                
                # display class
                cv2.putText(image, 'CLASS'
                            , (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, body_language_class.split(' ')[0]
                            , (95, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                # display probablity
                cv2.putText(image, 'PROB'
                            , (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2))
                            , (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                # display counter
                cv2.putText(image, 'COUNT'
                            , (180, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(pushup_counter[0])
                            , (175, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            
            
            
            
            except Exception as e:
                pass
            
            # cv2.imshow('Raw Webcam Feed', image)
            camera_feed_placeholder.image(image, caption = "Camera Feed", channels = "BGR", use_column_width = True)
            # Check if the "Stop" button is clicked
            # if st.button("Stop"):
            #     # Release the camera when done
            #     cap.release()
            #     # Clear the placeholder image
            #     camera_feed_placeholder.empty()
            #     # Update the stream status to stop
            #     st.session_state.stream_status["running"] = False
            #     break
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()


def squats():
 # for deadlift, pushups
 
 # Add a condition to display the "Start" button and camera feed
 squat_counter[0] = 0
 squat_accuracy.clear()
 current_stage = ''
 
 cap = cv2.VideoCapture(0)
 camera_feed_placeholder = st.empty()
 
 # Check if the "Stop" button is clicked
 # stop_button = st.button("Stop")
 if st.button("Stop"):
  # Release the camera when done
  cap.release()
  # Clear the placeholder image
  camera_feed_placeholder.empty()
  # Update the stream status to stop
  st.session_state.stream_status["running"] = False
  return
 
 # initiate holistic model
 
 with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
  while cap.isOpened():
   
   ret, image = cap.read()
   # recolor feed
   
   image = cv2.resize(image, (640, 380))
   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
   image.flags.writeable = False
   
   # make detections
   
   results = pose.process(image)
   
   # recolor
   image.flags.writeable = True
   image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
   print("i am before try")
   
   try:
    
    landmark_points = results.pose_landmarks.landmark
    
    print("i am try")
    # landmarks = results.pose_landmarks.landmark
    print("i am after landmarks")
    hip = [landmark_points[mp_pose.PoseLandmark.LEFT_HIP.value].x,
           landmark_points[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    knee = [landmark_points[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmark_points[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    ankle = [landmark_points[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
             landmark_points[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    knee1 = [landmark_points[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
             landmark_points[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    hip1 = [landmark_points[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
            landmark_points[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    
    hip_mid = [(x + y) / 2 for x, y in zip(hip, hip1)]
    angle = calculate_angle(ankle, knee, hip)
    leg_angle = calculate_angle(knee, hip_mid, knee1)
    
    row = np.array(
     [[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten()
    x = pd.DataFrame([row], columns = landmarks[1:])
    body_language_class = model.predict(x)[0]
    body_language_prob = model.predict_proba(x)[0]
    print(body_language_class, body_language_prob)
    
    # Visualize angle
    cv2.putText(image, str(leg_angle),
                tuple(np.multiply(hip, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                )
    
    if 30 <= leg_angle <= 180:
     if body_language_class == 'down' and body_language_prob[body_language_prob.argmax()] >= .7:
      current_stage = 'down'
     elif current_stage == 'down' and body_language_class == 'up' and body_language_prob[
      body_language_prob.argmax()] <= .7:
      current_stage = 'up'
      squat_counter[0] += 1
      squat_accuracy.append(round(body_language_prob[np.argmax(body_language_prob)], 2))
      print(current_stage)
     
     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                               mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                                                      circle_radius = 4),
                               mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2,
                                                      circle_radius = 2))
     
     # if 20 <= angle <= 160:
     #     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
     #                               mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
     #                                                      circle_radius = 4),
     #                               mp_drawing.DrawingSpec(color = (245, 66, 230), thickness = 2,
     #                                                      circle_radius = 2))
     # else:
     #     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
     #                               mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
     #                                                      circle_radius = 4),
     #                               mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2,
     #                                                      circle_radius = 2))
    elif (30 <= leg_angle <= 170) and current_stage == "down":
     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                               mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                                                      circle_radius = 4),
                               mp_drawing.DrawingSpec(color = (0, 0, 255), thickness = 2,
                                                      circle_radius = 2))
    else:
     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                               mp_drawing.DrawingSpec(color = (245, 117, 66), thickness = 2,
                                                      circle_radius = 4),
                               mp_drawing.DrawingSpec(color = (0, 0, 255), thickness = 2,
                                                      circle_radius = 2))
    
    # if body_language_class == 'down' and body_language_prob[body_language_prob.argmax()] >= .7:
    #     current_stage = 'down'
    # elif current_stage == 'down' and body_language_class == 'up' and body_language_prob[
    #     body_language_prob.argmax()] <= .7:
    #     current_stage = 'up'
    #     counter += 1
    #     print(current_stage)
    
    # status box
    cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)
    
    # display class
    cv2.putText(image, 'CLASS'
                , (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, body_language_class.split(' ')[0]
                , (95, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # display probablity
    cv2.putText(image, 'PROB'
                , (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2))
                , (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # display probablity
    cv2.putText(image, 'COUNT'
                , (180, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(squat_counter[0])
                , (175, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # round(body_language_prob[np.argmax(body_language_prob)], 2)
   
   
   
   
   
   
   except Exception as e:
    pass
   
   camera_feed_placeholder.image(image, caption = "Camera Feed", channels = "BGR", use_column_width = True)
 
 cap.release()
 cv2.destroyAllWindows()


