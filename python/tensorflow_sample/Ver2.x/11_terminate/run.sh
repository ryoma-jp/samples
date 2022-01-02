#! /bin/bash

# --- Fixed parameters ---
DATASET_DIR="./dataset"
LIB_DIR="/work/lib"
mkdir -p ${DATASET_DIR}

# --- Trainer control ---
FIFO="/tmp/fifo_trainer_ctl"
if [ ! -e ${FIFO} ]; then
	mkfifo ${FIFO}
fi

# --- Prepare dataset ---
#  * MNIST
#  * CIFAR-10
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

dataset_dir="${DATASET_DIR}/cifar-10-batches-py"
if [ ! -e ${DATASET_DIR}/cifar-10-python.tar.gz ]; then
	cd ${DATASET_DIR}
	wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
	tar -zxf cifar-10-python.tar.gz
	cd ..
fi

# --- Training ---
echo `pwd`
OUTPUT_DIR="./output_cifar10"
DATA_TYPE="CIFAR-10"
MODEL_TYPE="SimpleCNN"
DATA_AUG="5,0.2,0.2,0.2,0.2,True"
DATA_AUG_NAME="DA-5"
OPTIMIZER="momentum"
BATCH_SIZE="100"
INITIALIZER="he_normal"
DATA_NORM="max"
DROPOUT_RATE="0.25"
LOSS_FUNC="categorical_crossentropy"
EPOCHS="400"

RESUME="False"
if [ ! -e ${OUTPUT_DIR} ] || [ ${RESUME} = "True" ]; then
	echo "[Training Conditions]"
	echo "  * MODEL_TYPE=${MODEL_TYPE}"
	echo "  * DATA_TYPE=${DATA_TYPE}"
	echo "  * DATA_AUG=${DATA_AUG}"
	echo "  * DATA_AUG_NAME=${DATA_AUG_NAME}"
	echo "  * OPTIMIZER=${OPTIMIZER}"
	echo "  * BATCH_SIZE=${BATCH_SIZE}"
	echo "  * INITIALIZER=${INITIALIZER}"
	echo "  * DATA_NORM=${DATA_NORM}"
	echo "  * DROPOUT_RATE=${DROPOUT_RATE}"
	echo "  * LOSS_FUNC=${LOSS_FUNC}"
	echo "  * EPOCHS=${EPOCHS}"
	
	model_dir="${OUTPUT_DIR}/model/${MODEL_TYPE}_${DATA_TYPE}_${DATA_AUG_NAME}_OPT-${OPTIMIZER}_batch${BATCH_SIZE}_${INITIALIZER}_datanorm-${DATA_NORM}_dropout-${DROPOUT_RATE}_${LOSS_FUNC}_epochs${EPOCHS}"
	
	if [ ! -e ${model_dir} ]; then
		mkdir -p ${model_dir}
		python3 main.py --data_type ${DATA_TYPE} \
			--fifo ${FIFO} \
			--dataset_dir ${dataset_dir} \
			--model_type ${MODEL_TYPE} \
			--data_augmentation ${DATA_AUG} \
			--optimizer ${OPTIMIZER} \
			--batch_size ${BATCH_SIZE} \
			--initializer ${INITIALIZER} \
			--dropout_rate ${DROPOUT_RATE} \
			--loss_func ${LOSS_FUNC} \
			--epochs ${EPOCHS} \
			--result_dir ${model_dir} 2>&1 | tee ${model_dir}/training_log.txt
	else
		echo "[INFO] Training model is skipped: ${model_dir}"
	fi
fi

