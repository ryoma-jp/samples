
# --- build command ---
#   docker build -f Dockerfile -t fair_mot_env .

# --- base model is PyTorch v1.7.0 ---
FROM nvcr.io/nvidia/pytorch:20.08-py3

RUN apt update && \
    apt install -y ffmpeg

