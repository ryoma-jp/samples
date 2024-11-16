#! /bin/bash

DOCKER_IMAGE="python_gui_app:latest"

docker run -it --rm \
    -v `pwd`:`pwd` \
    -w `pwd` \
    -u `id -u`:`id -g` \
    -e DISPLAY=$DISPLAY \
    $DOCKER_IMAGE
