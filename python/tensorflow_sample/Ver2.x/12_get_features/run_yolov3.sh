#! /bin/bash

# --- get YOLOv3 ---
if [ ! -e ./external/yolov3 ]; then
    cd external
    git clone https://github.com/ryoma-jp/yolov3-tf2 yolov3
    cd ..
fi

# --- run yolov3 ---
python3 yolov3.py

