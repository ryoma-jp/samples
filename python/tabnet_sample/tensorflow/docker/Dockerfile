
# --- build command ---
#   docker build -t tabnet/tensorflow:21.03-tf1-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf1-py3

RUN pip install pandas scikit-learn wget

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

