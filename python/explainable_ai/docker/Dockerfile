
# --- build command ---
#   docker build --network=host -f Dockerfile -t explainable_ai/tensorflow_gpu .

# --- for machine learning ---
FROM tensorflow/tensorflow:latest-gpu-jupyter

RUN apt update ; \
    apt upgrade -y ; \
    apt install -y libgl1-mesa-dev

RUN pip install opencv-python

