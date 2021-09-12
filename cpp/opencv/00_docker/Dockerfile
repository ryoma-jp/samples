
# --- build command ---
#   docker build -t cpp/opencv/tensorflow:21.03-tf2-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf2-py3

RUN apt update -y ; \
	apt install libopencv-dev -y

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

