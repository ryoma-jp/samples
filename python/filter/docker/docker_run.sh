#!/bin/bash

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="filter_sample/scipy-notebook:latest"

docker run -v "${WORK_ROOT}:/home/jovyan/work" -p 10000:8888 ${CONTAINER}


