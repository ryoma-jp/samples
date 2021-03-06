#! /bin/bash

# --- Fixed parameters ---
DATASET_DIR="./dataset"
LIB_DIR="/work/lib"
mkdir -p ${DATASET_DIR}

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
DATA_TYPE_LIST=("MNIST" "CIFAR-10")
MODEL_TYPE_LIST=("MLP" "SimpleCNN" "SimpleResNet")

for DATA_TYPE in ${DATA_TYPE_LIST[@]}
do
	if [ ${DATA_TYPE} = "MNIST" ]; then
		dataset_dir="${DATASET_DIR}/mnist"
	elif [ ${DATA_TYPE} = "CIFAR-10" ]; then
		dataset_dir="${DATASET_DIR}/cifar-10-batches-py"
	else
		echo "[ERROR] Unknown DATA_TYPE; ${DATA_TYPE}"
		exit
	fi
	
	for MODEL_TYPE in ${MODEL_TYPE_LIST[@]}
	do
		echo "[Training Conditions] MODEL_TYPE=${MODEL_TYPE}, DATA_TYPE=${DATA_TYPE}"
		result_dir="result_${MODEL_TYPE}_${DATA_TYPE}"
		mkdir -p ${result_dir}
		python3 main.py --data_type ${DATA_TYPE} \
			--dataset_dir ${dataset_dir} \
			--model_type ${MODEL_TYPE} \
			--result_dir ${result_dir}
		#python3 -m pdb main.py --data_type ${DATA_TYPE} \
		#	--dataset_dir ${dataset_dir} \
		#	--model_type ${MODEL_TYPE} \
		#	--result_dir ${result_dir}
	done
done

# --- Compare models ---
metrics_list="./result_MLP_CIFAR-10/metrics/metrics.csv,"\
"./result_MLP_MNIST/metrics/metrics.csv,"\
"./result_SimpleCNN_CIFAR-10/metrics/metrics.csv,"\
"./result_SimpleCNN_MNIST/metrics/metrics.csv,"\
"./result_SimpleResNet_CIFAR-10/metrics/metrics.csv,"\
"./result_SimpleResNet_MNIST/metrics/metrics.csv"
metrics_names="MLP_CIFAR-10,MLP_MNIST,SimpleCNN_CIFAR-10,SimpleCNN_MNIST,SimpleResNet_CIFAR-10,SimpleResNet_MNIST"
output_dir="./result/metrics_graph"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --output_dir ${output_dir}
#python3 -m pdb tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --output_dir ${output_dir}


