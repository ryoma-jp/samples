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

## Convert PTH to Hailo HEF

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
/tmp/lib/hailo/bin/hailomz compile --ckpt best.onnx --calib-path /home/ryoichi/.hailomz/data/coco/val2017/ --yaml /tmp/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8n.yaml
```

#### Issue

##### Failed to produce compiled graph
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

## Hailo Model Zoo

### [YOLOv8-seg](https://github.com/hailo-ai/hailo_model_zoo/blob/master/training/yolov8_seg/README.rst)

```bash
git clone https://github.com/hailo-ai/hailo_model_zoo.git
cd hailo_model_zoo/training/yolov8_seg
mkdir training_results
docker build --build-arg timezone=`cat /etc/timezone` -t yolov8_seg:v0 .
docker run --name "hailo_model_zoo" -it --gpus all --ipc=host -v ${HOME}/work/dataset:/dataset -v ${PWD}/training_results:/training_results yolov8_seg:v0
yolo segment train data=coco128-seg.yaml model=yolov8s-seg.pt name=retrain_yolov8s_seg epochs=100 batch=16
yolo export model=/workspace/ultralytics/runs/segment/retrain_yolov8s_seg/weights/best.pt imgsz=640 format=onnx opset=11
cp -a /workspace/ultralytics/runs/segment/retrain_yolov8s_seg/weights /training_results/
cd /path/to/convert_ptg_to_hailo_hef
cp -a /path/to/hailo_model_zoo/hailo_model_zoo/training/yolov8_seg/training_results/ ./yolov8_seg_training_results
docker compose up --build -d
docker compose exec compiler bash
hailomz compile --ckpt yolov8_seg_training_results/weights/best.onnx --calib-path /dataset/coco2017/val2017/ --yaml /tmp/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8s_seg.yaml
```

#### Issue

##### Failed to produce compiled graph

```
ryoichi@725dd283fefc:/work$ hailomz compile --ckpt yolov8_seg_training_results/weights/best.onnx --calib-path /dataset/coco2017/val2017/ --yaml /tmp/hailo_model_zoo/hailo_model_zoo/cfg/networks/yolov8s_seg.yaml
[warning] Cannot use graphviz, so no visualizations will be created
<Hailo Model Zoo INFO> Start run for network yolov8s_seg ...
<Hailo Model Zoo INFO> Initializing the hailo8 runner...
[info] Translation started on ONNX model yolov8s_seg
[info] Restored ONNX model yolov8s_seg (completion time: 00:00:00.73)
[info] Extracted ONNXRuntime meta-data for Hailo model (completion time: 00:00:01.52)
[info] Start nodes mapped from original model: 'images': 'yolov8s_seg/input_layer1'.
[info] End nodes mapped from original model: '/model.22/cv2.2/cv2.2.2/Conv', '/model.22/cv3.2/cv3.2.2/Conv', '/model.22/cv4.2/cv4.2.2/Conv', '/model.22/cv2.1/cv2.1.2/Conv', '/model.22/cv3.1/cv3.1.2/Conv', '/model.22/cv4.1/cv4.1.2/Conv', '/model.22/cv2.0/cv2.0.2/Conv', '/model.22/cv3.0/cv3.0.2/Conv', '/model.22/cv4.0/cv4.0.2/Conv', '/model.22/proto/cv3/act/Mul'.
[info] Translation completed on ONNX model yolov8s_seg (completion time: 00:00:02.66)
[info] Saved HAR to: /work/yolov8s_seg.har
<Hailo Model Zoo INFO> Preparing calibration data...
[info] Loading model script commands to yolov8s_seg from /tmp/lib/hailo/hailo_model_zoo/cfg/alls/generic/yolov8s_seg.alls
[info] Starting Model Optimization
[warning] Reducing optimization level to 0 (the accuracy won't be optimized and compression won't be used) because there's no available GPU
[warning] Running model optimization with zero level of optimization is not recommended for production use and might lead to suboptimal accuracy results
[info] Model received quantization params from the hn
[info] Starting Mixed Precision
[info] Mixed Precision is done (completion time is 00:00:00.67)
[info] LayerNorm Decomposition skipped
[info] Starting Statistics Collector
[info] Using dataset with 64 entries for calibration
Calibration: 100%|██████████████████████████████████████████████| 64/64 [00:53<00:00,  1.20entries/s]
[info] Statistics Collector is done (completion time is 00:00:55.22)
[info] Output layer yolov8s_seg/conv45 with sigmoid activation was detected. Forcing its output range to be [0, 1] (original range was [2.851756116102296e-16, 0.8801462650299072]).
[info] Output layer yolov8s_seg/conv61 with sigmoid activation was detected. Forcing its output range to be [0, 1] (original range was [4.5440000625936876e-18, 0.9473716020584106]).
[info] Output layer yolov8s_seg/conv74 with sigmoid activation was detected. Forcing its output range to be [0, 1] (original range was [2.007181576098283e-15, 0.9743812084197998]).
[info] Starting Fix zp_comp Encoding
[info] Fix zp_comp Encoding is done (completion time is 00:00:00.00)
[info] Matmul Equalization skipped
[info] Finetune encoding skipped
[info] Bias Correction skipped
[info] Adaround skipped
[info] Quantization-Aware Fine-Tuning skipped
[info] Layer Noise Analysis skipped
[info] Model Optimization is done
[info] Saved HAR to: /work/yolov8s_seg.har
[info] Loading model script commands to yolov8s_seg from /tmp/lib/hailo/hailo_model_zoo/cfg/alls/generic/yolov8s_seg.alls
[info] To achieve optimal performance, set the compiler_optimization_level to "max" by adding performance_param(compiler_optimization_level=max) to the model script. Note that this may increase compilation time.
[error] Failed to produce compiled graph
[error] TypeError: expected str, bytes or os.PathLike object, not NoneType
```

## Reference

- [Tutorial of AI Kit with Raspberry Pi 5 about YOLOv8n object detection](https://wiki.seeedstudio.com/tutorial_of_ai_kit_with_raspberrypi5_about_yolov8n_object_detection/)
- [Error with Model Zoo compile/optimize](https://community.hailo.ai/t/error-with-model-zoo-compile-optimize/5959)
