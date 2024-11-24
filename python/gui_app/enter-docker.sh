#! /bin/bash

DOCKER_IMAGE="python_gui_app:latest"

MOUNT="-v `pwd`:`pwd` -v /run/udev:/run/udev:ro"
if [ -d "/tmp/.X11-unix" ]; then
    echo "/tmp/.X11-unix exists."
    MOUNT="$MOUNT -v /tmp/.X11-unix:/tmp/.X11-unix"
fi
if [ -d "/dev" ]; then
    echo "/dev exists."
    MOUNT="$MOUNT -v /dev:/dev"
fi

#docker run -it --rm --privileged \
#    $MOUNT \
#    -w `pwd` \
#    -u `id -u`:`id -g` \
#    -e DISPLAY=$DISPLAY \
#    $DOCKER_IMAGE

docker run -it --rm --privileged \
    $MOUNT \
    -w `pwd` \
    -e DISPLAY=$DISPLAY \
    $DOCKER_IMAGE
