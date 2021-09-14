
# --- build command ---
#   docker build -t cartpole/tensorflow:21.03-tf2-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf2-py3

RUN apt update ; \
	apt upgrade -y ; \
	apt install -y libgl1-mesa-dev graphviz python3-tk python-opengl

RUN pip install matplotlib pandas opencv-python cython pydot
RUN pip install gym pyglet python-opengl

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

