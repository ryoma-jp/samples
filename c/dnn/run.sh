#! /bin/bash

input_data='./tools/img2byte/output/train/abandoned_ship_s_000004.bin'
output_dir='./output'

mkdir -p ${output_dir}
./dnn_inference ${input_data} 2>&1 | tee ${output_dir}/log.txt


