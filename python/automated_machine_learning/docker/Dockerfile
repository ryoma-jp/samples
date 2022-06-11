
# --- build command ---
#   docker build --network=host -t automated_machine_learning/jupyter .
#

# --- for machine learning ---
FROM tensorflow/tensorflow:latest-gpu-jupyter

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
RUN apt update
RUN apt upgrade -y
RUN apt install -y libgl1-mesa-dev

RUN pip install opencv-python scikit-learn pandas 
RUN pip install torch torchvision torchaudio

# --- Optuna ---
RUN pip install optuna

# --- PyCaret ---
RUN pip install pycaret shap

# --- AutoKeras ---
RUN pip install git+https://github.com/keras-team/keras-tuner.git
RUN pip install autokeras

# --- auto-sklearn ---
RUN pip install auto-sklearn

