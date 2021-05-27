#!/bin/bash

# --- ref ---
#   https://docs.nvidia.com/cuda/wsl-user-guide/index.html

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="resize_circle/tensorflow:21.03-tf2-py3"

docker run --gpus all --rm -it --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v "${WORK_ROOT}:/work" ${CONTAINER}


