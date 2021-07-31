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
MODEL_TYPE_LIST=("SimpleCNN" "DeepCNN")
DATA_AUG_LIST=("5,0.2,0.2,0.2,0.2,True")
DATA_AUG_NAME_LIST=("DA5")
	# DAn: rotation_range,width_shift_range,height_shift_range,zoom_range,channel_shift_range,horizontal_flip
	# DA-OFF: 0,0,0,0.0,0.0,False
	# DA0: 10,0.2,0.2,0.0,0.0,True
	# DA1: 5,0.2,0.2,0.0,0.0,True
	# DA2: 3,0.2,0.2,0.0,0.0,True
	# DA3: 3,0.1,0.1,0.0,0.0,True
	# DA4: 3,0.1,0.1,0.1,0.1,True
	# DA5: 5,0.2,0.2,0.2,0.2,True
	# DA6: 5,0.2,0.2,0.2,0.0,True
	# DA7: 5,0.2,0.2,0.0,0.2,True
OPTIMIZER_LIST=("adam" "momentum")
BATCH_SIZE_LIST=("50" "200")
INITIALIZER_LIST=("he_normal")
DATA_NORM_LIST=("z-score")
DROPOUT_RATE_LIST=("0.25")
LOSS_FUNC_LIST=("binary_crossentropy")
EPOCHS_LIST=("400")

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
							for DATA_NORM in ${DATA_NORM_LIST[@]}
							do
								for DROPOUT_RATE in ${DROPOUT_RATE_LIST[@]}
								do
									for LOSS_FUNC in ${LOSS_FUNC_LIST[@]}
									do
										for EPOCHS in ${EPOCHS_LIST[@]}
										do
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
											mkdir -p ${model_dir}
											
											python3 main.py --data_type ${DATA_TYPE} \
												--dataset_dir ${dataset_dir} \
												--model_type ${MODEL_TYPE} \
												--data_augmentation ${DATA_AUG} \
												--optimizer ${OPTIMIZER} \
												--batch_size ${BATCH_SIZE} \
												--initializer ${INITIALIZER} \
												--dropout_rate ${DROPOUT_RATE} \
												--loss_func ${LOSS_FUNC} \
												--epochs ${EPOCHS} \
												--result_dir ${model_dir}
										done
									done
								done
							done
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
"${OUTPUT_DIR}/model/${SimpleCNN_CIFAR10_DA5_OPTmomentum_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleCNN_CIFAR10_DA5_OPTmomentum_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleCNN_CIFAR10_DA5_OPTadam_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${SimpleCNN_CIFAR10_DA5_OPTadam_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${DeepCNN_CIFAR10_DA5_OPTmomentum_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${DeepCNN_CIFAR10_DA5_OPTmomentum_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${DeepCNN_CIFAR10_DA5_OPTadam_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${DeepCNN_CIFAR10_DA5_OPTadam_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv"
metrics_names=\
"${SimpleCNN_CIFAR10_DA5_OPTmomentum_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400},"\
"${SimpleCNN_CIFAR10_DA5_OPTmomentum_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400},"\
"${SimpleCNN_CIFAR10_DA5_OPTadam_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400},"\
"${SimpleCNN_CIFAR10_DA5_OPTadam_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400},"\
"${DeepCNN_CIFAR10_DA5_OPTmomentum_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400},"\
"${DeepCNN_CIFAR10_DA5_OPTmomentum_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400},"\
"${DeepCNN_CIFAR10_DA5_OPTadam_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400},"\
"${DeepCNN_CIFAR10_DA5_OPTadam_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}"
output_dir="${OUTPUT_DIR}/metrics_graph"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --fig_size ${fig_size} --output_dir ${output_dir}


# --- Compare models(Deep, momentum) ---
metrics_list=\
"${OUTPUT_DIR}/model/${DeepCNN_CIFAR10_DA5_OPTmomentum_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv,"\
"${OUTPUT_DIR}/model/${DeepCNN_CIFAR10_DA5_OPTmomentum_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}/metrics/metrics.csv"
metrics_names=\
"${DeepCNN_CIFAR10_DA5_OPTmomentum_batch50_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400},"\
"${DeepCNN_CIFAR10_DA5_OPTmomentum_batch200_he_normal_DNzscore_DROPOUT025_binary_crossentropy_epochs400}"
output_dir="${OUTPUT_DIR}/metrics_graph-deep_momentum"

python3 tools/create_metrics_graph/create_metrics_graph.py --metrics_list ${metrics_list} --metrics_names ${metrics_names} --fig_size ${fig_size} --output_dir ${output_dir}



