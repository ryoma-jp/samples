
# --- build command ---
#   docker build -t tf_sample_v2/tensorflow:ubuntu22.04 .

FROM ubuntu:22.04

RUN apt update && \
    apt upgrade -y xorg-input-abi-24 wget vim python3-pip libgl1-mesa-dev graphviz 

RUN wget -P /tmp/ https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin && \
    mv /tmp/cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \
    wget -P /tmp/ https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda-repo-wsl-ubuntu-11-2-local_11.2.0-1_amd64.deb && \
    dpkg -i /tmp/cuda-repo-wsl-ubuntu-11-2-local_11.2.0-1_amd64.deb && \
    apt-key add /var/cuda-repo-wsl-ubuntu-11-2-local/7fa2af80.pub && \
    apt update && \
    apt -y install cuda

COPY libcudnn8_8.1.0.77-1+cuda11.2_amd64.deb /tmp/
COPY libcudnn8-dev_8.1.0.77-1+cuda11.2_amd64.deb /tmp/
RUN dpkg -i /tmp/libcudnn8_8.1.0.77-1+cuda11.2_amd64.deb /tmp/libcudnn8-dev_8.1.0.77-1+cuda11.2_amd64.deb

RUN pip install \
        tqdm==4.65.0 \
        matplotlib==3.7.1 \
        pandas==2.0.2 \
        opencv-python==4.7.0.72 \
        cython==0.29.35 \
        pydot==1.4.2 \
        tensorflow==2.11.0


ENTRYPOINT /bin/bash

