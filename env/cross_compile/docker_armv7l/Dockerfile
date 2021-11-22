
# --- build command ---
#   docker build -t env_xc_armv7l/ubuntu:22.04 .

# --- base image ---
FROM ubuntu:22.04

# --- update packages and install necessary packages ---
RUN apt update ; \
    apt upgrade -y ; \
    apt install -y gcc make gcc-arm-linux-gnueabihf ; \
    apt install -y less file openssh-client openssh-server


