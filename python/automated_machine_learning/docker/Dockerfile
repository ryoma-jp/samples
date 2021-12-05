
# --- build command ---
#   docker build --network=host -t automated_machine_learning/jupyter .
#

# --- for machine learning ---
FROM tensorflow/tensorflow:latest-gpu-jupyter

RUN apt update
RUN apt upgrade -y
RUN apt install -y libgl1-mesa-dev

RUN pip install opencv-python scikit-learn pandas 
RUN pip install torch torchvision torchaudio
RUN pip install optuna
RUN pip install pycaret shap
