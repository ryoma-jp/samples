"""
Sample code to stream camera feed using OpenCV
"""
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from picamera2 import Picamera2

def main():
    camera = Picamera2()
    camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
    camera.start()
    
    root = tk.Tk()
    root.title("Camera Streaming")
    label = tk.Label(root)
    label.pack()
    
    update_camera(camera, label)
    root.mainloop()
    
def update_camera(camera, label):
    frame = camera.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(frame)
    label.config(image=frame)
    label.image = frame
    label.after(10, lambda: update_camera(camera, label))
    
if __name__ == "__main__":
    main()
