
FROM ubuntu:23.04

RUN apt update && \
    apt install -y vim python3-pip
RUN pip3 install --break-system-packages \
    requests==2.29.0 \
    Sphinx==7.0.0

ENTRYPOINT /bin/bash

