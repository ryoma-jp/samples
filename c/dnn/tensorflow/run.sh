#! /bin/bash

DATASET_DIR="./dataset"
OUTPUT_DIR="./output"

if [ ! -e ${DATASET_DIR} ]; then
	mkdir -p ${DATASET_DIR}
	cd ${DATASET_DIR}
	wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
	tar -zxf cifar-10-python.tar.gz

fi

mkdir -p ${OUTPUT_DIR}
python3 main.py --dataset_dir ${DATASET_DIR}/cifar-10-batches-py/ --model_dir ${OUTPUT_DIR} 2>&1 | tee ${OUTPUT_DIR}/log.txt

