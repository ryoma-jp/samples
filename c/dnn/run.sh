#! /bin/bash

input_data='./tensorflow/output/tflite/input_data.bin'
output_dir='./output'

mkdir -p ${output_dir}
./dnn_inference ${input_data} 2>&1 | tee ${OUTPUT_DIR}/log.txt


