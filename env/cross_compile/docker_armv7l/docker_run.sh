#!/bin/bash

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="env_xc_armv7l/ubuntu:22.04"

docker run --rm -it -v "${WORK_ROOT}:/work" ${CONTAINER} /bin/bash


