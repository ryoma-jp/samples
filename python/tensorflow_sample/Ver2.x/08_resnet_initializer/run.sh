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
DATA_AUG_LIST=("3,0.1,0.1,True")
DATA_AUG_NAME_LIST=("DA3")
	# DA0: 10,0.2,0.2,True
	# DA1: 5,0.2,0.2,True
	# DA2: 3,0.2,0.2,True
	# DA3: 3,0.1,0.1,True
OPTIMIZER_LIST=("momentum")
BATCH_SIZE_LIST=("32")
INITIALIZER_LIST=("glorot_normal" "glorot_uniform" "he_normal" "he_uniform")

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
			for _data_aug_idx in `seq ${#DATA_AUG_LIST[@]}`
			do
				data_aug_idx=`expr ${_data_aug_idx} - 1`
				DATA_AUG=${DATA_AUG_LIST[${data_aug_idx}]}
				DATA_AUG_NAME=${DATA_AUG_NAME_LIST[${data_aug_idx}]}
				
				for OPTIMIZER in ${OPTIMIZER_LIST[@]}
				do
					for BATCH_SIZE in ${BATCH_SIZE_LIST[@]}
					do
						for INITIALIZER in ${INITIALIZER_LIST[@]}
						do
							echo "[Training Conditions]"
							echo "  * MODEL_TYPE=${MODEL_TYPE}"
							echo "  * DATA_TYPE=${DATA_TYPE}"
							echo "  * DATA_AUG=${DATA_AUG}"
							echo "  * DATA_AUG_NAME=${DATA_AUG_NAME}"
							echo "  * OPTIMIZER=${OPTIMIZER}"
							echo "  * BATCH_SIZE=${BATCH_SIZE}"
							echo "  * INITIALIZER=${INITIALIZER}"
							
							model_dir="${OUTPUT_DIR}/model/${MODEL_TYPE}_${DATA_TYPE}_${DATA_AUG_NAME}_OPT-${OPTIMIZER}_batch${BATCH_SIZE}_${INITIALIZER}"
							mkdir -p ${model_dir}
							
							python3 main.py --data_type ${DATA_TYPE} \
								--dataset_dir ${dataset_dir} \
								--model_type ${MODEL_TYPE} \
								--data_augmentation ${DATA_AUG} \
								--optimizer ${OPTIMIZER} \
								--batch_size ${BATCH_SIZE} \
								--initializer ${INITIALIZER} \
								--result_dir ${model_dir}
						done
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
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DA3_OPTmomentum}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DA3_OPTmomentum_glorot_normal}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DA3_OPTmomentum_he_uniform}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleResNet_CIFAR10_DA3_OPTmomentum_he_normal}/metrics/metrics.csv"
metrics_names=\
"${SimpleResNet_CIFAR10_DA3_OPTmomentum},"\
"${SimpleResNet_CIFAR10_DA3_OPTmomentum_glorot_normal},"\
"${SimpleResNet_CIFAR10_DA3_OPTmomentum_he_uniform},"\
"${SimpleResNet_CIFAR10_DA3_OPTmomentum_he_normal}"
output_dir="${OUTPUT_DIR}/metrics_graph"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --fig_size ${fig_size} --output_dir ${output_dir}


