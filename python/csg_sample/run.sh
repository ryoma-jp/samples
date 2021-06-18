#! /bin/bash

if [ ! -e spectral_metric ]; then
	git clone https://github.com/Dref360/spectral_metric.git
	cd spectral_metric
	patch -p1 < ../spectral_metric.patch
else
	cd spectral_metric
fi

export DATASET_ROOT=$PWD
python3 ./main.py mnist cifar10 --embd cnn_embd --tsne --make_graph

