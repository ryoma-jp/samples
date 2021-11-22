#!/bin/bash

WORK_ROOT="${PWD}/.."
echo ${WORK_ROOT}

CONTAINER="arm_neon_intrinsic/ubuntu:22.04"

docker run --rm -it -v "${WORK_ROOT}:/work" ${CONTAINER} /bin/bash


