# GUI App Samples

Sample code for GUI applications using Python.

## Preparation

BUild the docker image and run the container.

```
./build-image.sh
./enter-docker.sh
```

## [Clock](./00_clock)

A simple clock application.

```
python ./00_clock/clock.py
```

## [Camera Streraming](./01_camera_streaming)

A camera streaming application.

```
python ./01_camera_streaming/camera_streaming.py
```

### Trouble Shooting

1. _tkinter.TclError: couldn't connect to display

Type `xhost +`.

```
xhost +
./enter-docker.sh
```

## [Inference Camera Image](./02_inference-camera-image)

An application that performs inference on a camera image.

```
02_inference-camera-image/run.sh
```

### Supported Models

- Object Detection
    - yolov8n.hef
    - yolox_l_leaky.hef
    - yolox_s_leaky.hef
    - yolox_tiny.hef
- Semantic Segmentation
    - deeplab_v3_mobilenet_v2.hef
- Instance Segmentation
    - yolov8s_seg.hef
- T.B.D
    - YOLOX-Nano
