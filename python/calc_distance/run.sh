#! /bin/bash

DIST_TYPE="EUCLIDEAN"			# "EUCLIDEAN" or ...(T.B.D)
DATA_TYPE="CIFAR-10"		# "CIFAR-10" or ...(T.B.D)
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
else
	echo "Unknown DATA_TYPE: ${DATA_TYPE}"
	exit
fi

python3 main.py --dist_type ${DIST_TYPE} --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir}
