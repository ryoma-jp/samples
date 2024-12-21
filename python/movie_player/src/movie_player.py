import cv2
import argparse
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# Argument parsing
parser = argparse.ArgumentParser(description='Video file player')
parser.add_argument('--file_path', type=str, help='Path to the video file')
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
        
        # Frame for speed scale and label
        self.speed_frame = tk.Frame(root)
        self.speed_frame.pack(side=tk.LEFT)
        
        self.speed_label = ttk.Label(self.speed_frame, text="Speed: 1.0x")
        self.speed_label.pack()
        
        self.speed_scale = ttk.Scale(self.speed_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL, command=self.change_speed)
        self.speed_scale.set(1)
        self.speed_scale.pack()
        
        # Frame for position scale and label
        self.position_frame = tk.Frame(root)
        self.position_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.position_label = ttk.Label(self.position_frame, text="0 / 0 (0 fps)")
        self.position_label.pack()
        
        self.position_scale = ttk.Scale(self.position_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.change_position)
        self.position_scale.pack(fill=tk.X, expand=True)

        self.update_frame()

    def toggle_play(self):
        self.playing = not self.playing

    def change_speed(self, val):
        self.speed = float(val)
        self.speed_label.config(text=f"Speed: {self.speed:.1f}x")

    def change_position(self, val):
        epsilon = 1e-6
        frame_number = int(float(val) * self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / 100 + epsilon)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def update_frame(self):
        if self.playing:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                self.imgtk = ImageTk.PhotoImage(image=img)  # インスタンス変数として保持
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgtk)
                
                # Update the position of the progress bar and label
                current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.position_scale.set((current_frame / total_frames) * 100)
                self.position_label.config(text=f"{int(current_frame)} / {int(total_frames)} ({fps:.1f} fps)")
                
                self.root.after(int(1000 / (fps * self.speed)), self.update_frame)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.playing = False
        else:
            self.root.after(100, self.update_frame)
    
if __name__ == "__main__":
    root = tk.Tk()
    VideoPlayer(root, args.file_path)
    root.mainloop()
