
# --- build command ---
#   docker build --network=host -t resize_circle/tensorflow:21.03-tf2-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf2-py3

RUN apt update
RUN apt upgrade -y
RUN apt install -y libgl1-mesa-dev

RUN pip install opencv-python Pillow
RUN pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

