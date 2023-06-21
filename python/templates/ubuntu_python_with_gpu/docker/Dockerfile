
FROM ubuntu:20.04

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && \
    apt install -y wget vim python3-pip

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

RUN pip3 install \
    tensorflow==2.12.0 \
    Sphinx==7.0.0

RUN pip3 install \
    torch==1.10.1+cu111 torchvision==0.11.2+cu111 torchaudio==0.10.1 -f https://download.pytorch.org/whl/cu111/torch_stable.html

ENTRYPOINT /bin/bash

