FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04

RUN apt update && apt install -y python3 python3-pip libgl1 libglib2.0-0

RUN pip install --break-system-packages torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 --index-url https://download.pytorch.org/whl/cu124
COPY requirements.txt /tmp/requirements.txt
RUN pip install --break-system-packages -r /tmp/requirements.txt
