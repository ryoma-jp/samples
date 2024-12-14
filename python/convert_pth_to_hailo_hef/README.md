# Convert PTH to Hailo HEF

This is a sample code to convert PyTorch's pre-trained model (.pth) to Hailo's executable format (.hef).

## Preparation

### Download `Hailo Dataflow Compiler` and `Hailo Model Zoo` from [Software Downloads](https://hailo.ai/developer-zone/software-downloads/)

Download `Hailo Dataflow Compiler` and `Hailo Model Zoo` from [Software Downloads](https://hailo.ai/developer-zone/software-downloads/) and save into `docker/compiler/whl/`.

### Build and Run Docker Container

```bash
./make_env.sh
docker compose up --build -d
```

### Convert PyTorch model to ONNX

```bash
docker compose exec converter bash
mkdir yolomodel && cd yolomodel
yolo detect train data=coco128.yaml model=yolov8n.pt name=retrain_yolov8n epochs=100 batch=16
cd ./runs/detect/retrain_yolov8n/weights/
yolo export model=./best.pt imgsz=640 format=onnx opset=11
```

### Convert ONNX model to Hailo HEF

```bash
```

## Reference

- [Tutorial of AI Kit with Raspberry Pi 5 about YOLOv8n object detection](https://wiki.seeedstudio.com/tutorial_of_ai_kit_with_raspberrypi5_about_yolov8n_object_detection/)
