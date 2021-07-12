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
#  * OUTPUT_DIRで指定のトップディレクトリが存在する場合は学習しない
echo `pwd`
OUTPUT_DIR="./output"
DATA_TYPE_LIST=("CIFAR-10")
MODEL_TYPE_LIST=("SimpleResNet")
DATA_AUG_LIST=("False" "True")
OPTIMIZER_LIST=("momentum" "adam")

if [ ! -e ${OUTPUT_DIR} ]; then
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
				for OPTIMIZER in ${OPTIMIZER_LIST[@]}
				do
					echo "[Training Conditions]"
					echo "  * MODEL_TYPE=${MODEL_TYPE}"
					echo "  * DATA_TYPE=${DATA_TYPE}"
					echo "  * DATA_AUG=${DATA_AUG}"
					echo "  * OPTIMIZER=${OPTIMIZER}"
					
					model_dir="${OUTPUT_DIR}/model/${MODEL_TYPE}_${DATA_TYPE}_DA-${DATA_AUG}_OPT-${OPTIMIZER}"
					mkdir -p ${model_dir}
					
					if [ ${DATA_AUG} = "True" ]; then
						python3 main.py --data_type ${DATA_TYPE} \
							--dataset_dir ${dataset_dir} \
							--model_type ${MODEL_TYPE} \
							--data_augmentation \
							--optimizer ${OPTIMIZER} \
							--result_dir ${model_dir}
					else
						python3 main.py --data_type ${DATA_TYPE} \
							--dataset_dir ${dataset_dir} \
							--model_type ${MODEL_TYPE} \
							--optimizer ${OPTIMIZER} \
							--result_dir ${model_dir}
					fi
				done
			done
		done
	done
fi

# --- 出力するグラフのサイズ[inch] ---
fig_size="15,5"

# --- モデル定義 ---
MLP_CIFAR10_DATrue="MLP_CIFAR-10_DA-True_OPT-adam"
MLP_CIFAR10_DAFalse="MLP_CIFAR-10_DA-False_OPT-adam"
MLP_MNIST_DATrue="MLP_MNIST_DA-True_OPT-adam"
MLP_MNIST_DAFalse="MLP_MNIST_DA-False_OPT-adam"
SimpleCNN_CIFAR10_DATrue="SimpleCNN_CIFAR-10_DA-True_OPT-adam"
SimpleCNN_CIFAR10_DAFalse="SimpleCNN_CIFAR-10_DA-False_OPT-adam"
SimpleCNN_MNIST_DATrue="SimpleCNN_MNIST_DA-True_OPT-adam"
SimpleCNN_MNIST_DAFalse="SimpleCNN_MNIST_DA-False_OPT-adam"
SimpleResNet_CIFAR10_DATrue="SimpleResNet_CIFAR-10_DA-True_OPT-adam"
SimpleResNet_CIFAR10_DAFalse="SimpleResNet_CIFAR-10_DA-False_OPT-adam"
SimpleResNet_MNIST_DATrue="SimpleResNet_MNIST_DA-True_OPT-adam"
SimpleResNet_MNIST_DAFalse="SimpleResNet_MNIST_DA-False_OPT-adam"

MLP_CIFAR10_DATrue_OPTsgd="MLP_CIFAR-10_DA-True_OPT-sgd"
MLP_CIFAR10_DAFalse_OPTsgd="MLP_CIFAR-10_DA-False_OPT-sgd"
MLP_MNIST_DATrue_OPTsgd="MLP_MNIST_DA-True_OPT-sgd"
MLP_MNIST_DAFalse_OPTsgd="MLP_MNIST_DA-False_OPT-sgd"
SimpleCNN_CIFAR10_DATrue_OPTsgd="SimpleCNN_CIFAR-10_DA-True_OPT-sgd"
SimpleCNN_CIFAR10_DAFalse_OPTsgd="SimpleCNN_CIFAR-10_DA-False_OPT-sgd"
SimpleCNN_MNIST_DATrue_OPTsgd="SimpleCNN_MNIST_DA-True_OPT-sgd"
SimpleCNN_MNIST_DAFalse_OPTsgd="SimpleCNN_MNIST_DA-False_OPT-sgd"
SimpleResNet_CIFAR10_DATrue_OPTsgd="SimpleResNet_CIFAR-10_DA-True_OPT-sgd"
SimpleResNet_CIFAR10_DAFalse_OPTsgd="SimpleResNet_CIFAR-10_DA-False_OPT-sgd"
SimpleResNet_MNIST_DATrue_OPTsgd="SimpleResNet_MNIST_DA-True_OPT-sgd"
SimpleResNet_MNIST_DAFalse_OPTsgd="SimpleResNet_MNIST_DA-False_OPT-sgd"

