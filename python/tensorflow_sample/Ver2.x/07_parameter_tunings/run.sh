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
DATA_AUG_LIST=("True")
OPTIMIZER_LIST=("momentum" "adam")
BATCH_SIZE_LIST=("32" "64" "128")

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
					for BATCH_SIZE in ${BATCH_SIZE_LIST[@]}
					do
						echo "[Training Conditions]"
						echo "  * MODEL_TYPE=${MODEL_TYPE}"
						echo "  * DATA_TYPE=${DATA_TYPE}"
						echo "  * DATA_AUG=${DATA_AUG}"
						echo "  * OPTIMIZER=${OPTIMIZER}"
						echo "  * BATCH_SIZE=${BATCH_SIZE}"
						
						model_dir="${OUTPUT_DIR}/model/${MODEL_TYPE}_${DATA_TYPE}_DA-${DATA_AUG}_OPT-${OPTIMIZER}_batch${BATCH_SIZE}"
						mkdir -p ${model_dir}
						
						if [ ${DATA_AUG} = "True" ]; then
							python3 main.py --data_type ${DATA_TYPE} \
								--dataset_dir ${dataset_dir} \
								--model_type ${MODEL_TYPE} \
								--data_augmentation \
								--optimizer ${OPTIMIZER} \
								--batch_size ${BATCH_SIZE} \
								--result_dir ${model_dir}
						else
							python3 main.py --data_type ${DATA_TYPE} \
								--dataset_dir ${dataset_dir} \
								--model_type ${MODEL_TYPE} \
								--optimizer ${OPTIMIZER} \
								--batch_size ${BATCH_SIZE} \
								--result_dir ${model_dir}
						fi
					done
				done
			done
		done
	done
fi

# --- 出力するグラフのサイズ[inch] ---
fig_size="15,5"

# --- モデル定義 ---
source ./model.list

# --- Compare models(ALL) ---
metrics_list=\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DATrue}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DATrue_batch64}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DATrue_batch128}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DATrue_OPTmomentum}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DATrue_OPTmomentum_batch64}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DATrue_OPTmomentum_batch128}/metrics/metrics.csv"
metrics_names=\
"${SimpleResNet_CIFAR10_DATrue},"\
"${SimpleResNet_CIFAR10_DATrue_batch64},"\
"${SimpleResNet_CIFAR10_DATrue_batch128},"\
"${SimpleResNet_CIFAR10_DATrue_OPTmomentum},"\
"${SimpleResNet_CIFAR10_DATrue_OPTmomentum_batch64},"\
"${SimpleResNet_CIFAR10_DATrue_OPTmomentum_batch128}"
output_dir="${OUTPUT_DIR}/metrics_graph"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --fig_size ${fig_size} --output_dir ${output_dir}


