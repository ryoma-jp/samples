#! /bin/bash

DATASET_TYPE="SARCOS"
OUTPUT_DIR="./output"

if [ ${DATASET_TYPE} = "Titanic" ]; then
	DATASET_DIR="./dataset/titanic"
elif [ ${DATASET_TYPE} = "SARCOS" ]; then
	TABNET_TYPE="TabNet-S"
	DATASET_DIR="./dataset/sarcos"
	if [ ! -e ${DATASET_DIR} ]; then
		mkdir -p ${DATASET_DIR}
		cd ${DATASET_DIR}
		wget http://www.gaussianprocess.org/gpml/data/sarcos_inv.mat
		wget http://www.gaussianprocess.org/gpml/data/sarcos_inv_test.mat
		cd ../..
	fi
fi

if [ "${TABNET_TYPE}x" = "x" ]; then
	# TABNET_TYPEが未定義の場合は引数に指定しない
	python3 main.py --dataset_type ${DATASET_TYPE} --dataset_dir ${DATASET_DIR} --output_dir ${OUTPUT_DIR}
else
	python3 main.py --dataset_type ${DATASET_TYPE} --dataset_dir ${DATASET_DIR} --output_dir ${OUTPUT_DIR} --tabnet_type ${TABNET_TYPE}
fi

