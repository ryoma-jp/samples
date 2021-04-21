
# --- build command ---
#   docker build -t google-research_sam/tensorflow:21.03-tf2-py3 .

# --- for machine learning ---
FROM nvcr.io/nvidia/tensorflow:21.03-tf2-py3

RUN apt update
RUN apt upgrade -y

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow_probability
RUN pip3 install flax
RUN pip3 install --upgrade jax jaxlib==0.1.65+cuda112 -f https://storage.googleapis.com/jax-releases/jax_releases.html

ENTRYPOINT /usr/local/bin/nvidia_entrypoint.sh

