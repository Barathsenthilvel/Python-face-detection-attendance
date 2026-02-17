# Face Recognition Based Attendance System

A complete Face Recognition Based Attendance System using Python, OpenCV, and Tkinter. This system captures student faces, trains a recognition model, and marks attendance in real-time, exporting the data to CSV/Excel.

## Features
- **Student Registration**: Capture student faces using a webcam or mobile camera.
- **Face Training**: Generate encodings for recognized faces.
- **Real-time Attendance**: Detect and recognize faces to mark attendance automatically.
- **Duplicate Prevention**: Prevents marking attendance multiple times for the same student on the same day.
- **Attendance View**: View today's attendance and export to Excel.
- **Mobile Camera Support**: Seamlessly use DroidCam or IP Webcam.

## Prerequisites
- Python 3.8+
- Visual Studio C++ Build Tools (required for `dlib` installation on Windows)

## Installation

1. **Clone or Download the Project**
   ```bash
   cd face_attendance_system
   ```

2. **Install Dependencies**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If `dlib` fails to install, ensure you have CMake and C++ Build Tools installed.*

## Usage

1. **Run the Application**
   Navigate to the `ui` folder or run from root (recommended to run via a driver script if created, but `ui/main_ui.py` handles path appending):
   ```bash
   python ui/main_ui.py
   ```

2. **Mobile Camera Setup (DroidCam)**
   - Install **DroidCam** on your phone and PC (optional client).
   - Connect via Wi-Fi (ensure Phone and PC are on the same network).
   - Open the App, note the IP address (e.g., `192.168.1.10`).
   - The stream URL is usually `http://192.168.1.10:4747/video`.
   - In the Application, click **Camera Settings**.
   - Enter the URL (e.g., `http://192.168.1.10:4747/video`) or `0` for default webcam.
   - Click **Save**.

3. **Workflow**
   - **Register New Student**: Enter Roll No and Name. The camera will open. Look at the camera until 20 images are captured.
   - **Train Face Encodings**: Click this button after registering new students. This generates the `encodings.pickle` file.
   - **Start Attendance**: Opens the camera for recognition. Press `q` to stop. Recognized faces will satisfy the attendance.
   - **View Attendance**: Shows today's records. You can export to Excel.

## Project Structure
- `dataset/`: Stores captured student images.
- `encodings/`: Stores the trained face encodings.
- `attendance/`: Stores daily attendance CSV files.
- `ui/`: Contains the Graphical User Interface.
- `register_student.py`: Logic for capturing images.
- `train_faces.py`: Logic for training the model.
- `recognize_attendance.py`: Logic for recognition and marking.
- `utils.py`: Helper functions.

## Troubleshooting
- **Camera not opening?** Check the Camera Settings and ensure the correct Source ID (0, 1) or URL is provided.
- **dlib installation error?** Try installing `cmake` first: `pip install cmake`, then try again.



<!-- installation steup -->

pip install cmake
pip install dlib
pip install -r requirements.txt