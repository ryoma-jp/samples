#! /bin/bash

INPUT_FILE="cifar10_images/train/abandoned_ship_s_000004.png"
OUTPUT_DIR="./output/train"
OUTPUT_FILE="${OUTPUT_DIR}/abandoned_ship_s_000004.bin"

mkdir -p ${OUTPUT_DIR}
python3 img2byte.py --input_img ${INPUT_FILE} --output_file ${OUTPUT_FILE}

