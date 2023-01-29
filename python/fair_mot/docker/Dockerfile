
# --- build command ---
#   docker build -f Dockerfile -t fair_mot_env .

# --- for machine learning ---
FROM python:3.8.16

RUN apt update && \
    apt install -y libgl1-mesa-dev

RUN pip install torch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0
RUN pip install -U numpy==1.23.3

