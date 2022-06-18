#!/bin/bash

# --- ref ---
#   https://docs.nvidia.com/cuda/wsl-user-guide/index.html

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="jupyter_nb/tensorflow_gpu:latest"

docker run --gpus all --rm -it --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	-v "${WORK_ROOT}/work:/tf/work" \
	-v "${WORK_ROOT}/data:/tf/data" \
	-p 35000:8888 ${CONTAINER}


