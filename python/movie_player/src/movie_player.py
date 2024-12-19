import cv2
import argparse
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# Argument parsing
parser = argparse.ArgumentParser(description='Video file player')
parser.add_argument('file_path', type=str, help='Path to the video file')
args = parser.parse_args()

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("Video Player")
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.playing = False
        self.speed = 1

        # Create UI elements
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.play_button = ttk.Button(root, text="Play/Pause", command=self.toggle_play)
        self.play_button.pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(root, from_=0.5, to=2.0, orient=tk.HORIZONTAL, command=self.change_speed)
        self.speed_scale.set(1)
        self.speed_scale.pack(side=tk.LEFT)
        self.position_scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.change_position)
        self.position_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.update_frame()

    def toggle_play(self):
        self.playing = not self.playing

    def change_speed(self, val):
        self.speed = float(val)

    def change_position(self, val):
        frame_number = int(float(val) * self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / 100)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def update_frame(self):
        if self.playing:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)
                self.canvas.image = frame
                self.position_scale.set(self.cap.get(cv2.CAP_PROP_POS_FRAMES) / self.cap.get(cv2.CAP_PROP_FRAME_COUNT) * 100)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.root.after(int(1000 / (self.cap.get(cv2.CAP_PROP_FPS) * self.speed)), self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    VideoPlayer(root, args.file_path)
    root.mainloop()
