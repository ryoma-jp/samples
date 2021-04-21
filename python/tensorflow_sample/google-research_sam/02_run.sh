#! /bin/bash

mkdir -p output
#XLA_FLAGS=--xla_gpu_cuda_data_dir=/usr/local/cuda/ \
#	python3 -m sam.sam_jax.train --dataset cifar10 --model_name WideResnet28x10 \
#	--output_dir ./output --image_level_augmentations autoaugment \
#	--num_epochs 1800 --sam_rho 0.05

XLA_FLAGS=--xla_gpu_cuda_data_dir=/usr/local/cuda/ \
	python3 -m sam.sam_jax.train --dataset cifar10 --model_name WideResnet28x10 \
	--output_dir ./output --image_level_augmentations autoaugment \
	--num_epochs 180 --sam_rho 0.05 2>&1 | tee output/log.txt

#XLA_FLAGS=--xla_gpu_cuda_data_dir=/usr/lib/x86_64-linux-gnu/,--xla_dump_to=./tmp_dump \
#	python3 -m sam.sam_jax.train --dataset cifar10 --model_name WideResnet28x10 \
#	--output_dir ./output --image_level_augmentations autoaugment \
#	--num_epochs 1800 --sam_rho 0.05

