
FROM ubuntu:23.04

RUN apt update && \
    apt install -y vim python3-pip

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --break-system-packages -r /tmp/requirements.txt

ENTRYPOINT /bin/bash

