#!/bin/bash

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="ubuntu_22.10/python:latest"

docker run --rm -it \
	-v "${WORK_ROOT}:/work" \
	${CONTAINER}


