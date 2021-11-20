
# --- build command ---
#   docker build -t matplotlib_sample/tensorflow:21.03-tf2-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf2-py3

RUN apt update ; \
	apt upgrade -y ; \
	apt install -y libgl1-mesa-dev graphviz python3-tk

RUN pip install matplotlib pandas opencv-python cython pydot

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