MLP_CIFAR10_DATrue_OPTadamlrs="MLP_CIFAR-10_DA-True_OPT-adam_lrs"
MLP_CIFAR10_DAFalse_OPTadamlrs="MLP_CIFAR-10_DA-False_OPT-adam_lrs"
MLP_MNIST_DATrue_OPTadamlrs="MLP_MNIST_DA-True_OPT-adam_lrs"
MLP_MNIST_DAFalse_OPTadamlrs="MLP_MNIST_DA-False_OPT-adam_lrs"
SimpleCNN_CIFAR10_DATrue_OPTadamlrs="SimpleCNN_CIFAR-10_DA-True_OPT-adam_lrs"
SimpleCNN_CIFAR10_DAFalse_OPTadamlrs="SimpleCNN_CIFAR-10_DA-False_OPT-adam_lrs"
SimpleCNN_MNIST_DATrue_OPTadamlrs="SimpleCNN_MNIST_DA-True_OPT-adam_lrs"
SimpleCNN_MNIST_DAFalse_OPTadamlrs="SimpleCNN_MNIST_DA-False_OPT-adam_lrs"
SimpleResNet_CIFAR10_DATrue_OPTadamlrs="SimpleResNet_CIFAR-10_DA-True_OPT-adam_lrs"
SimpleResNet_CIFAR10_DAFalse_OPTadamlrs="SimpleResNet_CIFAR-10_DA-False_OPT-adam_lrs"
SimpleResNet_MNIST_DATrue_OPTadamlrs="SimpleResNet_MNIST_DA-True_OPT-adam_lrs"
SimpleResNet_MNIST_DAFalse_OPTadamlrs="SimpleResNet_MNIST_DA-False_OPT-adam_lrs"

MLP_CIFAR10_DATrue_OPTsgdlrs="MLP_CIFAR-10_DA-True_OPT-sgd_lrs"
MLP_CIFAR10_DAFalse_OPTsgdlrs="MLP_CIFAR-10_DA-False_OPT-sgd_lrs"
MLP_MNIST_DATrue_OPTsgdlrs="MLP_MNIST_DA-True_OPT-sgd_lrs"
MLP_MNIST_DAFalse_OPTsgdlrs="MLP_MNIST_DA-False_OPT-sgd_lrs"
SimpleCNN_CIFAR10_DATrue_OPTsgdlrs="SimpleCNN_CIFAR-10_DA-True_OPT-sgd_lrs"
SimpleCNN_CIFAR10_DAFalse_OPTsgdlrs="SimpleCNN_CIFAR-10_DA-False_OPT-sgd_lrs"
SimpleCNN_MNIST_DATrue_OPTsgdlrs="SimpleCNN_MNIST_DA-True_OPT-sgd_lrs"
SimpleCNN_MNIST_DAFalse_OPTsgdlrs="SimpleCNN_MNIST_DA-False_OPT-sgd_lrs"
SimpleResNet_CIFAR10_DATrue_OPTsgdlrs="SimpleResNet_CIFAR-10_DA-True_OPT-sgd_lrs"
SimpleResNet_CIFAR10_DAFalse_OPTsgdlrs="SimpleResNet_CIFAR-10_DA-False_OPT-sgd_lrs"
SimpleResNet_MNIST_DATrue_OPTsgdlrs="SimpleResNet_MNIST_DA-True_OPT-sgd_lrs"
SimpleResNet_MNIST_DAFalse_OPTsgdlrs="SimpleResNet_MNIST_DA-False_OPT-sgd_lrs"

SimpleResNet_CIFAR10_DATrue_OPTmomentum="SimpleResNet_CIFAR-10_DA-True_OPT-momentum"
SimpleResNet_CIFAR10_DAFalse_OPTmomentum="SimpleResNet_CIFAR-10_DA-False_OPT-momentum"

# --- Compare models(ALL) ---
metrics_list=\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DAFalse}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DAFalse_OPTmomentum}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DATrue}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DATrue_OPTmomentum}/metrics/metrics.csv"
metrics_names=\
"${SimpleResNet_CIFAR10_DAFalse},"\
"${SimpleResNet_CIFAR10_DAFalse_OPTmomentum},"\
"${SimpleResNet_CIFAR10_DATrue},"\
"${SimpleResNet_CIFAR10_DATrue_OPTmomentum}"
output_dir="${OUTPUT_DIR}/metrics_graph"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --fig_size ${fig_size} --output_dir ${output_dir}


