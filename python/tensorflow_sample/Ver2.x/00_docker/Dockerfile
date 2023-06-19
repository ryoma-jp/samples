
# --- build command ---
#   docker build -t tf_sample_v2/tensorflow:21.03-tf2-py3 .

FROM ubuntu:23.04

RUN apt update && \
    apt upgrade -y xorg-input-abi-24 wget vim python3-pip libgl1-mesa-dev graphviz 

RUN wget -P /tmp/ https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin && \
    mv /tmp/cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \
    wget -P /tmp/ https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda-repo-wsl-ubuntu-11-2-local_11.2.0-1_amd64.deb && \
    dpkg -i /tmp/cuda-repo-wsl-ubuntu-11-2-local_11.2.0-1_amd64.deb && \
    apt-key add /var/cuda-repo-wsl-ubuntu-11-2-local/7fa2af80.pub && \
    apt update && \
    apt -y install cuda

COPY cudnn-local-repo-ubuntu2004-8.9.2.26_1.0-1_amd64.deb /tmp/
RUN dpkg -i /tmp/cudnn-local-repo-ubuntu2004-8.9.2.26_1.0-1_amd64.deb && \
    cp /var/cudnn-local-repo-ubuntu2004-8.9.2.26/cudnn-local-6D0A7AE1-keyring.gpg /usr/share/keyrings/ && \
    apt update && \
    apt install libcudnn8 libcudnn8-dev

RUN pip install --break-system-packages \
        matplotlib==3.7.1 \
        pandas==2.0.2 \
        opencv-python==4.7.0.72 \
        cython==0.29.35 \
        pydot==1.4.2 \
        tensorflow==2.12.0


ENTRYPOINT /bin/bash

