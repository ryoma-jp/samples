
# --- build command ---
#   docker build -t env_xc_aarch64/ubuntu:22.04 .

# --- base image ---
FROM ubuntu:22.04

# --- update packages and install necessary packages ---
RUN apt update ; \
    apt upgrade -y ; \
    apt install -y gcc make gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu ; \
    apt install -y less file openssh-client openssh-server


