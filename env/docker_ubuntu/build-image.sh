#! /bin/bash

IMAGE_NAME="ubuntu"
TAG="latest"
DOCKERFILE="Dockerfile"

docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .
