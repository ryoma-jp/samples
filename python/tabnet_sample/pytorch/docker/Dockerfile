
# --- build command ---
#   docker build --network=host -t tabnet/pytorch:21.04-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/pytorch:21.04-py3

RUN apt update
RUN apt upgrade -y
RUN apt install -y libgl1-mesa-dev

RUN pip install pandas opencv-python pytorch-tabnet

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

