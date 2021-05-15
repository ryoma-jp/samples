
# --- build command ---
#   docker build -t measuring_dataset_granularity/tensorflow:21.03-tf2-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf2-py3

RUN apt update
RUN apt upgrade -y
RUN apt install -y libgl1-mesa-dev

RUN pip install pandas opencv-python

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

