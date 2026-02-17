import os
import csv
from datetime import datetime

# Paths
DATASET_DIR = "dataset"
ENCODINGS_PATH = "encodings/encodings.pickle"
ATTENDANCE_DIR = "attendance"

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_attendance_file_path():
    ensure_directory(ATTENDANCE_DIR)
    current_date = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(ATTENDANCE_DIR, f"attendance_{current_date}.csv")

def mark_attendance(roll_no, name):
    file_path = get_attendance_file_path()
    
    # Check if file exists, if not create with header
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Roll Number", "Name", "Date", "Time"])
    
    # Read existing attendance to prevent duplicates for the day
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == roll_no:
                return "Already Marked"
    
    # Append new attendance
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([roll_no, name, current_date, current_time])
    
    return "Marked Successfully"

CONFIG_FILE = "config.txt"

def get_camera_source():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            source = f.read().strip()
            if source.isdigit():
                return int(source)
            return source
    return 0

def save_camera_source(source):
    with open(CONFIG_FILE, "w") as f:
        f.write(str(source))
