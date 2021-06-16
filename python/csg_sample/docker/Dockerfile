
# --- build command ---
#   docker build -t csg_sample/tensorflow:21.03-tf2-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf2-py3

RUN apt update
RUN apt upgrade -y
RUN apt install -y libgl1-mesa-dev

RUN pip install opencv-python

# --- https://github.com/Dref360/spectral_metric#requirements ---
RUN pip install keras scikit-learn joblib pandas tqdm seaborn
RUN pip install git+https://github.com/DmitryUlyanov/Multicore-TSNE.git

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

