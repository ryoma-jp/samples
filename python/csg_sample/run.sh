#! /bin/bash

git clone https://github.com/Dref360/spectral_metric.git
cd spectral_metric

wget "https://onedrive.live.com/download?cid=AB307638A9FB0EF9&resid=AB307638A9FB0EF9%21368&authkey=AC9YsfqB8u8f-nA" -O dataset.zip
unzip dataset.zip
DATASET_ROOT=$PWD

python3 ./main.py mnist cifar10 --embd cnn_embd --tsne --make_graph

