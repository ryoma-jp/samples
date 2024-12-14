FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04

RUN apt update && apt install -y python3 python3-pip

RUN pip install --break-system-packages torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 --index-url https://download.pytorch.org/whl/cu124
#RUN pip install --break-system-packages torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
#RUN pip install --break-system-packages torch==1.13.0+cu117 torchvision==0.14.0+cu117 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu117
COPY requirements.txt /tmp/requirements.txt
RUN pip install --break-system-packages -r /tmp/requirements.txt

