
# --- build command ---
#   docker build --network=host -f Dockerfile -t jupyter_nb/tensorflow_gpu .

# --- for machine learning ---
FROM tensorflow/tensorflow:latest-gpu-jupyter

RUN apt update ; \
    apt upgrade -y ; \
    apt install -y libgl1-mesa-dev

RUN pip install setuptools==57.4.0
RUN pip install opencv-python natsort numpy pandas xfeat \
                seaborn optuna scikit-learn japanize-matplotlib


