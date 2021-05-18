#! /bin/bash

DATA_TYPE="CIFAR-10"		# "CIFAR-10", "Titanic", "SARCOS", or ...(T.B.D)
DATASET_DIR="./dataset"

mkdir -p ${DATASET_DIR}

if [ ${DATA_TYPE} = "CIFAR-10" ]; then
	dataset_dir="${DATASET_DIR}/cifar-10-batches-py"
	if [ ! -e ${DATASET_DIR}/cifar-10-python.tar.gz ]; then
		cd ${DATASET_DIR}
		wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
		tar -zxf cifar-10-python.tar.gz
		cd ..
	fi
elif [ ${DATA_TYPE} = "Titanic" ]; then
	dataset_dir="${DATASET_DIR}/titanic"
elif [ ${DATA_TYPE} = "SARCOS" ]; then
	dataset_dir="${DATASET_DIR}/sarcos"
	if [ ! -e ${DATASET_DIR}/sarcos ]; then
		mkdir -p ${DATASET_DIR}/sarcos
		cd ${DATASET_DIR}/sarcos
		wget http://www.gaussianprocess.org/gpml/data/sarcos_inv.mat
		wget http://www.gaussianprocess.org/gpml/data/sarcos_inv_test.mat
		cd ../..
	fi
else
	echo "Unknown DATA_TYPE: ${DATA_TYPE}"
	exit
fi

python3 main.py --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir}
