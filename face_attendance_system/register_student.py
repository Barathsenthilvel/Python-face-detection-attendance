import cv2
import os
import time
from utils import get_camera_source

def capture_images(roll_no, name, num_images=20):
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    
    # Open camera from config
    source = get_camera_source()
    cam = cv2.VideoCapture(source) 
    
    # We need a face detector to only save images with faces
    # Using Haar Cascade for fast detection during improved capture
    # Ensure opencv-python is installed which includes data
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    count = 0
    
    print("Starting face capture. Please look at the camera.")
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Draw rectangle/visual feedback
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Save the captured image only if face is detected
            # We save the full frame or crop. The prompt implies just 'images'. 
            # Often keeping context is okay, but cropping is cleaner for recognition.
            # Let's save the cropped face for better training data quality.
            
            # Wait a bit between captures to avoid identical frames
            # count increments only when we save
            if count < num_images:
                # Save just the face or full frame?
                # face_recognition library works on full images too. 
                # But cropping reduces noise. Let's crop.
                # Adding some padding
                # face_img = gray[y:y+h, x:x+w] # Saving grayscale or color? Color is better for some models but gray is standard.
                # face_recognition works with RGB. Let's save color frame but cropped.
                
                # Setup path
                file_name = f"{roll_no}_{name}_{count+1}.jpg"
                file_path = os.path.join(dataset_dir, file_name)
                
                # Check for key press to capture or auto-capture?
                # Auto-capture every few frames is better for UX.
                # Let's save.
                cv2.imwrite(file_path, frame[y:y+h, x:x+w])
                count += 1
                
                # Visual feedback on count
                cv2.putText(frame, f"Captured: {count}/{num_images}", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                
                time.sleep(0.2) # small delay
            
        cv2.imshow("Register Face", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q') or count == num_images:
            break
            
    cam.release()
    cv2.destroyAllWindows()
    print("Dataset collection completed!")

if __name__ == "__main__":
    r_no = input("Enter Roll Number: ")
    s_name = input("Enter Name: ")
    capture_images(r_no, s_name)
