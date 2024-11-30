#! /bin/bash

MODEL_DIR="/tmp/models/"
mkdir -p $MODEL_DIR

MODEL="yolox_l_leaky.hef"
if [ -f $MODEL_DIR$MODEL ]; then
    echo "$MODEL_DIR$MODEL exists."
else
    wget https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/ModelZoo/Compiled/v2.13.0/hailo8l/yolox_l_leaky.hef -P $MODEL_DIR
fi

#python3 02_inference-camera-image/inference-camera-image.py --hef /usr/share/hailo-models/yolox_s_leaky_h8l_rpi.hef
python3 02_inference-camera-image/inference-camera-image.py --hef $MODEL_DIR$MODEL
