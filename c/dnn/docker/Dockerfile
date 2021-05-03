
# --- build command ---
#   docker build -t dnn/tensorflow:21.03-tf2-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf2-py3

RUN apt update
RUN apt upgrade -y
RUN apt install -y libgl1-mesa-dev
RUN apt install -y gdb

RUN pip3 install --upgrade pip
RUN pip3 install pandas opencv-python matplotlib

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

