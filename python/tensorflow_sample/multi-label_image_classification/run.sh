#! /bin/bash

DATA_TYPE="MoviePoster"		# "MoviePoster", "MoviePoster_npz" or ...(T.B.D)
DATASET_DIR="./dataset"

mkdir -p ${DATASET_DIR}

if [ ${DATA_TYPE} = "MoviePoster" ]; then
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
	
	echo `pwd`
	python3 main.py --data_type ${DATA_TYPE} --dataset_dir ${dataset_dir}
	
elif [ ${DATA_TYPE} = "MoviePoster_npz" ]; then
	dataset_file="./output/movie_poster/dataset_movie_poster.npz"
	
	echo `pwd`
	python3 main.py --data_type ${DATA_TYPE} --dataset_file ${dataset_file}
else
	echo "Unknown DATA_TYPE: ${DATA_TYPE}"
	exit
fi

