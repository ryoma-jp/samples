
FROM ubuntu:23.04

RUN apt update && \
    apt install -y vim less python3-pip build-essential
    
RUN pip3 install --break-system-packages \
    sorting==1.0.3 \
    Sphinx==7.0.0

ENTRYPOINT /bin/bash

