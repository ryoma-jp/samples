#!/bin/bash

# --- ref ---
#   https://docs.nvidia.com/cuda/wsl-user-guide/index.html

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

USE_WSLg="YES"
CONTAINER="matplotlib_sample/tensorflow:21.03-tf2-py3"

if [ ${USE_WSLg} = "YES" ]; then
	docker run --gpus all --rm -it --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY -v "${WORK_ROOT}:/work" ${CONTAINER}
else
	docker run --gpus all --rm -it --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v "${WORK_ROOT}:/work" ${CONTAINER}
fi


