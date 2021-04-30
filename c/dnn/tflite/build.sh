#! /bin/bash

ROOT_DIR=${PWD}
TENSORFLOW_DIR='./tensorflow'
FLATBUFFERS_DIR='./flatbuffers'
TFLITE_LIB_DIR='./tensorflow/tensorflow/lite/tools/make/gen/linux_x86_64/lib'

if [ ! -e ${TENSORFLOW_DIR} ]; then
	cd ${ROOT_DIR}
	git clone --recursive https://github.com/tensorflow/tensorflow.git
	cd tensorflow/tensorflow/lite/tools/make
	./download_dependencies.sh
	./build_lib.sh
fi

if [ ! -e ${FLATBUFFERS_DIR} ]; then
	cd ${ROOT_DIR}
	git clone https://github.com/google/flatbuffers.git
fi

cd ${ROOT_DIR}
g++ main.cpp \
	-I${TENSORFLOW_DIR} \
	-I${FLATBUFFERS_DIR}/include \
	-L${TFLITE_LIB_DIR} \
	-ltensorflow-lite \
	-lpthread -ldl -lm \
	-o tflite_inference

