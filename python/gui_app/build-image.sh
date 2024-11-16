#! /bin/bash

IMAGE_NAME="python_gui_app"
TAG="latest"
DOCKERFILE="Dockerfile"

docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .
