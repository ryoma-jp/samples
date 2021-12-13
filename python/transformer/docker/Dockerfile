
# --- build command ---
#   docker build --network=host -t transformer/tensorflow_gpu .

# --- for machine learning ---
FROM tensorflow/tensorflow:latest-gpu-jupyter

RUN apt update
RUN apt upgrade -y
RUN apt install -y libgl1-mesa-dev

RUN pip install opencv-python scikit-learn pandas 
RUN pip install torch torchvision torchaudio
RUN pip install tensorflow-datasets

