#! /bin/bash

export DATA_TYPE="CIFAR-10"		# "MNIST" or "CIFAR-10"
DATASET_DIR="./dataset"
MODEL_TYPE="ResNet"
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
elif [ ${DATA_TYPE} = "CIFAR-10" ]; then
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

echo `pwd`
python3 main.py --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir} --model_type ${MODEL_TYPE}
#python3 -m pdb main.py --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir} --model_type ${MODEL_TYPE}
