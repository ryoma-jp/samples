#! /bin/bash

DOCKER_IMAGE="ubuntu:latest"

docker run -it --rm \
    -v `pwd`:`pwd` \
    -w `pwd` \
    -u `id -u`:`id -g` \
    $DOCKER_IMAGE
