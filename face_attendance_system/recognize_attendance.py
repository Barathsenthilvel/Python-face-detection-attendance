import face_recognition
import cv2
import pickle
import os
import numpy as np
from utils import mark_attendance, get_camera_source
import time

def recognize_faces():
    encodings_path = "encodings/encodings.pickle"
    
    if not os.path.exists(encodings_path):
        print("Encodings file not found. Please train the faces first.")
        return

    print("Loading encodings...")
    data = pickle.loads(open(encodings_path, "rb").read())
    
    known_encodings = data["encodings"]
    known_names = data["names"]
    
    print("Starting camera for attendance...")
    # Open camera from config
    source = get_camera_source()
    video_capture = cv2.VideoCapture(source)
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            roll_no = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    identifier = known_names[best_match_index]
                    
                    # Split identifier "Roll-Name"
                    parts = identifier.split('-')
                    if len(parts) >= 2:
                        roll_no = parts[0]
                        name = parts[1]
                    else:
                        name = identifier
                        
                    # Mark attendance
                    status = mark_attendance(roll_no, name)
                    print(f"{name} ({roll_no}): {status}")

            face_names.append(f"{name}")
            
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)

        cv2.imshow('Face Recognition Attendance', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
