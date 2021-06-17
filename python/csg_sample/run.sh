#! /bin/bash

if [ ! -e spectral_metric ]; then
	git clone https://github.com/Dref360/spectral_metric.git
	cd spectral_metric
	patch -p1 < ../spectral_metric.patch
else
	cd spectral_metric
fi

export DATASET_ROOT=$PWD
if [ ! -e "${DATASET_ROOT}/Datasets" ]; then
	wget "https://onedrive.live.com/download?cid=AB307638A9FB0EF9&resid=AB307638A9FB0EF9%21368&authkey=AC9YsfqB8u8f-nA" -O dataset.zip
	unzip dataset.zip
fi

python3 ./main.py mnist cifar10 --embd cnn_embd --tsne --make_graph

