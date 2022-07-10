#!/bin/bash

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="jupyter_nb/module_list:latest"

docker run --env-file env.list -v "${WORK_ROOT}:/home/jovyan/work" -p 10000:8888 ${CONTAINER}


