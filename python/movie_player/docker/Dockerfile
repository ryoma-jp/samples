FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04

RUN apt update && apt install -y python3 python3-pip libgl1 wget unrar libglib2.0-0 python3-tk

COPY requirements.txt /tmp/requirements.txt
RUN pip install --break-system-packages -r /tmp/requirements.txt
