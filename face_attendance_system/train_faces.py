import face_recognition
import os
import pickle
import cv2

def train_faces():
    dataset_dir = "dataset"
    encodings_path = "encodings/encodings.pickle"
    
    if not os.path.exists(dataset_dir):
        print("Dataset directory not found. Please register students first.")
        return

    print("Starting training... This might take a while depending on the number of images.")
    
    known_encodings = []
    known_names = []
    
    # helper for checking extensions
    valid_extensions = ('.jpg', '.jpeg', '.png')
    
    image_paths = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.lower().endswith(valid_extensions)]
    
    if not image_paths:
        print("No images found in dataset.")
        return
        
    for i, image_path in enumerate(image_paths):
        print(f"Processing image {i+1}/{len(image_paths)}: {image_path}")
        
        # Extract ID and Name from filename: roll_name_count.jpg
        filename = os.path.basename(image_path)
        try:
            # Check format
            parts = filename.split('_')
            if len(parts) >= 3:
                roll_no = parts[0]
                name = parts[1]
                identifier = f"{roll_no}-{name}"
            else:
                print(f"Skipping {filename}: Incorrect format")
                continue
                
            # Load image
            image = face_recognition.load_image_file(image_path)
            # Convert to RGB (face_recognition uses RGB)
            # OpenCV loads as BGR so if we used cv2 here we'd convert. 
            # face_recognition.load_image_file uses PIL/scipy which is RGB.
            
            # Detect faces
            boxes = face_recognition.face_locations(image, model="hog") # use 'cnn' if GPU is available
            
            # Compute encodings
            encodings = face_recognition.face_encodings(image, boxes)
            
            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(identifier)
                
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            
    # Save encodings
    data = {"encodings": known_encodings, "names": known_names}
    
    if not os.path.exists("encodings"):
        os.makedirs("encodings")
        
    with open(encodings_path, "wb") as f:
        pickle.dump(data, f)
        
    print(f"Training complete. Encodings saved to {encodings_path}")

if __name__ == "__main__":
    train_faces()
