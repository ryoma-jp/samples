#! /bin/bash

#DATA_TYPE="CIFAR-10"		# "CIFAR-10", "BLOBS" or ...(T.B.D)
DATA_TYPE="BLOBS"		# "CIFAR-10", "BLOBS" or ...(T.B.D)
DATASET_DIR="./dataset"
OUTPUT_DIR="./output"

mkdir -p ${DATASET_DIR}

if [ ${DATA_TYPE} = "CIFAR-10" ]; then
	dataset_dir="${DATASET_DIR}/cifar-10-batches-py"
	if [ ! -e ${DATASET_DIR}/cifar-10-python.tar.gz ]; then
		cd ${DATASET_DIR}
		wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
		tar -zxf cifar-10-python.tar.gz
		cd ..
	fi
elif [ ${DATA_TYPE} = "BLOBS" ]; then
	# BLOBS指定時はmain.py内でデータを生成する
	dataset_dir="dummy"
else
	echo "Unknown DATA_TYPE: ${DATA_TYPE}"
	exit
fi

python3 main.py --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir} --output_dir ${OUTPUT_DIR}
