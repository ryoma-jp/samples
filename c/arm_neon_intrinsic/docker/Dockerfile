
# --- build command ---
#   docker build -t arm_neon_intrinsic/ubuntu:22.04 .

# --- for machine learning ---
FROM ubuntu:22.04

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update ; \
    apt upgrade -y ; \
    apt install -y gcc make gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu ; \
    apt install -y less file openssh-client openssh-server


