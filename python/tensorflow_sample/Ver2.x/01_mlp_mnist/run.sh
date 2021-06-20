#! /bin/bash

export DATA_TYPE="MNIST"		# "MNIST"
DATASET_DIR="./dataset"
LIB_DIR="/work/lib"

mkdir -p ${DATASET_DIR}

if [ ${DATA_TYPE} = "MNIST" ]; then
	dataset_dir="${DATASET_DIR}/mnist"
	if [ ! -e ${dataset_dir} ]; then
		mkdir -p ${dataset_dir}
		cd ${dataset_dir}
		wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz &
		wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz &
		wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz &
		wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
		wait
		gunzip train-images-idx3-ubyte.gz &
		gunzip train-labels-idx1-ubyte.gz &
		gunzip t10k-images-idx3-ubyte.gz &
		gunzip t10k-labels-idx1-ubyte.gz &
		wait
		cd ../..
	fi
else
	echo "Unknown DATA_TYPE: ${DATA_TYPE}"
	exit
fi

echo `pwd`
python3 main.py --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir}
