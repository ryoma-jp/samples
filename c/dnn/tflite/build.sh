#! /bin/bash

# --- Parameters ---
DEBUG="ON"		# ON or OFF

ROOT_DIR=${PWD}
TENSORFLOW_DIR='./tensorflow_src'
TFLITE_BUILD_DIR='./tflite_build'
TFLITE_LIB_DIR=${TFLITE_BUILD_DIR}
APP_BUILD_DIR='./inference_sample_build'

# --- Build TensorFlow Lite ---
if [ ! -e ${TENSORFLOW_DIR} ]; then
	cd ${ROOT_DIR}
	git clone --recursive https://github.com/tensorflow/tensorflow.git ${TENSORFLOW_DIR}
	cd ${TENSORFLOW_DIR}
	git checkout 205bc8e204fd0fcdd837d93abea9eb1de107fe74
	cd ..
	if [ -e ${TFLITE_BUILD_DIR} ]; then
		rm -rf ${TFLITE_BUILD_DIR}
	fi
	mkdir ${TFLITE_BUILD_DIR}
	cd ${TFLITE_BUILD_DIR}
	cmake ../${TENSORFLOW_DIR}/tensorflow/lite
	cmake --build . -j
fi

# --- Build Application using TensorFlow Lite ---
cd ${ROOT_DIR}
mkdir ${APP_BUILD_DIR}
cd ${APP_BUILD_DIR}
cmake ../inference_sample
cmake --build . -j
