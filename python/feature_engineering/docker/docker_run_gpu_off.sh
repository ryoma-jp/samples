#!/bin/bash

# --- ref ---
#   https://docs.nvidia.com/cuda/wsl-user-guide/index.html

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="feature_engineering/scipy-notebook:latest"

docker run -v "${WORK_ROOT}:/home/jovyan/work" -p 10000:8888 ${CONTAINER}


