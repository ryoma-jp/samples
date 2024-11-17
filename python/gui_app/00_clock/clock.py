"""
Simple clock application with miliseconds using tkinter
"""
import tkinter as tk
import datetime
import pytz

def main():
    root = tk.Tk()
    root.title("Clock")
    label = tk.Label(root, font=("Arial", 80), bg="white")
    label.pack(expand=True)
    update_clock(label)
    root.mainloop()

def update_clock(label):
    # Get current time with miliseconds
    now = datetime.datetime.now(pytz.utc)
    jst = pytz.timezone('Asia/Tokyo')
    now = now.astimezone(jst)
    current_time = now.strftime("%H:%M:%S.%f")[:-3]
    label.config(text=current_time)
    label.after(1, lambda: update_clock(label))
    
if __name__ == "__main__":
    main()

    