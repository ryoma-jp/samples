#! /bin/bash

export DATA_TYPE="CIFAR-10"		# "CIFAR-10", "Titanic", "SARCOS", "COCO2014", "MoviePoster", "MNIST" or ...(T.B.D)
DATASET_DIR="./dataset"
LIB_DIR="/work/lib"

mkdir -p ${DATASET_DIR}

if [ ${DATA_TYPE} = "CIFAR-10" ]; then
	dataset_dir="${DATASET_DIR}/cifar-10-batches-py"
	if [ ! -e ${DATASET_DIR}/cifar-10-python.tar.gz ]; then
		cd ${DATASET_DIR}
		wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
		tar -zxf cifar-10-python.tar.gz
		cd ..
	fi
elif [ ${DATA_TYPE} = "Titanic" ]; then
	dataset_dir="${DATASET_DIR}/titanic"
elif [ ${DATA_TYPE} = "SARCOS" ]; then
	dataset_dir="${DATASET_DIR}/sarcos"
	if [ ! -e ${dataset_dir} ]; then
		mkdir -p ${dataset_dir}
		cd ${dataset_dir}
		wget http://www.gaussianprocess.org/gpml/data/sarcos_inv.mat
		wget http://www.gaussianprocess.org/gpml/data/sarcos_inv_test.mat
		cd ../..
	fi
elif [ ${DATA_TYPE} = "COCO2014" ]; then
	dataset_dir="${DATASET_DIR}/coco2014"
	if [ ! -e ${dataset_dir} ]; then
		mkdir -p ${dataset_dir}
		cd ${dataset_dir}
		wget http://images.cocodataset.org/zips/train2014.zip &
		wget http://images.cocodataset.org/zips/val2014.zip &
		wget http://images.cocodataset.org/zips/test2014.zip &
		wget http://images.cocodataset.org/annotations/annotations_trainval2014.zip
		wait
		unzip train2014.zip &
		unzip val2014.zip &
		unzip test2014.zip &
		unzip annotations_trainval2014.zip
		wait
		cd ../..
	fi
	
	# --- pycocoapiのビルド ---
	if [ ! -e ${LIB_DIR}/cocoapi ]; then
		mkdir -p ${LIB_DIR}
		cd ${LIB_DIR}
		git clone https://github.com/cocodataset/cocoapi.git
		cd cocoapi/PythonAPI
		make
		cd ../../../
	fi
	export PYTHONPATH=${PYTHONPATH}:${LIB_DIR}/cocoapi/PythonAPI
	
elif [ ${DATA_TYPE} = "MoviePoster" ]; then
	#------------------------------------------------
	# Genreを分類するものとして読み込む
	#------------------------------------------------
	dataset_dir="${DATASET_DIR}/movie_poster"
	if [ ! -e ${dataset_dir} ]; then
		mkdir -p ${dataset_dir}
		cd ${dataset_dir}
		wget https://www.cs.ccu.edu.tw/~wtchu/projects/MoviePoster/Movie_Poster_Dataset.zip &
		wget https://www.cs.ccu.edu.tw/~wtchu/projects/MoviePoster/Movie_Poster_Metadata.zip
		wait
		unzip Movie_Poster_Dataset.zip &
		unzip Movie_Poster_Metadata.zip
		wait
		cd ../..
	fi
elif [ ${DATA_TYPE} = "MNIST" ]; then
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
		cd ..
	fi
else
	echo "Unknown DATA_TYPE: ${DATA_TYPE}"
	exit
fi

echo `pwd`
python3 main.py --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir}
