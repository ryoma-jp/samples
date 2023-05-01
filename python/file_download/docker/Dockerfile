
FROM ubuntu:23.04

RUN apt update && \
    apt install -y vim python3-pip
RUN pip3 install --break-system-packages \
    requests

ENTRYPOINT /bin/bash

