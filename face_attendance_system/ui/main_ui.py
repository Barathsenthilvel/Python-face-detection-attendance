import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import pandas as pd

# Add parent directory to path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import register_student
import train_faces
import recognize_attendance
from utils import get_attendance_file_path, save_camera_source, get_camera_source

class FaceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Header
        header = tk.Label(root, text="Student Attendance System", font=("Helvetica", 24, "bold"), bg="#4a90e2", fg="white", pady=20)
        header.pack(fill=tk.X)

        # Main Frame
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)

        # Buttons
        btn_register = tk.Button(main_frame, text="Register New Student", command=self.open_register_window, font=("Arial", 14), bg="#2ecc71", fg="white", width=20, height=2)
        btn_register.grid(row=0, column=0, padx=20, pady=20)

        btn_train = tk.Button(main_frame, text="Train Face Encodings", command=self.train_data, font=("Arial", 14), bg="#e67e22", fg="white", width=20, height=2)
        btn_train.grid(row=0, column=1, padx=20, pady=20)

        btn_attendance = tk.Button(main_frame, text="Start Attendance", command=self.start_attendance, font=("Arial", 14), bg="#3498db", fg="white", width=20, height=2)
        btn_attendance.grid(row=1, column=0, padx=20, pady=20)

        btn_view = tk.Button(main_frame, text="View Attendance", command=self.view_attendance, font=("Arial", 14), bg="#9b59b6", fg="white", width=20, height=2)
        btn_view.grid(row=1, column=1, padx=20, pady=20)

        btn_exit = tk.Button(main_frame, text="Exit", command=root.quit, font=("Arial", 14), bg="#e74c3c", fg="white", width=20, height=2)
        btn_exit.grid(row=2, column=1, padx=20, pady=20)

        btn_settings = tk.Button(main_frame, text="Camera Settings", command=self.open_settings_window, font=("Arial", 14), bg="#7f8c8d", fg="white", width=20, height=2)
        btn_settings.grid(row=2, column=0, padx=20, pady=20)

    def open_settings_window(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Camera Settings")
        settings_window.geometry("400x200")
        
        tk.Label(settings_window, text="Camera Source (0, 1, or URL):", font=("Arial", 12)).pack(pady=10)
        
        current_source = get_camera_source()
        source_entry = tk.Entry(settings_window, font=("Arial", 12), width=30)
        source_entry.insert(0, str(current_source))
        source_entry.pack(pady=5)
        
        def save_config():
            src = source_entry.get()
            # If digit, save as int, else string
            if src.isdigit():
                save_camera_source(src) # save as is, utils handles conversion on read? No, utils reads string. 
                # Let's check utils.py again. 
                # "if source.isdigit(): return int(source)". So saving as string "0" is fine.
                pass
            save_camera_source(src)
            messagebox.showinfo("Success", "Camera Source Saved!")
            settings_window.destroy()
            
        tk.Button(settings_window, text="Save", command=save_config, bg="#3498db", fg="white", font=("Arial", 12)).pack(pady=20)


    def open_register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register Student")
        register_window.geometry("400x300")
        
        tk.Label(register_window, text="Roll Number:", font=("Arial", 12)).pack(pady=10)
        roll_entry = tk.Entry(register_window, font=("Arial", 12))
        roll_entry.pack(pady=5)
        
        tk.Label(register_window, text="Name:", font=("Arial", 12)).pack(pady=10)
        name_entry = tk.Entry(register_window, font=("Arial", 12))
        name_entry.pack(pady=5)
        
        def capture():
            roll = roll_entry.get()
            name = name_entry.get()
            if not roll or not name:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            register_window.destroy()  # Close the small window
            # Call capture function
            try:
                register_student.capture_images(roll, name)
                messagebox.showinfo("Success", "Images Captured! Now Click 'Train Face Encodings'.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(register_window, text="Capture Faces", command=capture, bg="#2ecc71", fg="white", font=("Arial", 12)).pack(pady=20)

    def train_data(self):
        try:
            train_faces.train_faces()
            messagebox.showinfo("Success", "Training Completed! Encodings saved.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_attendance(self):
        try:
            messagebox.showinfo("Info", "Starting Camera... Press 'q' to stop.")
            recognize_attendance.recognize_faces()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_attendance(self):
        file_path = get_attendance_file_path()
        if not os.path.exists(file_path):
            messagebox.showwarning("Warning", "No attendance file found for today.")
            return

        view_window = tk.Toplevel(self.root)
        view_window.title(f"Attendance - {os.path.basename(file_path)}")
        view_window.geometry("600x400")

        # Treeview
        tree = ttk.Treeview(view_window)
        tree["columns"] = ("Roll", "Name", "Date", "Time")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Roll", anchor=tk.W, width=100)
        tree.column("Name", anchor=tk.W, width=150)
        tree.column("Date", anchor=tk.W, width=100)
        tree.column("Time", anchor=tk.W, width=100)
        
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Roll", text="Roll Number", anchor=tk.W)
        tree.heading("Name", text="Name", anchor=tk.W)
        tree.heading("Date", text="Date", anchor=tk.W)
        tree.heading("Time", text="Time", anchor=tk.W)
        
        tree.pack(fill=tk.BOTH, expand=True)

        # Load CSV data
        try:
            df = pd.read_csv(file_path)
            for index, row in df.iterrows():
                tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))
        except Exception as e:
            messagebox.showerror("Error", f"Could not read CSV: {e}")

        # Export Button
        def export_excel():
            try:
                excel_path = file_path.replace(".csv", ".xlsx")
                df.to_excel(excel_path, index=False)
                messagebox.showinfo("Success", f"Exported to {excel_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(view_window, text="Export to Excel", command=export_excel, bg="#9b59b6", fg="white").pack(pady=10)

def main():
    root = tk.Tk()
    app = FaceAttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
