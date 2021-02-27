#! /bin/bash

CONTAINER="node-web-app/sample:node_12"
docker run -it --rm -p 127.0.0.1:8080:8080 ${CONTAINER}

