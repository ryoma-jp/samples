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
docker-compose exec compiler bash
cd yolomodel/runs/detect/retrain_yolov8n/weights
#git clone https://github.com/hailo-ai/hailo_model_zoo.git
ln -s /tmp/hailo_model_zoo
python3 hailo_model_zoo/hailo_model_zoo/datasets/create_coco_tfrecord.py val2017
python3 hailo_model_zoo/hailo_model_zoo/datasets/create_coco_tfrecord.py calib2017
#hailomz parse --hw-arch hailo8l --ckpt ./best.onnx yolov8n
/tmp/lib/hailo/bin/hailomz parse --hw-arch hailo8l --ckpt ./best.onnx yolov8n
#python3 hailo_model_zoo/hailo_model_zoo/main.py parse --hw-arch hailo8l --ckpt ./best.onnx yolov8n
ln -s ~/.hailomz/data/models_files/coco/2023-08-03/ ~/.hailomz/data/models_files/coco/2023-06-18
#hailomz optimize --hw-arch hailo8l --har ./yolov8n.har yolov8n
/tmp/lib/hailo/bin/hailomz optimize --hw-arch hailo8l --har ./yolov8n.har yolov8n
#python3 hailo_model_zoo/hailo_model_zoo/main.py optimize --hw-arch hailo8l --har ./yolov8n.har yolov8n
#hailomz compile  yolov8n --hw-arch hailo8l --har ./yolov8n.har 
/tmp/lib/hailo/bin/hailomz compile  yolov8n --hw-arch hailo8l --har ./yolov8n.har 
#python3 hailo_model_zoo/hailo_model_zoo/main.py compile  yolov8n --hw-arch hailo8l --har ./yolov8n.har
```

#### Issue

```
ryoichi@8e83775ddc26:/work/yolomodel/runs/detect/retrain_yolov8n/weights$ /tmp/lib/hailo/bin/hailomz compile  yolov8n --hw-arch hailo8l --har ./yolov8n.har 
[warning] Cannot use graphviz, so no visualizations will be created
<Hailo Model Zoo INFO> Start run for network yolov8n ...
<Hailo Model Zoo INFO> Initializing the hailo8l runner...
[info] Loading model script commands to yolov8n from /tmp/lib/hailo/hailo_model_zoo/cfg/alls/generic/yolov8n.alls
[info] To achieve optimal performance, set the compiler_optimization_level to "max" by adding performance_param(compiler_optimization_level=max) to the model script. Note that this may increase compilation time.
[error] Failed to produce compiled graph
[error] TypeError: expected str, bytes or os.PathLike object, not NoneType
```

## Reference

- [Tutorial of AI Kit with Raspberry Pi 5 about YOLOv8n object detection](https://wiki.seeedstudio.com/tutorial_of_ai_kit_with_raspberrypi5_about_yolov8n_object_detection/)
- [Error with Model Zoo compile/optimize](https://community.hailo.ai/t/error-with-model-zoo-compile-optimize/5959)
