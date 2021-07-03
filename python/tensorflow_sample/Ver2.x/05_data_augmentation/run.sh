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
OUTPUT_DIR="./output"
DATA_TYPE_LIST=("MNIST" "CIFAR-10")
MODEL_TYPE_LIST=("MLP" "SimpleCNN" "SimpleResNet")
DATA_AUG_LIST=("True" "False")

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
		for DATA_AUG in ${DATA_AUG_LIST[@]}
		do
			echo "[Training Conditions]"
			echo "  * MODEL_TYPE=${MODEL_TYPE}"
			echo "  * DATA_TYPE=${DATA_TYPE}"
			echo "  * DATA_AUG=${DATA_AUG}"
			
			model_dir="${OUTPUT_DIR}/model/${MODEL_TYPE}_${DATA_TYPE}_DA-${DATA_AUG}"
			mkdir -p ${model_dir}
			
			if [ ${DATA_AUG} = "True" ]; then
				python3 main.py --data_type ${DATA_TYPE} \
					--dataset_dir ${dataset_dir} \
					--model_type ${MODEL_TYPE} \
					--data_augmentation \
					--result_dir ${model_dir}
			else
				python3 main.py --data_type ${DATA_TYPE} \
					--dataset_dir ${dataset_dir} \
					--model_type ${MODEL_TYPE} \
					--result_dir ${model_dir}
			fi
		done
	done
done

# --- Compare models(ALL) ---
metrics_list=\
"${OUTPUT_DIR}/model/MLP_CIFAR-10_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/MLP_CIFAR-10_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/MLP_MNIST_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/MLP_MNIST_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleCNN_CIFAR-10_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleCNN_CIFAR-10_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleCNN_MNIST_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleCNN_MNIST_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleResNet_CIFAR-10_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleResNet_CIFAR-10_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleResNet_MNIST_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleResNet_MNIST_DA-False/metrics/metrics.csv"
metrics_names=\
"MLP_CIFAR-10_DA-True,"\
"MLP_CIFAR-10_DA-False,"\
"MLP_MNIST_DA-True,"\
"MLP_MNIST_DA-False,"\
"SimpleCNN_CIFAR-10_DA-True,"\
"SimpleCNN_CIFAR-10_DA-False,"\
"SimpleCNN_MNIST_DA-True,"\
"SimpleCNN_MNIST_DA-False,"\
"SimpleResNet_CIFAR-10_DA-True,"\
"SimpleResNet_CIFAR-10_DA-False,"\
"SimpleResNet_MNIST_DA-True,"\
"SimpleResNet_MNIST_DA-False"
output_dir="${OUTPUT_DIR}/metrics_graph"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --output_dir ${output_dir}
#python3 -m pdb tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --output_dir ${output_dir}

# --- Compare models(MNIST) ---
metrics_list=\
"${OUTPUT_DIR}/model/MLP_MNIST_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/MLP_MNIST_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleCNN_MNIST_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleCNN_MNIST_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleResNet_MNIST_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleResNet_MNIST_DA-False/metrics/metrics.csv"
metrics_names=\
"MLP_MNIST_DA-True,"\
"MLP_MNIST_DA-False,"\
"SimpleCNN_MNIST_DA-True,"\
"SimpleCNN_MNIST_DA-False,"\
"SimpleResNet_MNIST_DA-True,"\
"SimpleResNet_MNIST_DA-False"
output_dir="${OUTPUT_DIR}/metrics_graph-mnist"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --output_dir ${output_dir}
#python3 -m pdb tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --output_dir ${output_dir}

# --- Compare models(CIFAR-10) ---
metrics_list=\
"${OUTPUT_DIR}/model/MLP_CIFAR-10_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/MLP_CIFAR-10_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleCNN_CIFAR-10_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleCNN_CIFAR-10_DA-False/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleResNet_CIFAR-10_DA-True/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/SimpleResNet_CIFAR-10_DA-False/metrics/metrics.csv"
metrics_names=\
"MLP_CIFAR-10_DA-True,"\
"MLP_CIFAR-10_DA-False,"\
"SimpleCNN_CIFAR-10_DA-True,"\
"SimpleCNN_CIFAR-10_DA-False,"\
"SimpleResNet_CIFAR-10_DA-True,"\
"SimpleResNet_CIFAR-10_DA-False"
output_dir="${OUTPUT_DIR}/metrics_graph-cifar10"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --output_dir ${output_dir}
#python3 -m pdb tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --output_dir ${output_dir}



