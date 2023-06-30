#!/bin/bash

# --- ref ---
#   https://docs.nvidia.com/cuda/wsl-user-guide/index.html

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="tf_sample_v2/tensorflow:ubuntu22.04"

docker run --gpus all --rm -it --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v "${WORK_ROOT}:/work" -p 6006:6006 ${CONTAINER}


