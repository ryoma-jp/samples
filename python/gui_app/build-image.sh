#! /bin/bash

IMAGE_NAME="python_gui_app"
TAG="latest"
#DOCKERFILE="Dockerfile_for_UbuntuPC"
DOCKERFILE="Dockerfile_for_RasPi5"

docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .
